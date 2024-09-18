from django.conf.urls.static import static
from django.urls import path
from core import views
from django.conf import settings

urlpatterns = [
    path('', views.login_n, name='login_new'),
    path('base/', views.home, name='base'),
    path('base/formulario1/', views.form1_view, name='form1'),
    path('base/formulario2/', views.form2_view, name='form2'),
    path('base/formulario3/', views.form3_view, name='form3'),
    path('base/formulario4/', views.form4_view, name='form4'),
    path('base/busca/', views.busca_cpf_view, name='busca'),
    path('base/edit_form/', views.edit_form_view, name='edit_view'),
    path('footer/', views.footer_view, name='footer'),
    path('logout/', views.logout_view, name='logout'),
    path('base/perfil/', views.usuario_view, name='perfil'),
    path('base/excluir/', views.excluir_form, name='excluir_form'),
    path('base/editar_dados',views.capturar_cpf, name='capturar_dados'),
    path('atualizar_dados/<str:cpf>/', views.atualizar_dados, name='atualizar_dados'),
    path('base/not_found', views.notfound_view, name='not_found_page'),
    path('base/missing_data/', views.missing_data_view, name='missing_data'),
    path('base/sucess_page/', views.sucess_page_view, name='sucess_page'),
    path('base/estatisticas/', views.analise_view, name='estatisticas'),
    path('base/form4/form_acomp/', views.form_acomp_view, name='form_acomp'),
    path('base/buscar_acmform', views.buscar_acmform_view, name='acmform'),
    path('base/acmform/', views.register_acmform_view, name='register_acmform_view'),
    path('acomp-central-form/', views.acomp_central_form, name='acomp_central_form'),
    path('base/exibir_time/', views.exibir_time, name='exibir_time'),
    path('base/exibir_time/add_time/', views.add_time_view, name='add_time'),
    path('base/buscar_nome/', views.buscar_nome_view, name='buscar_nome'),
    ]


