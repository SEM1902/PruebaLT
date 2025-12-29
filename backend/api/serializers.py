from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Empresa, Producto, Inventario


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'rol', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class LoginSerializer(serializers.Serializer):
    """Serializer para el login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Debe proporcionar email y contraseña.')
        return attrs


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Empresa"""
    
    class Meta:
        model = Empresa
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    def create(self, validated_data):
        """Crea un producto y convierte automáticamente precios si solo se proporciona USD"""
        precio_usd = validated_data.get('precio_usd')
        
        # Si se proporciona precio_usd, convertir automáticamente a EUR y COP
        if precio_usd:
            from .currency_service import convert_currency
            converted = convert_currency(precio_usd)
            validated_data['precio_eur'] = converted['eur']
            validated_data['precio_cop'] = converted['cop']
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Actualiza un producto y recalcula precios si se actualiza el USD"""
        precio_usd = validated_data.get('precio_usd', instance.precio_usd)
        
        # Si se actualiza precio_usd, recalcular EUR y COP automáticamente
        if 'precio_usd' in validated_data:
            from .currency_service import convert_currency
            converted = convert_currency(precio_usd)
            validated_data['precio_eur'] = converted['eur']
            validated_data['precio_cop'] = converted['cop']
        
        return super().update(instance, validated_data)


class InventarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inventario"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_codigo = serializers.CharField(source='producto.codigo', read_only=True)
    precio_usd = serializers.DecimalField(source='producto.precio_usd', max_digits=10, decimal_places=2, read_only=True)
    precio_eur = serializers.DecimalField(source='producto.precio_eur', max_digits=10, decimal_places=2, read_only=True)
    precio_cop = serializers.DecimalField(source='producto.precio_cop', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Inventario
        fields = '__all__'
        read_only_fields = ('fecha_ingreso', 'fecha_actualizacion', 'transaccion_hash')


class InventarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear inventario"""
    
    class Meta:
        model = Inventario
        fields = ('empresa', 'producto', 'cantidad')

