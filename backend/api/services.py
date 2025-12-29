"""
Servicios para funcionalidades adicionales con IA usando Google Gemini (Plan Gratuito)
"""
import google.generativeai as genai
from django.conf import settings
from .models import User, Empresa, Producto, Inventario
from .utils import send_stock_alert_email
import json


def _get_available_gemini_model():
    """
    Intenta obtener un modelo de Gemini disponible.
    Prueba diferentes modelos en orden de preferencia.
    
    Returns:
        GenerativeModel: Modelo de Gemini disponible, o None si ninguno funciona
    """
    if not settings.GEMINI_API_KEY:
        return None
    
    # Lista de modelos a probar en orden de preferencia
    # Los modelos más recientes primero
    # Nota: Los modelos disponibles pueden variar según la región y el plan
    modelos_a_probar = [
        'gemini-1.5-flash-latest',  # Versión más reciente de flash
        'gemini-1.5-pro-latest',    # Versión más reciente de pro
        'gemini-1.5-flash',         # Versión estable de flash
        'gemini-1.5-pro',            # Versión estable de pro
        'gemini-pro',                # Modelo legacy (puede no estar disponible)
    ]
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Intentar listar modelos disponibles primero
    try:
        available_models = genai.list_models()
        # Filtrar modelos que soportan generateContent
        supported_models = []
        for m in available_models:
            try:
                # Intentar acceder a los atributos del modelo
                model_name = getattr(m, 'name', None) or getattr(m, 'display_name', None) or str(m)
                methods = getattr(m, 'supported_generation_methods', [])
                
                if model_name and ('generateContent' in methods or len(methods) == 0):
                    # Limpiar el nombre del modelo
                    model_clean = model_name.replace('models/', '')
                    supported_models.append(model_clean)
            except Exception:
                continue
        
        # Priorizar modelos de nuestra lista que estén disponibles
        for modelo_preferido in modelos_a_probar:
            modelo_limpio = modelo_preferido.replace('models/', '')
            if modelo_limpio in supported_models:
                try:
                    return genai.GenerativeModel(modelo_limpio)
                except Exception:
                    continue
        
        # Si no encontramos ninguno de los preferidos, usar el primero disponible
        if supported_models:
            try:
                return genai.GenerativeModel(supported_models[0])
            except Exception:
                pass
    except Exception:
        # Si falla list_models, intentar directamente con los modelos preferidos
        pass
    
    # Fallback: intentar cada modelo directamente
    last_error = None
    for modelo in modelos_a_probar:
        modelo_limpio = modelo.replace('models/', '')
        try:
            model = genai.GenerativeModel(modelo_limpio)
            # Intentar una llamada de prueba para verificar que el modelo funciona
            # (No generamos contenido, solo verificamos que el modelo existe)
            return model
        except Exception as e:
            last_error = e
            continue
    
    # Si llegamos aquí, ningún modelo funcionó
    # El error se manejará en las funciones que llaman a esta
    return None


