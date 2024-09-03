from django.contrib import admin
from core.models import Cidadao, User, HistoricoCriminal, HistoricoSaude
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import InformacoesComplementares, User
from .forms import UserCreationFormCustom, UserChangeFormCustom

# Register your models here.
admin.site.register(Cidadao)
admin.site.register(HistoricoSaude)
admin.site.register(HistoricoCriminal)
admin.site.register(InformacoesComplementares)

class UserAdmin(BaseUserAdmin):
    form = UserChangeFormCustom
    add_form = UserCreationFormCustom
    #list display define quais campos serão exibidos na lista de lista de usuarios que fica na interface do django admin
    list_display = ('cpf', 'nome', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('cpf', 'nome', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'nome', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    #define quais campos devem ser pesquisaveis na lista de usuarios aqui foi definido para pesquisar com o cpf
    search_fields = ('cpf',)
    #usuarios ordenados por cpf
    ordering = ('cpf',)

# Registre o modelo e o UserAdmin
admin.site.register(User, UserAdmin)


