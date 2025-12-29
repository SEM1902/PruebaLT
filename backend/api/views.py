from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from .models import User, Empresa, Producto, Inventario
from .serializers import (
    UserSerializer,
    LoginSerializer,
    EmpresaSerializer,
    ProductoSerializer,
    InventarioSerializer,
    InventarioCreateSerializer
)
from .permissions import IsAdministrador, IsAdministradorOrReadOnly
from .utils import generate_pdf, send_pdf_email, generate_blockchain_hash
from .services import get_ai_product_suggestions, get_inventory_predictions, get_chatbot_response


class LoginView(APIView):
    """Vista para inicio de sesión"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para Empresa"""
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAdministradorOrReadOnly]
    
    def get_queryset(self):
        queryset = Empresa.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset


class ProductoViewSet(viewsets.ModelViewSet):
    """ViewSet para Producto"""
    queryset = Producto.objects.select_related('empresa').all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdministrador]
    
    def get_queryset(self):
        queryset = Producto.objects.select_related('empresa').all()
        empresa = self.request.query_params.get('empresa', None)
        if empresa:
            queryset = queryset.filter(empresa__nit=empresa)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset
    
    @action(detail=True, methods=['get'])
    def ai_suggestions(self, request, pk=None):
        """Obtiene sugerencias de productos usando IA"""
        producto = self.get_object()
        suggestions = get_ai_product_suggestions(producto.nombre, producto.caracteristicas)
        return Response({'suggestions': suggestions})
    
    @action(detail=False, methods=['get'], url_path='convert-currency')
    def convert_currency(self, request):
        """Convierte un monto en USD a EUR y COP"""
        from .currency_service import convert_currency as convert_currency_service
        
        amount_usd = request.query_params.get('amount')
        if not amount_usd:
            return Response(
                {'error': 'Debe proporcionar el parámetro "amount" con el monto en USD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount_usd = float(amount_usd)
            converted = convert_currency_service(amount_usd)
            return Response({
                'usd': float(converted['usd']),
                'eur': float(converted['eur']),
                'cop': float(converted['cop'])
            })
        except ValueError:
            return Response(
                {'error': 'El monto debe ser un número válido'},
                status=status.HTTP_400_BAD_REQUEST
            )


class InventarioViewSet(viewsets.ModelViewSet):
    """ViewSet para Inventario"""
    queryset = Inventario.objects.select_related('empresa', 'producto').all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAdministrador]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InventarioCreateSerializer
        return InventarioSerializer
    
    def get_queryset(self):
        queryset = Inventario.objects.select_related('empresa', 'producto').all()
        empresa = self.request.query_params.get('empresa', None)
        if empresa:
            queryset = queryset.filter(empresa__nit=empresa)
        return queryset
    
    def perform_create(self, serializer):
        """Crea el inventario y genera hash de blockchain"""
        inventario = serializer.save()
        
        # Generar hash de blockchain para la transacción
        hash_transaccion = generate_blockchain_hash(
            inventario.empresa.nit,
            inventario.producto.codigo,
            inventario.cantidad
        )
        inventario.transaccion_hash = hash_transaccion
        inventario.save()
    
    def perform_update(self, serializer):
        """Actualiza el inventario y regenera hash de blockchain"""
        inventario = serializer.save()
        
        # Regenerar hash de blockchain para la transacción actualizada
        hash_transaccion = generate_blockchain_hash(
            inventario.empresa.nit,
            inventario.producto.codigo,
            inventario.cantidad
        )
        inventario.transaccion_hash = hash_transaccion
        inventario.save()
    
    @action(detail=False, methods=['get'], url_path='empresa/(?P<empresa_nit>[^/.]+)')
    def by_empresa(self, request, empresa_nit=None):
        """Obtiene inventario por empresa"""
        inventarios = self.queryset.filter(empresa__nit=empresa_nit)
        serializer = self.get_serializer(inventarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='pdf/(?P<empresa_nit>[^/.]+)')
    def download_pdf(self, request, empresa_nit=None):
        """Descarga PDF del inventario de una empresa"""
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
            inventarios = Inventario.objects.filter(empresa=empresa).select_related('producto')
            
            if not inventarios.exists():
                return Response(
                    {'error': 'No hay productos en el inventario de esta empresa'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            pdf_buffer = generate_pdf(inventarios, empresa.nombre)
            response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="inventario_{empresa.nombre.replace(" ", "_")}.pdf"'
            return response
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], url_path='send-pdf/(?P<empresa_nit>[^/.]+)')
    def send_pdf_email(self, request, empresa_nit=None):
        """Envía PDF del inventario por email"""
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
            inventarios = Inventario.objects.filter(empresa=empresa).select_related('producto')
            
            if not inventarios.exists():
                return Response(
                    {'error': 'No hay productos en el inventario de esta empresa'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            recipient_email = request.data.get('email')
            if not recipient_email:
                return Response(
                    {'error': 'Debe proporcionar un email'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pdf_buffer = generate_pdf(inventarios, empresa.nombre)
            send_pdf_email(pdf_buffer, empresa.nombre, recipient_email)
            
            return Response({
                'message': f'PDF enviado exitosamente a {recipient_email}'
            }, status=status.HTTP_200_OK)
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al enviar email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='predictions')
    def inventory_predictions(self, request):
        """Obtiene predicciones de inventario usando IA"""
        try:
            # Obtener todos los inventarios con información relevante
            inventarios = Inventario.objects.select_related('empresa', 'producto').all()
            
            # Filtrar por empresa si se proporciona
            empresa_nit = request.query_params.get('empresa', None)
            if empresa_nit:
                inventarios = inventarios.filter(empresa__nit=empresa_nit)
            
            # Preparar datos para el análisis
            inventario_data = []
            for inv in inventarios:
                inventario_data.append({
                    'producto_nombre': inv.producto.nombre,
                    'producto_codigo': inv.producto.codigo,
                    'cantidad': inv.cantidad,
                    'empresa_nombre': inv.empresa.nombre,
                    'empresa_nit': inv.empresa.nit,
                    'fecha_ingreso': inv.fecha_ingreso.strftime('%Y-%m-%d') if inv.fecha_ingreso else '',
                    'fecha_actualizacion': inv.fecha_actualizacion.strftime('%Y-%m-%d') if inv.fecha_actualizacion else ''
                })
            
            if not inventario_data:
                return Response({
                    'alerts': [],
                    'message': 'No hay inventario disponible para analizar'
                })
            
            # Obtener predicciones usando IA
            alerts = get_inventory_predictions(inventario_data)
            
            return Response({
                'alerts': alerts,
                'total_alerts': len(alerts)
            })
        except Exception as e:
            return Response(
                {'error': f'Error al obtener predicciones: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatbotView(APIView):
    """Vista para el chatbot con IA"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Responde preguntas del usuario usando IA con contexto del sistema"""
        try:
            question = request.data.get('question', '').strip()
            
            if not question:
                return Response(
                    {'error': 'Debe proporcionar una pregunta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener respuesta del chatbot
            response = get_chatbot_response(question, request.user)
            
            return Response({
                'response': response,
                'question': question
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al procesar la pregunta: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

