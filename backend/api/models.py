from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el email y password dados"""
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', User.Rol.ADMINISTRADOR)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado"""
    
    class Rol(models.TextChoices):
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        EXTERNO = 'EXTERNO', 'Externo'
    
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.EXTERNO, verbose_name='Rol')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.email


class Empresa(models.Model):
    """Modelo para empresas"""
    nit_validator = RegexValidator(
        regex=r'^\d{9,15}$',
        message='El NIT debe contener entre 9 y 15 dígitos'
    )
    
    nit = models.CharField(
        max_length=15,
        primary_key=True,
        validators=[nit_validator],
        verbose_name='NIT'
    )
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la empresa')
    direccion = models.TextField(verbose_name='Dirección')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.nit}"
    
    def to_domain(self):
        """Convierte el modelo Django a entidad de dominio"""
        from .domain_adapters import EmpresaAdapter
        return EmpresaAdapter.to_domain(self)
    
    @classmethod
    def from_domain(cls, domain_empresa):
        """Crea o actualiza un modelo Django desde una entidad de dominio"""
        from .domain_adapters import EmpresaAdapter
        django_empresa = EmpresaAdapter.to_django(domain_empresa)
        django_empresa.save()
        return django_empresa


class Producto(models.Model):
    """Modelo para productos"""
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=200, verbose_name='Nombre del producto')
    caracteristicas = models.TextField(verbose_name='Características')
    precio_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio USD')
    precio_eur = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio EUR')
    precio_cop = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio COP')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos', verbose_name='Empresa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    def to_domain(self):
        """Convierte el modelo Django a entidad de dominio"""
        from .domain_adapters import ProductoAdapter
        return ProductoAdapter.to_domain(self)
    
    @classmethod
    def from_domain(cls, domain_producto):
        """Crea o actualiza un modelo Django desde una entidad de dominio"""
        from .domain_adapters import ProductoAdapter
        from .models import Empresa
        django_empresa = Empresa.objects.get(nit=domain_producto.empresa_nit)
        django_producto = ProductoAdapter.to_django(domain_producto, django_empresa)
        django_producto.save()
        return django_producto


class Inventario(models.Model):
    """Modelo para inventario de productos por empresa"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='inventarios', verbose_name='Empresa')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventarios', verbose_name='Producto')
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    transaccion_hash = models.CharField(max_length=66, blank=True, null=True, verbose_name='Hash de Transacción (Blockchain)')
    
    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ['empresa', 'producto']
        ordering = ['-fecha_ingreso']
    
    def __str__(self):
        return f"{self.empresa.nombre} - {self.producto.nombre} - Cantidad: {self.cantidad}"
    
    def to_domain(self):
        """Convierte el modelo Django a entidad de dominio"""
        from .domain_adapters import InventarioAdapter
        return InventarioAdapter.to_domain(self)
    
    @classmethod
    def from_domain(cls, domain_inventario):
        """Crea o actualiza un modelo Django desde una entidad de dominio"""
        from .domain_adapters import InventarioAdapter
        from .models import Empresa, Producto
        django_empresa = Empresa.objects.get(nit=domain_inventario.empresa_nit)
        django_producto = Producto.objects.get(codigo=domain_inventario.producto_codigo)
        django_inventario = InventarioAdapter.to_django(domain_inventario, django_empresa, django_producto)
        django_inventario.save()
        return django_inventario

