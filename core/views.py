import io
from datetime import date, datetime
import os
import tempfile
from django.conf import settings
from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from .forms import CidadaoForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from .models import *
from .utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.forms import modelformset_factory
from .models import ActivityLog, User
from django.http import FileResponse
from django.views.generic import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pypandoc
from django.template.loader import render_to_string


def is_staff(user):
    return user.is_staff

def login_n(request):
    if request.method == 'POST':
        form = CPFValidationForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']

            user = authenticate(request, username = cpf, password = senha)
            if user is not None:
                login(request, user)
                return redirect('base')
            else: 
                form.add_error('cpf', 'Não consta no banco')
        else:
            messages.error(request, 'Dados invalidos!')
    else:
        form = CPFValidationForm()

    return render(request, 'account/login_n.html', {'form': form})

@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def register_user(request):
    template_name = 'account/register.html'

    nome = None
    cpf= None
    password = None
    confirmar_password = None

    if request.method == 'POST':
       nome = request.POST.get('nome')
       cpf = request.POST.get('cpf')
       password = request.POST.get('password')
       confirmar_password = request.POST.get('confirmar_password')
  
    if password != confirmar_password:
        messages.error(request, 'As senhas devem ser iguais!')
        return redirect('register')

    #verifica se não está vazio antes de tentar criar o objeto
    if not nome or not cpf or not password:
        return render(request, template_name)

    try:
        user = User.objects.create_user(
            cpf=cpf,
            password=password,
            nome=nome,
        )
        messages.success(request, 'Cadastro realizado com sucesso!')
    except DatabaseError:
        messages.error(request, 'Não foi possível cadastrar!')
           
    return render(request, template_name)

def remover_acesso(request):
    template_name = 'account/remov_acess.html'

    usuario = None
    confirmar = None

    cpf = request.POST.get('cpf')
    confirmar = request.POST.get('cpf')

    try:
        usuario = User.objects.get(cpf=cpf)
        print(usuario.nome)
        if confirmar == True:
            usuario.delete()
    except User.DoesNotExist:
        print(f"O usuario: {cpf} não existe!")

    context = { 
        'usuario': usuario,
    }

    return render(request, template_name, context)
        
def atualizar_perfil_img(request):
    if request.user.is_authenticated:
        user = request.user  # Now it's guaranteed to be a User instance
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('perfil')
        else:
            form = UserForm(instance=user)
        
        return render(request, 'account/perfil.html', {'form': form})
    else:
        return redirect('login_new')  # Redirect to login if not authenticated

#essa view é usada para verificar se o usuario logado possui is_staff igual a true
#tal referência pode ser usado ao chamar o decorador @user_passes_test(is_staff, login_url='login_new')
#para esse caso foi usado o atributo is staff, e caso o ususario não seja é redirecionado para a pagina 

@login_required
def home(request):
    template_name = 'commons/home.html'
    aumento_percentual = calcular_porcent()

    total_usuarios = Cidadao.objects.count()  
    total_usuarios_site = User.objects.count()
    ativos = contar_ativos()

    context = {
        'total_usuarios': total_usuarios,  
        'aumento_percentual': aumento_percentual,
        'total_usuarios_site': total_usuarios_site,
        'ativos': ativos,
    }

    return render(request, template_name, context)

@login_required
def actions_view(request): 
    alteracoes = ActivityLog.objects.all().order_by('-timestamp')[:20]
    return render(request, 'commons/include/actions.html', {'alteracoes': alteracoes})

#Views de formulario aqui, todas utilizam a mesma logica utilizada
#-------------------------------------------------------------------------------------------------------#         
@login_required
def form1_view(request):
    if request.method == 'POST':
        form = CidadaoForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            
            # Converter datas para string
            for field in form_data:
                if isinstance(form_data[field], (date, datetime)):
                    form_data[field] = form_data[field].isoformat()  # Usa o formato ISO para datas e datetimes

            # Salvar dados no session
            request.session['cidadao_form_data'] = form_data
            request.session['form1_complete'] = True
            return redirect('form2')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CidadaoForm()
    
    return render(request, 'commons/include/forms/form.html', {'formulario': form})

