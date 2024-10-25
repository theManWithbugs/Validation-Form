from django.urls import path
from core import views
from django.conf import settings
from core.views import FaixasEtarias, IndexView, custom_404_view, generate_docx

handler404 = custom_404_view

urlpatterns = [
    #login, register and logout
    path('', views.login_n, name='login_new'),
    path('register/', views.register_user, name='register'),
    path('remov_user', views.remover_acesso, name='rem_user'),
    path('logout/', views.logout_view, name='logout'),

    #base page
    path('base/', views.home, name='base'),
    path('faixas-etarias/', FaixasEtarias.as_view(), name='faixas_etarias'),
    path('base/', views.actions_view, name='action'),

    #forms register
    path('base/formulario1/', views.form1_view, name='form1'),
    path('base/formulario2/', views.form2_view, name='form2'),
    path('base/formulario3/', views.form3_view, name='form3'),
    path('base/formulario4/', views.form4_view, name='form4'),
    path('base/acmform/', views.register_acmform_view, name='register_acmform_view'),
    path('base/capturar_dados_viole/', views.capturar_dados_viole, name='capturar_violen'),
    path('base/formulario4/form_violen_domes/<str:cpf>/', views.form_violencia_domest, name='form_violen'),
    path('acomp-central-form/', views.acomp_central_form, name='acomp_central_form'),

    #search
    path('base/busca/', views.busca_cpf_view, name='busca'),
    path('base/buscar_acmform/', views.buscar_acmform_view, name='acmform'),
    path('base/buscar_nome/', views.buscar_nome_view, name='buscar_nome'),

    #messages page
    path('base/not_found', views.notfound_view, name='not_found_page'),
    path('base/missing_data/', views.missing_data_view, name='missing_data'),
    path('base/sucess_page/', views.sucess_page_view, name='sucess_page'),
    path('base/permission_denied/', views.permission_denied_view, name='permission_denied'),

    #the other views
    path('base/edit_form/', views.edit_form_view, name='edit_view'),
    path('base/excluir/', views.excluir_form, name='excluir_form'),
    path('base/excluir/', views.excluir_process, name='excluir_process'),
    path('base/editar_dados',views.capturar_cpf, name='capturar_dados'),
    path('atualizar_dados/<str:cpf>/', views.atualizar_dados, name='atualizar_dados'),
    path('base/estatisticas/', views.analise_view, name='estatisticas'),
    path('base/buscar_nome/more_info/<str:cpf>/', views.more_info_view, name='more_info'),
    path('base/busca/process_info/<str:process_referente>/', views.violen_info, name='violen_info'),
    path('base/alterar_process/', views.capturar_cpf_process, name='alterar_process'),
    path('base/alterar_process/editar_process/<str:cpf>/', views.editar_process, name='editar_process'),
    path('base/actions/', views.actions_view, name='actions'),
    path('base/perfil/', views.atualizar_perfil_img, name='perfil'),

    #pdf views
    path('base/pdf_test/', IndexView.as_view(), name='imprimir_pdf'), 
    path('acmp_pdf/', views.pdf_view, name='acmp_pdf'),

    #word_view
    path('generate-docx/', generate_docx, name='generate_docx'),
    ]