def get_ai_product_suggestions(producto_nombre, caracteristicas):
    """Obtiene sugerencias de productos usando OpenAI"""
    
    # Generar sugerencias básicas como fallback
    def get_basic_suggestions(nombre, caracteristicas):
        """Genera sugerencias básicas basadas en el producto"""
        sugerencias = []
        nombre_lower = nombre.lower()
        caracteristicas_lower = caracteristicas.lower() if caracteristicas else ""
        texto_completo = f"{nombre_lower} {caracteristicas_lower}"
        
        # Categorías más específicas con sugerencias detalladas
        # Tecnología y electrónicos
        if any(palabra in texto_completo for palabra in ['computador', 'laptop', 'pc', 'ordenador', 'portatil']):
            sugerencias = [
                "Mouse inalámbrico",
                "Teclado mecánico",
                "Monitor adicional"
            ]
        elif any(palabra in texto_completo for palabra in ['telefono', 'smartphone', 'celular', 'movil', 'iphone', 'android']):
            sugerencias = [
                "Cable de carga USB-C/Lightning",
                "Funda protectora resistente",
                "Auriculares inalámbricos"
            ]
        elif any(palabra in texto_completo for palabra in ['tablet', 'ipad']):
            sugerencias = [
                "Estuche con teclado",
                "Lápiz digital compatible",
                "Soporte ajustable"
            ]
        elif any(palabra in texto_completo for palabra in ['electronico', 'tecnologia', 'gadget', 'dispositivo']):
            sugerencias = [
                "Cable de carga compatible",
                "Funda o protector",
                "Accesorio de soporte"
            ]
        # Ropa y moda
        elif any(palabra in texto_completo for palabra in ['camisa', 'camiseta', 'polo', 'blusa']):
            sugerencias = [
                "Pantalón o falda coordinada",
                "Cinturón complementario",
                "Chaqueta o abrigo"
            ]
        elif any(palabra in texto_completo for palabra in ['pantalon', 'jeans', 'pantalones']):
            sugerencias = [
                "Cinturón de cuero",
                "Zapatos o zapatillas",
                "Camisa o blusa"
            ]
        elif any(palabra in texto_completo for palabra in ['vestido', 'falda']):
            sugerencias = [
                "Zapatos de tacón o planos",
                "Bolso o cartera",
                "Accesorios de joyería"
            ]
        elif any(palabra in texto_completo for palabra in ['ropa', 'vestimenta', 'moda', 'prenda']):
            sugerencias = [
                "Complemento de moda relacionado",
                "Accesorio de vestimenta",
                "Producto de cuidado textil"
            ]
        # Alimentos y bebidas
        elif any(palabra in texto_completo for palabra in ['bebida', 'refresco', 'jugo', 'agua', 'cerveza', 'vino']):
            sugerencias = [
                "Vaso o copa apropiada",
                "Hielo o enfriador",
                "Snacks complementarios"
            ]
        elif any(palabra in texto_completo for palabra in ['comida', 'alimento', 'comestible', 'snack']):
            sugerencias = [
                "Plato o recipiente para servir",
                "Utensilios de cocina",
                "Bebida complementaria"
            ]
        # Herramientas y construcción
        elif any(palabra in texto_completo for palabra in ['herramienta', 'taladro', 'martillo', 'destornillador']):
            sugerencias = [
                "Caja de herramientas",
                "Guantes de protección",
                "Accesorios o repuestos"
            ]
        # Muebles
        elif any(palabra in texto_completo for palabra in ['mueble', 'silla', 'mesa', 'sofa', 'cama']):
            sugerencias = [
                "Almohadas o cojines",
                "Mesa auxiliar",
                "Lámpara o iluminación"
            ]
        # Libros y material educativo
        elif any(palabra in texto_completo for palabra in ['libro', 'texto', 'manual', 'guia']):
            sugerencias = [
                "Marcador o resaltador",
                "Cuaderno o libreta",
                "Estuche o portafolio"
            ]
        # Deportes
        elif any(palabra in texto_completo for palabra in ['deporte', 'futbol', 'balon', 'pelota', 'gimnasio']):
            sugerencias = [
                "Equipamiento deportivo relacionado",
                "Ropa deportiva",
                "Accesorios de entrenamiento"
            ]
        # Si no se detecta ninguna categoría específica, analizar palabras clave más generales
        else:
            # Intentar detectar el tipo de producto por palabras más generales
            if any(palabra in texto_completo for palabra in ['cable', 'conexion', 'conector']):
                sugerencias = [
                    "Adaptador compatible",
                    "Extensión o prolongador",
                    "Organizador de cables"
                ]
            elif any(palabra in texto_completo for palabra in ['bateria', 'pilas', 'energia']):
                sugerencias = [
                    "Cargador compatible",
                    "Cable de carga",
                    "Power bank o banco de energía"
                ]
            elif any(palabra in texto_completo for palabra in ['limpieza', 'detergente', 'jabon', 'shampoo']):
                sugerencias = [
                    "Esponja o cepillo",
                    "Recipiente o dispensador",
                    "Producto complementario de cuidado"
                ]
            else:
                # Si realmente no se puede determinar, dar sugerencias más genéricas pero útiles
                sugerencias = [
                    f"Accesorio compatible para {nombre}",
                    "Producto complementario relacionado",
                    "Solución adicional recomendada"
                ]
        
        return "\n".join([f"- {sug}" for sug in sugerencias])
    
    # Si no hay API key, retornar sugerencias básicas
    if not settings.GEMINI_API_KEY:
        return get_basic_suggestions(producto_nombre, caracteristicas)
    
    try:
        # Obtener modelo disponible
        model = _get_available_gemini_model()
        if not model:
            return get_basic_suggestions(producto_nombre, caracteristicas)
        
        prompt = f"""
        Eres un asistente experto en sugerencias de productos para inventarios.
        
        Basándote en el siguiente producto:
        Nombre: {producto_nombre}
        Características: {caracteristicas}
        
        Proporciona 3 sugerencias de productos complementarios o relacionados que podrían interesar a los clientes.
        Formato: Lista con nombres cortos de productos.
        """
        
        response = model.generate_content(prompt)
        
        return response.text.strip()
    
    except Exception as e:
        error_str = str(e).lower()
        
        # Si hay error con la IA, retornar sugerencias básicas
        return get_basic_suggestions(producto_nombre, caracteristicas)