@login_required
def form2_view(request):
    if not request.session.get('form1_complete'):
        messages.error(request, 'Formulario 1 não preenchido')
        return redirect('form1')

    if request.method == 'POST':
        form = HistoricoSaudeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            
            # Converter datas para string
            for field in form_data:
                if isinstance(form_data[field], (date, datetime)):
                    form_data[field] = form_data[field].isoformat()

            request.session['historico_saude_form_data'] = form_data
            request.session['form2_complete'] = True
            return redirect('form3')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = HistoricoSaudeForm()

    return render(request, 'commons/include/forms/form2.html', {'formulario_saude': form})

@login_required
def form3_view(request):
    if not request.session.get('form2_complete'):
        messages.error(request, 'Formulario 2 não preenchido')
        return redirect('form2')

    if request.method == 'POST':
        form = HistoricoCriminalForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            
            # Converter datas para string
            for field in form_data:
                if isinstance(form_data[field], (date, datetime)):
                    form_data[field] = form_data[field].isoformat()

            request.session['historico_criminal_form_data'] = form_data
            request.session['form3_complete'] = True
            return redirect('form4')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = HistoricoCriminalForm()

    return render(request, 'commons/include/forms/form3.html', {'formulario_tecnico': form})


@login_required
def form4_view(request):
    if not (request.session.get('form1_complete') and
            request.session.get('form2_complete') and
            request.session.get('form3_complete')):
        messages.error(request, 'É necessário que todos os formulários sejam preenchidos!')
        return redirect('form1')
    
    if request.method == 'POST':
        form = InformacoesComplementaresForm(request.POST)
        if form.is_valid():
            cidadao_data = request.session.get('cidadao_form_data')
            historico_saude_data = request.session.get('historico_saude_form_data')
            historico_criminal_data = request.session.get('historico_criminal_form_data')

            if not all([cidadao_data, historico_saude_data, historico_criminal_data]):
                messages.error(request, 'Restam dados anteriores não preenchidos!')
                return redirect('missing_data')
            
            # Cria os objetos para serem salvos no banco de dados
            cidadao = Cidadao.objects.create(**cidadao_data)

            HistoricoSaude.objects.create(cidadao=cidadao, **historico_saude_data)

            HistoricoCriminal.objects.create(cidadao=cidadao, **historico_criminal_data)

            # Cria e salva o último objeto que diz respeito ao formulário 4
            informacoes_complementares = form.save(commit=False) 
            informacoes_complementares.cidadao = cidadao
            informacoes_complementares.save()

            # Limpa os dados da sessão
            request.session.pop('cidadao_form_data', None)
            request.session.pop('historico_saude_form_data', None)
            request.session.pop('historico_criminal_form_data', None)
            request.session['form4_complete'] = True
            return redirect('sucess_page')
        else:
            messages.error(request, 'Formulario inválido!')
    else:
        form = InformacoesComplementaresForm()

    return render(request, 'commons/include/forms/form4.html', {'formulario_complementar': form,})

@login_required
def capturar_dados_viole(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            return redirect('form_violen', cpf)
        else:
            messages.error(request, 'O campo CPF não deve estar vazio!')

    return render(request, 'commons/include/cap_viol.html')

@login_required
def form_violencia_domest(request, cpf):
    try:
        cidadao = Cidadao.objects.get(cpf=cpf)
    except Cidadao.DoesNotExist:
        return redirect('not_found_page')

    if request.method == 'POST':
        form = ViolenDomestForm(request.POST)
        if form.is_valid():
            form_violen = form.save(commit=False)
            form_violen.cidadao = cidadao
            form_violen.save()
            return redirect('sucess_page')
        else:
            messages.error(request, 'Formulário inválido!')
    else:
        form = ViolenDomestForm(initial={'cpf': cidadao.cpf})

    context = {
        'form': form,
        'cidadao': cidadao,
    }

    return render(request, 'commons/include/forms/form_violen.html', context)
       
#-------------------------------------------------------------------------------------------------------#  
@login_required
def busca_cpf_view(request):
    form = BuscarCidadaoForm(request.GET or None)

    cidadao = None
    historico_saude = None
    historico_criminal = None
    informacoes_complementares = None
    form_violen = None

    if form.is_valid():
        cpf = form.cleaned_data.get('cpf')
        cidadao_queryset = Cidadao.objects.filter(cpf=cpf)
        request.session['cpf'] = cpf

        if cidadao_queryset.exists():
            cidadao = cidadao_queryset.first()
            historico_saude = cidadao.historicos_saude.first()
            historico_criminal = cidadao.historicos_criminais.first()
            informacoes_complementares = cidadao.informacoes_complementares.first()
            form_violen = cidadao.form_violencia_domes.all()

        else:
            return redirect('not_found_page')

    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
        'form_violen': form_violen,
    }

    return render(request, 'commons/include/busca_cpf.html', context)

