from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Empresa, Producto, Inventario


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'rol', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('rol', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'rol'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre', 'telefono', 'fecha_creacion')
    search_fields = ('nit', 'nombre')
    list_filter = ('fecha_creacion',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'empresa', 'precio_cop', 'fecha_creacion')
    search_fields = ('codigo', 'nombre')
    list_filter = ('empresa', 'fecha_creacion')


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'producto', 'cantidad', 'fecha_ingreso', 'transaccion_hash')
    search_fields = ('empresa__nombre', 'producto__nombre')
    list_filter = ('empresa', 'fecha_ingreso')

