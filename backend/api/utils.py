"""
Utilidades para el proyecto
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from io import BytesIO
from .models import Inventario
import hashlib
import json
from datetime import datetime


def generate_pdf(inventario_list, empresa_nombre):
    """Genera un PDF con la información del inventario"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.HexColor('#2C3E50')
    )
    
    # Contenido del PDF
    story = []
    
    # Título
    title = Paragraph(f"Inventario - {empresa_nombre}", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Fecha de generación
    fecha = Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    story.append(fecha)
    story.append(Spacer(1, 0.3*inch))
    
    # Datos de la tabla
    data = [['Código', 'Producto', 'Cantidad', 'Precio USD', 'Precio EUR', 'Precio COP']]
    
    for inv in inventario_list:
        data.append([
            inv.producto.codigo,
            inv.producto.nombre,
            str(inv.cantidad),
            f"${inv.producto.precio_usd}",
            f"€{inv.producto.precio_eur}",
            f"${inv.producto.precio_cop}"
        ])
    
    # Crear tabla
    table = Table(data, colWidths=[1*inch, 2*inch, 0.8*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(table)
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def send_pdf_email(pdf_buffer, empresa_nombre, recipient_email):
    """Envía el PDF por email usando API REST (SendGrid, Mailgun, etc.)"""
    # En producción se usaría una API REST como SendGrid o Mailgun
    # Por ahora usare el backend de Django con SMTP
    
    # Verificar que la configuración de email esté completa
    if not settings.EMAIL_HOST or settings.EMAIL_HOST == '':
        raise ValueError(
            'EMAIL_HOST no está configurado. '
            'Por favor, configure EMAIL_HOST en el archivo .env (ej: smtp.gmail.com)'
        )
    
    # Detectar error común: EMAIL_HOST configurado con un email en lugar del servidor SMTP
    if '@' in settings.EMAIL_HOST:
        raise ValueError(
            f'ERROR: EMAIL_HOST está configurado incorrectamente con "{settings.EMAIL_HOST}".\n'
            'EMAIL_HOST debe ser el servidor SMTP, no tu email.\n'
            'Configuración correcta en .env:\n'
            '  EMAIL_HOST=smtp.gmail.com\n'
            '  EMAIL_HOST_USER=estradamontoyasimon803@gmail.com\n'
            '  EMAIL_HOST_PASSWORD=qvjvacfkqnqqufmk'
        )
    
    if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == '':
        raise ValueError(
            'EMAIL_HOST_USER no está configurado. '
            'Por favor, configure EMAIL_HOST_USER en el archivo .env (ej: tu-email@gmail.com)'
        )
    
    if not settings.EMAIL_HOST_PASSWORD or settings.EMAIL_HOST_PASSWORD == '':
        raise ValueError(
            'EMAIL_HOST_PASSWORD no está configurado. '
            'Por favor, configure EMAIL_HOST_PASSWORD en el archivo .env. '
            'Para Gmail, necesita usar una "Contraseña de aplicación"'
        )
    
    pdf_buffer.seek(0)
    
    email = EmailMessage(
        subject=f'Inventario de {empresa_nombre}',
        body=f'Adjunto encontrará el inventario de {empresa_nombre} generado el {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}.',
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )
    
    email.attach(
        f'inventario_{empresa_nombre.replace(" ", "_")}.pdf',
        pdf_buffer.read(),
        'application/pdf'
    )
    
    try:
        email.send()
        return True
    except Exception as e:
        error_message = str(e)
        error_str = str(e)
        
        # Errores de resolución de hostname
        if 'nodename nor servname provided' in error_str or 'not known' in error_str:
            raise ValueError(
                f'No se puede conectar al servidor de email "{settings.EMAIL_HOST}". '
                'Verifica que EMAIL_HOST esté configurado correctamente en el archivo .env. '
                'Para Gmail usa: smtp.gmail.com'
            )
      #  .atomic(using=settings.DATABASES['default']['NAME'])
        # Errores de autenticación
        if 'Authentication Required' in error_message or '530' in error_message:
            raise ValueError(
                'Error de autenticación con el servidor de email. '
                'Para Gmail, necesitas usar una "Contraseña de aplicación" en lugar de tu contraseña normal. '
                'Consulta: https://support.google.com/accounts/answer/185833'
            )
        
        # Error de remitente no configurado
        if 'webmaster@localhost' in error_message:
            raise ValueError(
                'EMAIL_HOST_USER no está configurado correctamente en el archivo .env'
            )
        
        # Error genérico
        raise ValueError(f'Error al enviar email: {error_str}')


def send_stock_alert_email(producto_nombre, empresa_nombre, cantidad, dias_hasta_quiebre, nivel_riesgo, admin_email):
    """Envía un correo de alerta de stock bajo al administrador"""
    # Verificar que la configuración de email esté completa
    if not settings.EMAIL_HOST or settings.EMAIL_HOST == '':
        return False
    
    if '@' in settings.EMAIL_HOST:
        return False
    
    if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == '':
        return False
    
    if not settings.EMAIL_HOST_PASSWORD or settings.EMAIL_HOST_PASSWORD == '':
        return False
    
    # Determinar el tipo de alerta y el mensaje
    if nivel_riesgo == 'ALTO':
        if cantidad == 0:
            tipo_alerta = "🚨 ALERTA CRÍTICA: SIN STOCK"
            mensaje_principal = f"El producto <strong>{producto_nombre}</strong> de la empresa <strong>{empresa_nombre}</strong> está <strong>SIN STOCK</strong>."
            accion = "Reabastecimiento URGENTE requerido inmediatamente."
        elif cantidad <= 3:
            tipo_alerta = "🚨 ALERTA CRÍTICA: STOCK CRÍTICO"
            mensaje_principal = f"El producto <strong>{producto_nombre}</strong> de la empresa <strong>{empresa_nombre}</strong> tiene stock <strong>CRÍTICO</strong> ({cantidad} unidades)."
            accion = f"Quiebre de inventario inminente en {dias_hasta_quiebre} día(s). Se requiere reabastecimiento urgente."
        else:
            tipo_alerta = "⚠️ ALERTA: STOCK MUY BAJO"
            mensaje_principal = f"El producto <strong>{producto_nombre}</strong> de la empresa <strong>{empresa_nombre}</strong> tiene stock <strong>MUY BAJO</strong> ({cantidad} unidades)."
            accion = f"Quiebre de inventario previsto en aproximadamente {dias_hasta_quiebre} días. Se recomienda reabastecimiento pronto."
    else:
        return False  # Solo enviar emails para alertas ALTO
    
    # Crear el cuerpo del email en HTML
    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-radius: 0 0 5px 5px; }}
            .alert-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; }}
            .critical-box {{ background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 15px 0; }}
            .info {{ background-color: #d1ecf1; border-left: 4px solid #0dcaf0; padding: 15px; margin: 15px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>{tipo_alerta}</h2>
            </div>
            <div class="content">
                <p>{mensaje_principal}</p>
                
                <div class="{'critical-box' if cantidad <= 3 else 'alert-box'}">
                    <h3>Detalles de la Alerta:</h3>
                    <ul>
                        <li><strong>Producto:</strong> {producto_nombre}</li>
                        <li><strong>Empresa:</strong> {empresa_nombre}</li>
                        <li><strong>Cantidad actual:</strong> {cantidad} unidades</li>
                        <li><strong>Días hasta quiebre:</strong> {dias_hasta_quiebre} día(s)</li>
                        <li><strong>Nivel de riesgo:</strong> {nivel_riesgo}</li>
                    </ul>
                </div>
                
                <div class="info">
                    <h3>Acción requerida:</h3>
                    <p>{accion}</p>
                </div>
                
                <p>Por favor, revise el inventario y tome las medidas necesarias para evitar el quiebre de stock.</p>
                
                <div class="footer">
                    <p>Este es un correo automático generado por el sistema de gestión de inventario.</p>
                    <p>Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Versión en texto plano
    body_text = f"""
{tipo_alerta}

{mensaje_principal}

Detalles de la Alerta:
- Producto: {producto_nombre}
- Empresa: {empresa_nombre}
- Cantidad actual: {cantidad} unidades
- Días hasta quiebre: {dias_hasta_quiebre} día(s)
- Nivel de riesgo: {nivel_riesgo}

Acción requerida:
{accion}

Por favor, revise el inventario y tome las medidas necesarias para evitar el quiebre de stock.

Este es un correo automático generado por el sistema de gestión de inventario.
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    """
    
    try:
        email = EmailMessage(
            subject=f'{tipo_alerta} - {producto_nombre} ({empresa_nombre})',
            body=body_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[admin_email],
        )
        email.content_subtype = "html"  # Establecer el contenido como HTML
        email.body = body_html  # Usar la versión HTML
        
        email.send()
        return True
    except Exception as e:
        # No lanzar excepción para no interrumpir el proceso de predicción
        # Solo registrar el error silenciosamente
        print(f"Error al enviar email de alerta: {str(e)}")
        return False


def generate_blockchain_hash(empresa_nit, producto_codigo, cantidad):
    """Genera un hash tipo blockchain para la transacción de inventario"""
    # Simula una transacción de blockchain generando un hash
    transaction_data = {
        'empresa_nit': empresa_nit,
        'producto_codigo': producto_codigo,
        'cantidad': str(cantidad),
        'timestamp': datetime.now().isoformat(),
        'type': 'inventory_transaction'
    }
    
    # Crear hash SHA-256 (similar a blockchain)
    transaction_string = json.dumps(transaction_data, sort_keys=True)
    hash_object = hashlib.sha256(transaction_string.encode())
    hash_hex = '0x' + hash_object.hexdigest()
    
    return hash_hex