@login_required
def buscar_nome_view(request):
    form = BuscarNomeForm(request.GET or None)

    cidadao = None
    historico_saude = None
    historico_criminal= None
    informacoes_complementares = None

    #inicia a lista como vazia para evitar erros
    objs = []

    #recebe a variavel nome do input
    #caso a variavel nome não tenha nenhum valor associado,
    # será definida como uma string vazia para evitar erros
    nome = request.GET.get('nome', '')

    if form.is_valid():
        #limpa os dados 
        nome = form.cleaned_data['nome']

        #verifica se nome não está vazio
        if nome:
            cidadao__queryset = Cidadao.objects.filter(nome__icontains=nome)
            paginator = Paginator(cidadao__queryset, 10)
            page = request.GET.get('page')

            try:
                objs = paginator.page(page)
            except PageNotAnInteger:
                objs = paginator.page(1)
            except EmptyPage:
                objs = paginator.page(paginator.num_pages)

            if objs.object_list.exists():
                cidadao = objs.object_list.all()
            else:
                messages.error(request, 'Não consta nenhum dado com esse caracter!')

    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
        'objs': objs,
        'search': nome,
    }

    return render(request, 'commons/include/buscar_nome.html', context)

def more_info_view(request, cpf):

    cidadao = get_object_or_404(Cidadao, cpf=cpf)

    try:
        historico_saude = cidadao.historicos_saude.first()
        historico_criminal = cidadao.historicos_criminais.first()
        informacoes_complementares = cidadao.informacoes_complementares.first()
        form_acomp = cidadao.form_acompanhamento_central.first()
        form_violen = cidadao.form_violencia_domes.all()
    except DatabaseError:
        messages.error(request, 'Não foi possível localizar os dados no banco!')

    context = {
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
        'form_acomp_central': form_acomp,
        'form_violen': form_violen,
    }

    return render(request, 'commons/include/more_info.html', context)
    
#-------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def excluir_form(request):
    form = BuscarCidadaoForm(request.POST or None)
    cidadao = None
    
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            try:
                cidadao = Cidadao.objects.get(cpf=cpf)
                
                cidadao.delete()
                ActivityLog.objects.create(
                    user=request.user,
                    cpf_excluido=cpf,
                )
                messages.success(request, 'Cidadão excluído com sucesso.')
                return redirect('busca')  
            except Cidadao.DoesNotExist:
                messages.error(request, 'Cidadão não encontrado.')
        else:
            messages.error(request, 'CPF não fornecido.')
    
    if form.is_valid():
        cpf = form.cleaned_data.get('cpf', None)
        if cpf:
            try:
                cidadao = Cidadao.objects.get(cpf=cpf)
            except Cidadao.DoesNotExist:
                messages.error(request, 'Cidadão não encontrado')
        else:
            messages.error(request, 'CPF inválido.')

    context = {
        'form': form,
        'cidadao': cidadao,
    }

    return request, context