def get_inventory_predictions(inventario_data):
    """
    Analiza el historial de inventario y predice cuándo un producto se quedará sin stock usando IA
    
    Args:
        inventario_data: Lista de diccionarios con información del inventario
            Cada diccionario debe tener: producto_nombre, cantidad, fecha_ingreso, fecha_actualizacion, empresa_nombre
    
    Returns:
        Lista de alertas con predicciones
    """
    # Primero, validar productos con bajo stock directamente (fallback si IA falla o no está configurada)
    alerts_basicas = []
    # Obtener emails de administradores para enviar alertas
    administradores = User.objects.filter(rol=User.Rol.ADMINISTRADOR)
    admin_emails = [admin.email for admin in administradores if admin.email]
    
    for item in inventario_data:
        cantidad = item.get('cantidad', 0)
        producto_nombre = item.get('producto_nombre', '')
        empresa_nombre = item.get('empresa_nombre', '')
        
        if cantidad <= 10:
            if cantidad == 0:
                dias = 0
                nivel = 'ALTO'
                mensaje = f"El producto {producto_nombre} está SIN STOCK. Reabastecimiento urgente requerido."
            elif cantidad <= 3:
                dias = 1
                nivel = 'ALTO'
                mensaje = f"El producto {producto_nombre} tiene stock CRÍTICO ({cantidad} unidades). Quiebre de inventario inminente en 1-2 días."
            elif cantidad <= 5:
                dias = 3
                nivel = 'ALTO'
                mensaje = f"El producto {producto_nombre} tiene stock MUY BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 3 días."
            else:  # 6-10 unidades
                dias = 7
                nivel = 'MEDIO'
                mensaje = f"El producto {producto_nombre} tiene stock BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 7 días."
            
            alert_data = {
                'producto': producto_nombre,
                'empresa': empresa_nombre,
                'cantidad_actual': cantidad,
                'dias_hasta_quiebre': dias,
                'alerta': mensaje,
                'nivel_riesgo': nivel
            }
            alerts_basicas.append(alert_data)
            
            # Enviar email de alerta si es nivel ALTO (crítico o muy bajo)
            if nivel == 'ALTO' and admin_emails:
                for admin_email in admin_emails:
                    try:
                        send_stock_alert_email(
                            producto_nombre=producto_nombre,
                            empresa_nombre=empresa_nombre,
                            cantidad=cantidad,
                            dias_hasta_quiebre=dias,
                            nivel_riesgo=nivel,
                            admin_email=admin_email
                        )
                    except Exception as e:
                        # No interrumpir el proceso si falla el envío de email
                        print(f"Error al enviar email de alerta a {admin_email}: {str(e)}")
    
    # Si no hay API key, retornar alertas básicas
    if not settings.GEMINI_API_KEY:
        return alerts_basicas
    
    try:
        # Obtener modelo disponible
        model = _get_available_gemini_model()
        if not model:
            return alerts_basicas
        
        # Preparar datos para el análisis
        productos_info = []
        for item in inventario_data:
            productos_info.append({
                'producto': item.get('producto_nombre', ''),
                'cantidad_actual': item.get('cantidad', 0),
                'empresa': item.get('empresa_nombre', ''),
                'fecha_ingreso': item.get('fecha_ingreso', ''),
                'fecha_actualizacion': item.get('fecha_actualizacion', '')
            })
        
        # Crear prompt más específico para Gemini
        prompt = f"""
        Eres un experto en análisis de inventario y predicción de stock. DEBES detectar productos con bajo stock (<=10 unidades) y generar alertas. Responde siempre en formato JSON válido.
        
        Analiza el siguiente inventario de productos y predice cuándo cada producto se quedará sin stock.
        
        Datos del inventario:
        {productos_info}
        
        REGLAS IMPORTANTES:
        1. Si un producto tiene cantidad 0: nivel_riesgo = "ALTO", dias_hasta_quiebre = 0, alerta = "SIN STOCK - Reabastecimiento urgente"
        2. Si un producto tiene cantidad 1-3: nivel_riesgo = "ALTO", dias_hasta_quiebre = 1-2, alerta debe mencionar stock CRÍTICO
        3. Si un producto tiene cantidad 4-5: nivel_riesgo = "ALTO", dias_hasta_quiebre = 3, alerta debe mencionar stock MUY BAJO
        4. Si un producto tiene cantidad 6-10: nivel_riesgo = "MEDIO", dias_hasta_quiebre = 5-7, alerta debe mencionar stock BAJO
        5. Si un producto tiene cantidad 11-20: nivel_riesgo = "BAJO", dias_hasta_quiebre = 10-15
        6. Si un producto tiene cantidad > 20: nivel_riesgo = "NINGUNO", dias_hasta_quiebre = null
        
        OBLIGATORIO: TODOS los productos con cantidad <= 10 DEBEN tener nivel_riesgo diferente de "NINGUNO" y dias_hasta_quiebre debe ser un número (nunca null).
        
        Responde SOLO con un JSON array de objetos, cada uno con este formato:
        {{
            "producto": "nombre del producto",
            "empresa": "nombre de la empresa",
            "cantidad_actual": número,
            "dias_hasta_quiebre": número o null,
            "alerta": "mensaje de alerta descriptivo",
            "nivel_riesgo": "ALTO", "MEDIO", "BAJO" o "NINGUNO"
        }}
        
        Responde SOLO con el JSON, sin texto adicional.
        """
        
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        # Limpiar el resultado (puede tener markdown code blocks)
        if result.startswith('```'):
            result = result.split('```')[1]
            if result.startswith('json'):
                result = result[4:]
            result = result.strip()
        
        import json
        predictions = json.loads(result)
        
        # Procesar predicciones y asegurar que productos con bajo stock siempre generen alertas
        alerts = []
        productos_procesados = set()
        
        # Obtener emails de todos los administradores
        administradores = User.objects.filter(rol=User.Rol.ADMINISTRADOR)
        admin_emails = [admin.email for admin in administradores if admin.email]
        
        for pred in predictions:
            cantidad = pred.get('cantidad_actual', 0)
            nivel_riesgo = pred.get('nivel_riesgo', 'NINGUNO')
            dias_hasta_quiebre = pred.get('dias_hasta_quiebre')
            producto_nombre = pred.get('producto', '')
            empresa_nombre = pred.get('empresa', '')
            
            # Si tiene bajo stock (<=10), SIEMPRE generar alerta
            if cantidad <= 10:
                if nivel_riesgo == 'NINGUNO' or dias_hasta_quiebre is None:
                    # Corregir automáticamente si la IA no detectó el riesgo
                    if cantidad == 0:
                        dias_hasta_quiebre = 0
                        nivel_riesgo = 'ALTO'
                        alerta = f"El producto {producto_nombre} está SIN STOCK. Reabastecimiento urgente requerido."
                    elif cantidad <= 3:
                        dias_hasta_quiebre = 1
                        nivel_riesgo = 'ALTO'
                        alerta = f"El producto {producto_nombre} tiene stock CRÍTICO ({cantidad} unidades). Quiebre de inventario inminente."
                    elif cantidad <= 5:
                        dias_hasta_quiebre = 3
                        nivel_riesgo = 'ALTO'
                        alerta = f"El producto {producto_nombre} tiene stock MUY BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 3 días."
                    else:  # 6-10
                        dias_hasta_quiebre = 7
                        nivel_riesgo = 'MEDIO'
                        alerta = f"El producto {producto_nombre} tiene stock BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 7 días."
                else:
                    alerta = pred.get('alerta', f"El producto {producto_nombre} tendrá quiebre de inventario en {dias_hasta_quiebre} días")
                
                alert_data = {
                    'producto': producto_nombre,
                    'empresa': empresa_nombre,
                    'cantidad_actual': cantidad,
                    'dias_hasta_quiebre': dias_hasta_quiebre,
                    'alerta': alerta,
                    'nivel_riesgo': nivel_riesgo
                }
                alerts.append(alert_data)
                productos_procesados.add((producto_nombre, empresa_nombre))
                
                # Enviar email de alerta si es nivel ALTO (crítico o muy bajo)
                if nivel_riesgo == 'ALTO' and admin_emails:
                    for admin_email in admin_emails:
                        try:
                            send_stock_alert_email(
                                producto_nombre=producto_nombre,
                                empresa_nombre=empresa_nombre,
                                cantidad=cantidad,
                                dias_hasta_quiebre=dias_hasta_quiebre,
                                nivel_riesgo=nivel_riesgo,
                                admin_email=admin_email
                            )
                        except Exception as e:
                            # No interrumpir el proceso si falla el envío de email
                            print(f"Error al enviar email de alerta a {admin_email}: {str(e)}")
            # Si tiene stock moderado o alto pero la IA detectó riesgo, incluirla
            elif nivel_riesgo != 'NINGUNO' and dias_hasta_quiebre is not None:
                alerts.append({
                    'producto': producto_nombre,
                    'empresa': empresa_nombre,
                    'cantidad_actual': cantidad,
                    'dias_hasta_quiebre': dias_hasta_quiebre,
                    'alerta': pred.get('alerta', f"El producto {producto_nombre} tendrá quiebre de inventario en {dias_hasta_quiebre} días"),
                    'nivel_riesgo': nivel_riesgo
                })
                productos_procesados.add((producto_nombre, empresa_nombre))
        
        # Asegurar que todos los productos con bajo stock estén en las alertas
        # Obtener emails de administradores si no se obtuvieron antes
        if not admin_emails:
            administradores = User.objects.filter(rol=User.Rol.ADMINISTRADOR)
            admin_emails = [admin.email for admin in administradores if admin.email]
        
        for item in inventario_data:
            cantidad = item.get('cantidad', 0)
            producto = item.get('producto_nombre', '')
            empresa = item.get('empresa_nombre', '')
            key = (producto, empresa)
            
            if cantidad <= 10 and key not in productos_procesados:
                # Agregar alerta básica si no fue procesada por la IA
                if cantidad == 0:
                    dias = 0
                    nivel = 'ALTO'
                    mensaje = f"El producto {producto} está SIN STOCK. Reabastecimiento urgente requerido."
                elif cantidad <= 3:
                    dias = 1
                    nivel = 'ALTO'
                    mensaje = f"El producto {producto} tiene stock CRÍTICO ({cantidad} unidades). Quiebre de inventario inminente."
                elif cantidad <= 5:
                    dias = 3
                    nivel = 'ALTO'
                    mensaje = f"El producto {producto} tiene stock MUY BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 3 días."
                else:  # 6-10
                    dias = 7
                    nivel = 'MEDIO'
                    mensaje = f"El producto {producto} tiene stock BAJO ({cantidad} unidades). Quiebre de inventario en aproximadamente 7 días."
                
                alert_data = {
                    'producto': producto,
                    'empresa': empresa,
                    'cantidad_actual': cantidad,
                    'dias_hasta_quiebre': dias,
                    'alerta': mensaje,
                    'nivel_riesgo': nivel
                }
                alerts.append(alert_data)
                
                # Enviar email de alerta si es nivel ALTO (crítico o muy bajo)
                if nivel == 'ALTO' and admin_emails:
                    for admin_email in admin_emails:
                        try:
                            send_stock_alert_email(
                                producto_nombre=producto,
                                empresa_nombre=empresa,
                                cantidad=cantidad,
                                dias_hasta_quiebre=dias,
                                nivel_riesgo=nivel,
                                admin_email=admin_email
                            )
                        except Exception as e:
                            # No interrumpir el proceso si falla el envío de email
                            print(f"Error al enviar email de alerta a {admin_email}: {str(e)}")
        
        return alerts
    
    except Exception as e:
        error_str = str(e).lower()
        
        # Si hay error con la IA, retornar alertas básicas basadas en cantidad
        if 'insufficient_quota' in error_str or 'quota' in error_str:
            return alerts_basicas
        elif 'invalid_api_key' in error_str or 'authentication' in error_str:
            return alerts_basicas
        else:
            # En caso de cualquier otro error, retornar alertas básicas
            return alerts_basicas


