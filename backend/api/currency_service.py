"""
Servicio para conversión de monedas usando APIs externas
"""
import requests
from decimal import Decimal
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_exchange_rates(base_currency='USD'):
    """
    Obtiene las tasas de cambio desde una API gratuita
    Usa exchangerate-api.com que es gratis y no requiere autenticación
    """
    try:
        # API gratuita de exchangerate-api.com
        url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            'EUR': Decimal(str(data['rates'].get('EUR', 0.85))),
            'COP': Decimal(str(data['rates'].get('COP', 3900))),
            'USD': Decimal('1.0')
        }
    except requests.exceptions.RequestException as e:
        logger.warning(f'Error al obtener tasas de cambio desde API: {e}')
        # Tasas de cambio por defecto (fallback)
        return {
            'EUR': Decimal('0.85'),
            'COP': Decimal('3900'),
            'USD': Decimal('1.0')
        }
    except Exception as e:
        logger.error(f'Error inesperado al obtener tasas de cambio: {e}')
        # Tasas de cambio por defecto (fallback)
        return {
            'EUR': Decimal('0.85'),
            'COP': Decimal('3900'),
            'USD': Decimal('1.0')
        }


def convert_currency(amount_usd):
    """
    Convierte un monto en USD a EUR y COP usando tasas de cambio actuales
    
    Args:
        amount_usd: Monto en dólares (Decimal o float)
    
    Returns:
        dict: {'usd': amount, 'eur': eur_amount, 'cop': cop_amount}
    """
    if amount_usd is None or amount_usd == 0:
        return {
            'usd': Decimal('0'),
            'eur': Decimal('0'),
            'cop': Decimal('0')
        }
    
    # Convertir a Decimal para mayor precisión
    amount_usd = Decimal(str(amount_usd))
    
    # Obtener tasas de cambio
    rates = get_exchange_rates('USD')
    
    # Calcular conversiones
    eur_amount = (amount_usd * rates['EUR']).quantize(Decimal('0.01'))
    cop_amount = (amount_usd * rates['COP']).quantize(Decimal('0.01'))
    
    return {
        'usd': amount_usd,
        'eur': eur_amount,
        'cop': cop_amount
    }