@login_required
def capturar_cpf(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            return redirect('atualizar_dados', cpf=cpf)
        else:
            messages.error(request, 'CPF não fornecido')
    return render(request, 'commons/include/capturar_cpf.html')

#view para atualizar dados do formulario
@login_required
def atualizar_dados(request, cpf):
    try:
        cidadao = Cidadao.objects.get(cpf=cpf)
    except Cidadao.DoesNotExist:
        return redirect('not_found_page')

    #é realizado a criação de variaveis e em seguida é atribuido valores a cada instância de modelo
    if request.method == 'POST':
        form_cidadao = AlterarDadosForm(request.POST, instance=cidadao)
        form_historico_saude = HistoricoSaudeForm(request.POST, instance=HistoricoSaude.objects.filter(cidadao=cidadao).first())
        form_historico_criminal = HistoricoCriminalForm(request.POST, instance=HistoricoCriminal.objects.filter(cidadao=cidadao).first())
        form_informacoes_complementares = InformacoesComplementaresForm(request.POST, instance=InformacoesComplementares.objects.filter(cidadao=cidadao).first())


        if (form_cidadao.is_valid() and
            form_historico_saude.is_valid() and
            form_historico_criminal.is_valid() and
            form_informacoes_complementares.is_valid()):

            form_cidadao.save()
            form_historico_saude.save()
            form_historico_criminal.save()
            form_informacoes_complementares.save()
            
            return redirect('sucess_page')
        else:
            messages.error(request, 'Há erros no formulário. Por favor, corrija-os.')

    else:
        form_cidadao = AlterarDadosForm(instance=cidadao)
        form_historico_saude = HistoricoSaudeForm(instance=HistoricoSaude.objects.filter(cidadao=cidadao).first() or HistoricoSaude(cidadao=cidadao))
        form_historico_criminal = HistoricoCriminalForm(instance=HistoricoCriminal.objects.filter(cidadao=cidadao).first() or HistoricoCriminal(cidadao=cidadao))
        form_informacoes_complementares = InformacoesComplementaresForm(instance=InformacoesComplementares.objects.filter(cidadao=cidadao).first() or InformacoesComplementares(cidadao=cidadao))

    return render(request, 'commons/include/editar_form.html', {
        'form_cidadao': form_cidadao,
        'form_historico_saude': form_historico_saude,
        'form_historico_criminal': form_historico_criminal,
        'form_informacoes_complementares': form_informacoes_complementares,
        'cidadao': cidadao
    })

# Aqui nesta pagina ficam as estatisticas para análise de dados
@login_required
def analise_view(request):
    aumento_percentual =  calcular_porcent()
    template_name = 'commons/include/estatisticas.html'
    resultado_tipo_penal = tipo_penal()
    resultado = tipo_penal_quant()
    resultado_medida = medida_cumprimento_calc()
    resultado_cumprimento_saida = medida_cumprimento_saida()
    ativos = contar_ativos()
    faixas_etarias = contar_faixa_etaria()
    faixas_etarias_porcentagem = contar_faixa_etaria_porcentagem_sta()

    tip_penal_ativos =  tipo_penal_ativos()
    medida_cump_ativos = medida_cumprimento_calc_ativos()
    resultado_masculino_at, resultado_feminino_at = calcular_sexo_ativos()
    resultado_faixas_etarias_ativos = contar_faixa_etaria_porcentagem_ativos()


    resultado_masculino, resultado_feminino = calcular_sexo()

    total_usuarios = Cidadao.objects.count()

    total_usuarios_site = User.objects.count()


    drogas_ms = (HistoricoSaude.objects
                 .values('drogas_uso')
                 .annotate(quantidade=Count('drogas_uso'))
                [:5]
                )
    
    context = {
        'porcentagem_homens': resultado_masculino,
        'porcentagem_mulheres': resultado_feminino,
        'aumento_percentual': aumento_percentual,
        'total_usuarios': total_usuarios,
        'drogas_ms': drogas_ms,
        'resultado_tipo_penal': resultado_tipo_penal,
        'resultado_tip_quant': resultado,
        'resultado_medida': resultado_medida,
        'total_usuarios_site': total_usuarios_site,
        'resultado_cumprimento_saida': resultado_cumprimento_saida,
        'ativos': ativos,
        'faixas_etarias': faixas_etarias,
        'faixas_etarias_porcentagem': faixas_etarias_porcentagem,

        'tip_penal_ativos': tip_penal_ativos,
        'medida_cump_ativos': medida_cump_ativos,
        'resultado_masculino_at': resultado_masculino_at,
        'resultado_feminino_at': resultado_feminino_at,
        'resultado_faixas_etarias_ativos': resultado_faixas_etarias_ativos,
    }

    return render(request, template_name, context)

class HistoricoCriminalList(APIView):
    def get(self, request):
        # Obtendo os históricos
        historicos = HistoricoCriminal.objects.all()
        serializer = HistoricoCriminalSerializer(historicos, many=True)

        # Chamando a função para calcular porcentagens dos tipos penais
        tipos_penais_porcentagens = tipo_penal()

        # Chamando a função para calcular medidas de cumprimento
        medidas_cumprimento = medida_cumprimento_calc()

        # Retornando os dados em um formato que inclua as porcentagens e medidas
        return Response({
            'historicos': serializer.data,
            'tipos_penais_porcentagens': tipos_penais_porcentagens,
            'medidas_cumprimento': medidas_cumprimento
        })
class FaixasEtarias(APIView):
    def get(self, request):
        # Obtendo as idades dos cidadãos
        idades = Cidadao.objects.all()
        serializer = CidadaoSerializer(idades, many=True)

        # Chamando a função para calcular as faixas etárias
        faixas_etarias = contar_faixa_etaria_porcentagem_ativos()

        # Retornando os dados em um formato que inclua as idades e faixas etárias
        return Response({
            'idades': serializer.data,
            'faixas_etarias': faixas_etarias,
        })

#-------------------------------------------------------------------------------------------------------#
@login_required
def buscar_acmform_view (request):
    form = BuscarCidadaoForm(request.GET or None)

    form_acomp = None
    cidadao = None
    historico_criminal = None
    violen_domest = None

    if form.is_valid():
        cpf = form.cleaned_data['cpf']
        request.session['cpf'] = cpf

        try:
            cidadao = Cidadao.objects.get(cpf=cpf)
        
        except Cidadao.DoesNotExist:
            return redirect('not_found_page')
        
        else:
            historico_criminal = cidadao.historicos_criminais.first()
            form_acomp = cidadao.form_acompanhamento_central.all()
            violen_domest = cidadao.form_violencia_domes.all()


    context = {
        'formulario': form, 
        'form_acomp_central': form_acomp,
        'cidadao': cidadao,
        'historico_criminal': historico_criminal,
        'violen_domest':  violen_domest,
    }

    return render(request, 'commons/include/acomp_busca.html', context)

@login_required
def pdf_view(request):
    template_name = 'commons/include/acmp_pdf.html'
    cpf = request.session.get('cpf')

    historico_criminal = None
    form_acomp = None
    violen_domest = None

    if cpf:
        try:
            cidadao = Cidadao.objects.get(cpf=cpf)

            historico_criminal = cidadao.historicos_criminais.first()
            form_acomp = cidadao.form_acompanhamento_central.all()
            violen_domest = cidadao.form_violencia_domes.all()
        except Cidadao.DoesNotExist:
            return redirect('not_found_page')

    context = {
            'cidadao': cidadao,
            'historico_criminal': historico_criminal,
            'form_acomp': form_acomp,
            'violen_domest': violen_domest,
            }
    return render_to_pdf(template_name, context)

#Ambas essa views se interligam uma capturando e outra exibindo o formulario para inserção
#-------------------------------------------------------------------------------------------------------#    

@login_required
def register_acmform_view(request):
    if request.method == 'POST':
        form = BuscarCidadaoForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            request.session['cpf'] = cpf
            return redirect('acomp_central_form')
        else:
            return redirect('not_found_page')
    
    else:
        form = BuscarCidadaoForm()
    
    return render(request, 'commons/include/acomp_reg.html', {'form': form})

@login_required
def acomp_central_form(request):
    cpf = request.session.get('cpf')

    try:
        cidadao = Cidadao.objects.get(cpf=cpf)
    except Cidadao.DoesNotExist:
        return redirect('not_found_page')

    if request.method == 'POST': 
        form = AcompCentralForm(request.POST)
        if form.is_valid():
            acomp_central = form.save(commit=False)
            acomp_central.cidadao = cidadao
            acomp_central.save()
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('sucess_page')
    else:
        form = AcompCentralForm()

    return render(request, 'commons/include/acomp_regtwo.html', {'acomp_central': form, 'cidadao': cidadao,})

#-------------------------------------------------------------------------------------------------------#

@login_required
def violen_info(request, process_referente):

    model = get_object_or_404(ViolenDomest, process_referente=process_referente)
    
    #Acessa o modelo cidadao e sua related name form_violencia_domes
    cidadao = model.cidadao
    processos = cidadao.form_violencia_domes.first()  

    context = {
        'cidadao': cidadao,
        'processo': model,  
        'processos': processos, 
    }

    return render(request, 'commons/include/process_more.html', context)

@user_passes_test(is_staff, login_url='permission_denied')
def capturar_cpf_process(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            return redirect('editar_process', cpf=cpf)
        else:
            messages.error(request, 'O campo CPF não deve estar vazio!')
    return render(request, 'commons/include/capturar_process.html')

#formset cria uma coleção de formulario baseados em um modelo, que nesse caso é ViolenDomestica
#ou seja ele exibe todos os formularios de ViolenDomestica na tela, isso é semelhante a um loop for
#como extra foi definido como 0, não serão exibidos formularios em branco para preenchimento,
#apenas formularios já existentes são exibidos na tela.
ViolenDomestFormSet = modelformset_factory(ViolenDomest, form=ViolenDomestFormTwo, extra=0)

@login_required
@user_passes_test(is_staff, login_url='permission_denied')
def editar_process(request, cpf):
    try:
        cidadao = Cidadao.objects.get(cpf=cpf)
    except Cidadao.DoesNotExist:
        return redirect('not_found_page')
    
    if request. method == 'POST':
        formset = ViolenDomestFormSet(request.POST, queryset=ViolenDomest.objects.filter(cidadao=cidadao))

        if formset.is_valid():
            formset.save()
            return redirect('sucess_page')
        else:
            messages.error(request ,'Formulario invalido!')

    else:
        formset = ViolenDomestFormSet(queryset=ViolenDomest.objects.filter(cidadao=cidadao))

    context = {
        'violen_domest_formset': formset,
        'cidadao': cidadao,
    }

    return render(request, 'commons/include/exibir_edicaoprocss.html', context)

@login_required
def custom_404_view(request, exception):
    return render(request, 'templates/errors/404.html', status=404)

@login_required
def edit_form_view(request):
    return render(request, 'commons/include/editar_form.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login_new')

@login_required
def sucess_page_view(request):
    template_name = 'commons/include/add_pages/sucess_page.html'
    return render(request, template_name)

@login_required
def notfound_view(request):
    template_name='commons/include/add_pages/not_found.html'
    return render(request, template_name)

@login_required
def missing_data_view(request):
    return render(request, 'commons/include/add_pages/missing_data.html')

@login_required
def permission_denied_view(request):
    return render(request, 'commons/include/add_pages/permiss.html')

class IndexView(View):
    def get(self, request, *args, **kwargs):
        cpf = request.session.get('cpf')
        
        buffer = io.BytesIO()

        #esse comando cria um canvas pdf, não sei o que é isso, deve ser o arquivo pdf
        pdf = canvas.Canvas(buffer, pagesize=letter)

        cidadao = Cidadao.objects.get(cpf=cpf)
        historico_saude = HistoricoSaude.objects.filter(cidadao=cidadao)
        historico_criminal = HistoricoCriminal.objects.filter(cidadao=cidadao)
        informacoes_complementares = InformacoesComplementares.objects.filter(cidadao=cidadao)

        image_path = 'static/img/ciap_img.png'
        pdf.drawImage(image_path, 210, 660, width=170, height=110)

        pdf.drawString(100, 630, f"Cidadão: {cidadao.nome}")
        pdf.drawString(100, 612, f"CPF: {cidadao.cpf}")

        y_position = 580
        line_height = 20

        pdf.drawString(100, y_position, "-HISTORICO DE SAÚDE-")
        y_position -= line_height
        for item in historico_saude:
            pdf.drawString(100, y_position, f"Apresenta problemas de saude?: {item.saude}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Faz ou fez tratamento psiquiatrico?: {item.tratamento_psi}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Especifique o tratamento psiquiatrico: {item.tratamento_psi_jus}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Faz uso de alguma medicação controlada?: {item.medicacao_controlada}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Especifique o tipo de medicação controlada: {item.medicacao_controlada_jus}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"É portador de alguma deficiência: {item.deficiencia}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Faz ou já fez uso de: {item.drogas_uso}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Já procurou tratamento?: {item.tratamento}")
            y_position -= line_height
            if y_position < 40:  
                pdf.showPage()  
                pdf.setFont("Helvetica", 12)
                y_position = 800  

            y_position -= line_height

        pdf.drawString(100, y_position, "-HISTORICO CRIMINAL-")
        y_position -= line_height
        for item in historico_criminal:
            pdf.drawString(100, y_position, f"Já esteve preso?: {item.ja_esteve_preso}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Por qual motivo esteve preso?: {item.prisao_justificativa}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Alguém da sua familia já esteve preso?: {item.prisao_familiar}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Número do processo: {item.numero_do_processo}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Juiz de origem: {item.juiz_de_origem}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Medida aplicada: {item.medida_aplicada}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Tipo penal: {item.tipo_penal}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Em caso de violência domestica: {item.violencia_domestica}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Nome da vitima de violência domestica: {item.violencia_dome_nome_vitima}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Grau de parentesco da vitima: {item.grau_de_parentesco}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Relata reincidência?: {item.reincidencia}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Sugestão de trabalho: {item.sugestao_de_trabalho}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Sugestão de encaminhamento: {item.sugest_encaminhamento}")
            y_position -= line_height
            if y_position < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = 800

            y_position -= line_height

        pdf.showPage()
        pdf.setFont("Helvetica", 12)
        y_position = 730
        pdf.drawString(100, y_position, "-INFORMAÇÕES COMPLEMENTARES-")
        y_position -= line_height
        for item in informacoes_complementares:
            pdf.drawString(100, y_position, f"Quantas pessoas moram com você ? (inclua você na contagem): {item.quantas_pessoas}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Nome de um familiar: {item.nome_familiar}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Grau de parentesco: {item.parentesco}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Idade do familiar: {item.idade_familiar}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Grau de Escolaridade do familiar: {item.escolaridade_familiar}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Análise descritiva: {item.analise_descritiva}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Tipificação penal: {item.tip_penal}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Medida de cumprimento: {item.medida_cumprimento}")
            y_position -= line_height
            pdf.drawString(100, y_position, f"Motivo de saida: {item.motivo_saida}")
            y_position -= line_height
            if y_position < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = 800
                
        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename='Ficha.pdf')

def generate_docx(request):
    template_name = 'commons/include/acmp_ficha_edit.html'
    cpf = request.session.get('cpf')

    historico_criminal = None
    form_acomp = None
    violen_domest = None

    if cpf:
        try:
            cidadao = Cidadao.objects.get(cpf=cpf)

            historico_criminal = cidadao.historicos_criminais.first()
            form_acomp = cidadao.form_acompanhamento_central.all()
            violen_domest = cidadao.form_violencia_domes.all()
        except Cidadao.DoesNotExist:
            return redirect('not_found_page')

    context = {
            'cidadao': cidadao,
            'historico_criminal': historico_criminal,
            'form_acomp': form_acomp,
            'violen_domest': violen_domest,
            }
    
    # aqui é passado o nome do template e o contexto
    html_content = render_to_string(template_name, context)
        
    # cria um arquivo temporario
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_docx:
        # Converter HTML para DOCX e salvar no arquivo temporário
        pypandoc.convert_text(html_content, 'docx', format='html', outputfile=temp_docx.name)

        # Abrir o arquivo para leitura
        temp_docx.seek(0)
        response = HttpResponse(temp_docx.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="output.docx"'

    # Após baixar exclui o arquivo temporario
    os.unlink(temp_docx.name)
    
    return response























    







        
        
    









    

        































            
           