def _search_in_data(question, productos_data, empresas_data, inventarios_data):
    """
    Busca información en los datos del sistema sin usar IA.
    Retorna respuesta si encuentra información relevante, None si no.
    """
    question_lower = question.lower()
    
    # Buscar productos por nombre
    productos_encontrados = []
    for prod in productos_data:
        if (question_lower in prod['nombre'].lower() or 
            question_lower in prod['caracteristicas'].lower() or
            question_lower in prod['codigo'].lower()):
            productos_encontrados.append(prod)
    
    if productos_encontrados:
        respuesta = "**Productos encontrados:**\n\n"
        for prod in productos_encontrados:
            respuesta += f"📦 **{prod['nombre']}** (Código: {prod['codigo']})\n"
            respuesta += f"   - Empresa: {prod['empresa']}\n"
            respuesta += f"   - Precio USD: ${prod['precio_usd']:,.2f}\n"
            respuesta += f"   - Precio EUR: €{prod['precio_eur']:,.2f}\n"
            respuesta += f"   - Precio COP: ${prod['precio_cop']:,.2f}\n"
            respuesta += f"   - Características: {prod['caracteristicas']}\n\n"
            
            # Buscar en inventario
            inv_encontrados = [inv for inv in inventarios_data if inv['producto'] == prod['nombre']]
            if inv_encontrados:
                respuesta += "   **En inventario:**\n"
                for inv in inv_encontrados:
                    respuesta += f"   - Empresa: {inv['empresa']}\n"
                    respuesta += f"   - Cantidad: {inv['cantidad']} unidades\n"
                    respuesta += f"   - Valor total USD: ${inv['valor_total_usd']:,.2f}\n"
                    respuesta += f"   - Valor total EUR: €{inv['valor_total_eur']:,.2f}\n"
                    respuesta += f"   - Valor total COP: ${inv['valor_total_cop']:,.2f}\n\n"
            else:
                respuesta += "   - No hay stock en inventario\n\n"
        
        return respuesta
    
    # Buscar empresas
    empresas_encontradas = []
    for emp in empresas_data:
        if (question_lower in emp['nombre'].lower() or 
            question_lower in emp['nit'].lower()):
            empresas_encontradas.append(emp)
    
    if empresas_encontradas:
        respuesta = "**Empresas encontradas:**\n\n"
        for emp in empresas_encontradas:
            respuesta += f"🏢 **{emp['nombre']}**\n"
            respuesta += f"   - NIT: {emp['nit']}\n"
            respuesta += f"   - Dirección: {emp['direccion']}\n"
            respuesta += f"   - Teléfono: {emp['telefono']}\n\n"
            
            # Buscar productos e inventario de esta empresa
            productos_empresa = [p for p in productos_data if p['empresa'] == emp['nombre']]
            if productos_empresa:
                respuesta += f"   **Productos ({len(productos_empresa)}):**\n"
                for p in productos_empresa:
                    respuesta += f"   - {p['nombre']} (${p['precio_usd']:,.2f} USD)\n"
            
            inv_empresa = [inv for inv in inventarios_data if inv['empresa'] == emp['nombre']]
            if inv_empresa:
                total_cantidad = sum(inv['cantidad'] for inv in inv_empresa)
                total_valor_usd = sum(inv['valor_total_usd'] for inv in inv_empresa)
                respuesta += f"\n   **Inventario:**\n"
                respuesta += f"   - Total unidades: {total_cantidad}\n"
                respuesta += f"   - Valor total USD: ${total_valor_usd:,.2f}\n"
        
        return respuesta
    
    # Preguntas sobre estadísticas generales
    if any(palabra in question_lower for palabra in ['total', 'cuantos', 'cuantas', 'resumen', 'estadisticas']):
        return None  # Se manejará en la función principal
    
    return None


def get_chatbot_response(question, user):
    """
    Responde preguntas del usuario sobre el sistema usando IA con contexto de los datos.
    
    Args:
        question: Pregunta del usuario
        user: Usuario que hace la pregunta
    
    Returns:
        Respuesta del chatbot
    """
    # Obtener datos del sistema para proporcionar contexto
    empresas = Empresa.objects.all()
    productos = Producto.objects.select_related('empresa').all()
    inventarios = Inventario.objects.select_related('empresa', 'producto').all()
    
    # Preparar datos en formato legible
    empresas_data = []
    for emp in empresas:
        empresas_data.append({
            'nit': emp.nit,
            'nombre': emp.nombre,
            'direccion': emp.direccion,
            'telefono': emp.telefono
        })
    
    productos_data = []
    for prod in productos:
        productos_data.append({
            'codigo': prod.codigo,
            'nombre': prod.nombre,
            'caracteristicas': prod.caracteristicas,
            'precio_usd': float(prod.precio_usd),
            'precio_eur': float(prod.precio_eur),
            'precio_cop': float(prod.precio_cop),
            'empresa': prod.empresa.nombre
        })
    
    inventarios_data = []
    for inv in inventarios:
        inventarios_data.append({
            'empresa': inv.empresa.nombre,
            'producto': inv.producto.nombre,
            'codigo_producto': inv.producto.codigo,
            'cantidad': inv.cantidad,
            'precio_usd': float(inv.producto.precio_usd),
            'precio_eur': float(inv.producto.precio_eur),
            'precio_cop': float(inv.producto.precio_cop),
            'valor_total_usd': float(inv.cantidad * inv.producto.precio_usd),
            'valor_total_eur': float(inv.cantidad * inv.producto.precio_eur),
            'valor_total_cop': float(inv.cantidad * inv.producto.precio_cop)
        })
    
    # Calcular estadísticas generales
    total_productos = productos.count()
    total_empresas = empresas.count()
    total_inventario = sum(inv.cantidad for inv in inventarios)
    valor_total_usd = sum(float(inv.cantidad * inv.producto.precio_usd) for inv in inventarios)
    valor_total_eur = sum(float(inv.cantidad * inv.producto.precio_eur) for inv in inventarios)
    valor_total_cop = sum(float(inv.cantidad * inv.producto.precio_cop) for inv in inventarios)
    
    # SIEMPRE intentar usar IA primero si está configurada
    if not settings.GEMINI_API_KEY:
        # Si no hay API key, usar búsqueda básica
        respuesta_basica = _search_in_data(question, productos_data, empresas_data, inventarios_data)
        if respuesta_basica:
            return respuesta_basica
        
        # Si no encuentra nada, retornar respuesta con estadísticas
        respuesta = "**Resumen del sistema:**\n\n"
        respuesta += f"📊 Total de empresas: {total_empresas}\n"
        respuesta += f"📦 Total de productos: {total_productos}\n"
        respuesta += f"📋 Total de unidades en inventario: {total_inventario}\n"
        respuesta += f"💰 Valor total del inventario:\n"
        respuesta += f"   - USD: ${valor_total_usd:,.2f}\n"
        respuesta += f"   - EUR: €{valor_total_eur:,.2f}\n"
        respuesta += f"   - COP: ${valor_total_cop:,.2f}\n\n"
        respuesta += "⚠️ La funcionalidad de IA no está configurada (falta GEMINI_API_KEY).\n\n"
        respuesta += "No encontré información específica sobre tu pregunta. Por favor, intenta con el nombre exacto del producto o empresa."
        return respuesta
    
    try:
        # Obtener modelo disponible
        model = _get_available_gemini_model()
        if not model:
            # Si no hay modelo disponible, usar búsqueda básica
            respuesta_basica = _search_in_data(question, productos_data, empresas_data, inventarios_data)
            if respuesta_basica:
                return respuesta_basica
            
            # Si no encuentra nada, retornar respuesta con estadísticas
            respuesta = "⚠️ **Error con el servicio de IA**: No se pudo conectar con ningún modelo de Gemini disponible.\n\n"
            respuesta += "**Resumen del sistema:**\n\n"
            respuesta += f"📊 Total de empresas: {total_empresas}\n"
            respuesta += f"📦 Total de productos: {total_productos}\n"
            respuesta += f"📋 Total de unidades en inventario: {total_inventario}\n"
            respuesta += f"💰 Valor total del inventario:\n"
            respuesta += f"   - USD: ${valor_total_usd:,.2f}\n"
            respuesta += f"   - EUR: €{valor_total_eur:,.2f}\n"
            respuesta += f"   - COP: ${valor_total_cop:,.2f}\n\n"
            respuesta += "No encontré información específica sobre tu pregunta. Por favor, intenta con el nombre exacto del producto o empresa."
            return respuesta
        
        # Crear contexto con los datos del sistema
        contexto = f"""
        Eres un asistente virtual experto en gestión de inventario, empresas y productos.
        
        DATOS DEL SISTEMA:
        
        RESUMEN GENERAL:
        - Total de empresas: {total_empresas}
        - Total de productos: {total_productos}
        - Total de unidades en inventario: {total_inventario}
        - Valor total del inventario en USD: ${valor_total_usd:,.2f}
        - Valor total del inventario en EUR: €{valor_total_eur:,.2f}
        - Valor total del inventario en COP: ${valor_total_cop:,.2f}
        
        EMPRESAS ({len(empresas_data)}):
        {json.dumps(empresas_data, indent=2, ensure_ascii=False)}
        
        PRODUCTOS ({len(productos_data)}):
        {json.dumps(productos_data, indent=2, ensure_ascii=False)}
        
        INVENTARIO ({len(inventarios_data)}):
        {json.dumps(inventarios_data, indent=2, ensure_ascii=False)}
        
        INSTRUCCIONES:
        1. Responde preguntas sobre empresas, productos, inventario, cantidades, valores, precios en USD/EUR/COP, etc.
        2. Usa los datos proporcionados para dar respuestas precisas y específicas.
        3. Si se pregunta por valores, menciona las tres monedas (USD, EUR, COP) cuando sea relevante.
        4. Si se pregunta por una empresa, producto o inventario específico, busca en los datos y proporciona información detallada.
        5. Responde de forma clara, concisa y amigable en español.
        6. Si no encuentras información específica, indícalo claramente.
        7. Para cálculos de valores totales, usa las cantidades del inventario multiplicadas por los precios.
        """
        
        prompt = f"""
        {contexto}
        
        PREGUNTA DEL USUARIO: {question}
        
        Responde de forma clara y útil usando los datos proporcionados.
        """
        
        response = model.generate_content(prompt)
        
        return response.text.strip()
    
    except Exception as e:
        error_str = str(e).lower()
        error_message = str(e)
        
        # Determinar el tipo de error y mensaje apropiado
        motivo_error = ""
        mostrar_error = True  # Flag para decidir si mostrar el mensaje de error
        
        # Detectar errores de modelo no encontrado (404) - estos son diferentes a límites de cuota
        if '404' in error_str or 'not found' in error_str or 'is not found' in error_str or 'not supported' in error_str:
            motivo_error = "ℹ️ **Nota**: El servicio de IA no está disponible temporalmente. Continuando con búsqueda básica...\n\n"
            mostrar_error = False  # No mostrar error si encontramos resultados en búsqueda básica
        elif 'insufficient_quota' in error_str or ('quota' in error_str and 'exceeded' in error_str):
            motivo_error = "⚠️ **Límite de uso excedido**: Has alcanzado el límite del plan gratuito de Gemini. Por favor, espera unos momentos o verifica tu cuenta en: https://makersuite.google.com/app/apikey\n\n"
        elif 'invalid_api_key' in error_str or 'authentication' in error_str or '401' in error_str or '403' in error_str:
            motivo_error = "⚠️ **Clave API inválida**: La clave de Gemini configurada no es válida. Verifica que GEMINI_API_KEY en el archivo .env sea correcta. Obtén una clave gratuita en: https://makersuite.google.com/app/apikey\n\n"
        elif 'rate_limit' in error_str or '429' in error_str:
            motivo_error = "ℹ️ **Nota**: Demasiadas solicitudes en poco tiempo. Continuando con búsqueda básica...\n\n"
            mostrar_error = False
        elif 'connection' in error_str or 'timeout' in error_str:
            motivo_error = "ℹ️ **Nota**: No se pudo conectar con la API de Gemini. Continuando con búsqueda básica...\n\n"
            mostrar_error = False
        else:
            # Para otros errores, verificar si es un error de límite real
            if ('quota' in error_str or 'limit' in error_str) and ('exceeded' in error_str or 'reached' in error_str):
                motivo_error = "⚠️ **Límite de uso excedido**: Has alcanzado el límite del plan gratuito de Gemini. Por favor, espera unos momentos o verifica tu cuenta en: https://makersuite.google.com/app/apikey\n\n"
            else:
                motivo_error = f"ℹ️ **Nota**: Error con el servicio de IA. Continuando con búsqueda básica...\n\n"
                mostrar_error = False
        
        # Si hay error con la IA, intentar búsqueda básica como fallback
        respuesta_basica = _search_in_data(question, productos_data, empresas_data, inventarios_data)
        if respuesta_basica:
            # Si encontramos resultados, solo mostrar el error si es importante (no para errores temporales)
            return (motivo_error if mostrar_error else "") + respuesta_basica
        
        # Si no encuentra nada, retornar respuesta con estadísticas
        respuesta = motivo_error if mostrar_error else ""
        respuesta += "**Resumen del sistema:**\n\n"
        respuesta += f"📊 Total de empresas: {total_empresas}\n"
        respuesta += f"📦 Total de productos: {total_productos}\n"
        respuesta += f"📋 Total de unidades en inventario: {total_inventario}\n"
        respuesta += f"💰 Valor total del inventario:\n"
        respuesta += f"   - USD: ${valor_total_usd:,.2f}\n"
        respuesta += f"   - EUR: €{valor_total_eur:,.2f}\n"
        respuesta += f"   - COP: ${valor_total_cop:,.2f}\n\n"
        respuesta += "No encontré información específica sobre tu pregunta. Por favor, intenta con el nombre exacto del producto o empresa."
        return respuesta

