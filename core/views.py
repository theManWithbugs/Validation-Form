from itertools import count
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import *
from .forms import CidadaoForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from .models import Cidadao, HistoricoSaude
from .utils import *


def login_n(request):
    if request.method == 'POST':
        form = CPFValidationForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']

            user = authenticate(request, username = cpf, password=senha)
            if user is not None:
                login(request, user)
                return redirect('base')

            else: 
                form.add_error('senha', 'Senha incorreta')
        else:
            messages.error(request, '')
    else:
        form = CPFValidationForm()

    return render(request, 'account/login_n.html', {'form': form})


@login_required
def home(request):
    template_name = 'commons/home.html'
    
    total_usuarios = Cidadao.objects.count()  # Contar o total de usuários

    drogas_ms = (HistoricoSaude.objects
                 .values('drogas_uso')  # Agrupar pelos valores de drogas_uso
                 .annotate(quantidade=Count('drogas_uso'))  # Contar a quantidade de cada droga
                 .order_by('-quantidade')  # Ordenar pelo total em ordem decrescente
                 [:3]  # Selecionar os 3 principais
                )

    context = {
        'total_usuarios': total_usuarios,  # Adicione o total de usuários ao contexto
        'drogas_ms': drogas_ms
    }

    return render(request, template_name, context)

#Views de formulario aqui, todas utilizam a mesma logica utilizada
#-------------------------------------------------------------------------------------------------------#         
@login_required
def form1_view(request):
    if request.method == 'POST':
        form = CidadaoForm(request.POST)
        if form.is_valid():
            cidadao = form.save()
            # Armazena o cpf do cidadão na sessão para que possa ser utilizado em uma requisição futura
            request.session['cidadao_cpf'] = cidadao.cpf
            # Marca o formulário como completo
            request.session['form1_complete'] = True
            return redirect('form2')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CidadaoForm()
    
    return render(request, 'commons/include/form.html', {'formulario': form})

@login_required
def form2_view(request):
    cidadao_cpf = request.session.get('cidadao_cpf')
    if not cidadao_cpf:
        messages.error(request, 'Dados do cidadão não encontrados.')
        return redirect('form1')
    
    cidadao = get_object_or_404(Cidadao, cpf=cidadao_cpf)

    if request.method == 'POST':
        form = HistoricoSaudeForm(request.POST)
        if form.is_valid():
            historico_saude = form.save(commit=False)
            historico_saude.cidadao = cidadao
            historico_saude.save()
            # Marca o formulário como completo
            request.session['form2_complete'] = True
            return redirect('form3')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = HistoricoSaudeForm()

    return render(request, 'commons/include/form2.html', {'formulario_saude': form})

@login_required
def form3_view(request):
    cidadao_cpf = request.session.get('cidadao_cpf')
    if not cidadao_cpf:
        messages.error(request, 'Dados do cidadão não encontrados.')
        return redirect('form1')
    
    cidadao = get_object_or_404(Cidadao, cpf=cidadao_cpf)

    if request.method == 'POST':
        form = HistoricoCriminalForm(request.POST)
        if form.is_valid():
            historico_criminal = form.save(commit=False)
            historico_criminal.cidadao = cidadao
            try:
                historico_criminal.save()
                # Marca o formulário como completo
                request.session['form3_complete'] = True
                return redirect('form4')
            except IntegrityError:
                messages.error(request, 'Já existe um registro de histórico criminal para este cidadão.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = HistoricoCriminalForm()

    return render(request, 'commons/include/form3.html', {'formulario_tecnico': form})

@login_required
def form4_view(request):
    cidadao_cpf = request.session.get('cidadao_cpf')
    if not cidadao_cpf:
        messages.error(request, 'Dados do cidadão não encontrados.')
        return redirect('form1')
    
    cidadao = get_object_or_404(Cidadao, cpf=cidadao_cpf)

    # Verifica se todos os formulários anteriores foram preenchidos
    if not (request.session.get('form1_complete') and 
            request.session.get('form2_complete') and 
            request.session.get('form3_complete')):
        messages.error(request, 'Por favor, complete todos os formulários anteriores antes de enviar.')
        return redirect('form1')

    if request.method == 'POST':
        form = InformacoesComplementaresForm(request.POST)
        if form.is_valid():
            informacoes_complementares = form.save(commit=False)
            informacoes_complementares.cidadao = cidadao
            informacoes_complementares.save()
            # Marca o formulário como completo
            request.session['form4_complete'] = True
            return redirect('sucess_page')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = InformacoesComplementaresForm()
        
    return render(request, 'commons/include/form4.html', {'formulario_complementar': form})

def form_acomp_view(request):
    cidadao_cpf = request.session.get('cidadao_cpf')

    if not cidadao_cpf:
        messages.error(request, 'Dados do cidadão não encontrados')
        return redirect('base/not_found')
    
    cidadao = get_object_or_404(Cidadao, cpf=cidadao_cpf)

    if request.method == 'POST':
        form = AcompCentralForm(request.POST)
        if form.is_valid():
            acompcentral = form.save(commit=False)
            acompcentral.cidadao = cidadao
            acompcentral.save()
          
            request.session['form_acomp_complete'] = True
        
            return redirect('sucess_page')
        else:
      
            messages.error(request, 'Por favor, corrija os erros no formulário')
    else:
    
        form = AcompCentralForm()

    return render(request, 'commons/include/form_acom.html', {
        'formulario_acom': form,
        'cidadao_nome': cidadao.nome,
        'data_entrada': cidadao.data_entrada,
    })
       
#-------------------------------------------------------------------------------------------------------#  
#View de busca de dados, usa como principal parametro o cpf pois é o elemento que interliga as tabelas
@login_required
def busca_form_view(request):
    # Instancia o formulário com os dados da requisição GET, se disponíveis, ou um formulário vazio
    form = BuscarCidadaoForm(request.GET or None)
    
    # Inicializa as variáveis que armazenarão as informações do cidadão e seus históricos
    cidadao = None
    historico_saude = None
    historico_criminal = None
    informacoes_complementares = None
    form_acomp = None

    # Verifica se o formulário é válido
    if form.is_valid():
        # Extrai o CPF do formulário
        cpf = form.cleaned_data['cpf']

        try:
            cidadao = Cidadao.objects.get(cpf=cpf)

        except Cidadao.DoesNotExist:
            return redirect('not_found_page')

        else:
            # Recupera o primeiro histórico de saúde associado ao cidadão
            historico_saude = cidadao.historicos_saude.first()  
            # Recupera o primeiro histórico criminal associado ao cidadão
            historico_criminal = cidadao.historicos_criminais.first()  
            # Recupera a primeira informação complementar associada ao cidadão
            informacoes_complementares = cidadao.informacoes_complementares.first()
            #Recupera as informações do formulario de acompanhamento na central
            form_acomp = cidadao.form_acompanhamento_central.first()
    else:
        messages.error(request, '')

    # Prepara o contexto para o template, incluindo o formulário e as informações recuperadas
    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
        'form_acomp_central': form_acomp,
    }
    
    # Renderiza o template 'busca_form.html' com o contexto preparado
    return render(request, 'commons/include/busca_form.html', context)

#-------------------------------------------------------------------------------------------------------#
@login_required
def excluir_form(request):
    form = BuscarCidadaoForm(request.POST or None)
    cidadao = None
    
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            try:
                cidadao = Cidadao.objects.get(cpf=cpf)
                cidadao.delete()
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

    return render(request, 'commons/include/busca_form.html', context)

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
def analise_view(request):
    aumento_percentual =  calcular_porcent()
    template_name = 'commons/include/estatisticas.html'

    porcentagem_masculino, porcentagem_feminino = calcular_sexo()

    total_usuarios = Cidadao.objects.count()

    drogas_ms = (HistoricoSaude.objects
                 .values('drogas_uso')
                 .annotate(quantidade=Count('drogas_uso'))
                [:3]
                )
    
    context = {
        'porcentagem_homens': porcentagem_masculino,
        'porcentagem_mulheres': porcentagem_feminino,
        'aumento_percentual': aumento_percentual,
        'total_usuarios': total_usuarios,
        'drogas_ms': drogas_ms
    }

    return render(request, template_name, context)

@login_required
def base_view(request):
    return render(request, 'base.html')

@login_required
def sucess_page_view(request):
    template_name = 'commons/include/sucess_page.html'
    return render(request, template_name)

@login_required
def usuario_view(request):
    return render(request, 'account/perfil.html')

def edit_form_view(request):
    return render(request, 'commons/include/editar_form.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login_new')

def footer_view(request):
    template_name = 'commons/include/footer.html'
    return render(request, template_name)

def notfound_view(request):
    template_name='commons/include/not_found.html'
    return render(request, template_name)


#-------------------------------------------------------------------------------------------------------#
def buscar_acmform_view (request):
    form = BuscarCidadaoForm(request.GET or None)

    form_acomp = None
    cidadao = None
    historico_criminal = None

    if form.is_valid():
        cpf = form.cleaned_data['cpf']

        try:
            cidadao = Cidadao.objects.get(cpf=cpf)
        
        except Cidadao.DoesNotExist:
            return redirect('not_found_page')
        
        else:
            historico_criminal = cidadao.historicos_criminais.first()
            form_acomp = cidadao.form_acompanhamento_central.all()

    else:
        messages.error(request, '')

    context = {
        'formulario': form, 
        'form_acomp_central': form_acomp,
        'cidadao': cidadao,
        'historico_criminal': historico_criminal,
    }

    return render(request, 'commons/include/acomp_busca.html', context)

#Ambas essa views se interligam uma capturando e outra exibindo o formulario para inserção
#-------------------------------------------------------------------------------------------------------#    

#Capturar os dados aqui
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

#Receber e realizar o processamento 
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

    return render(request, 'commons/include/acomp_regtwo.html', {'acomp_central': form})

#-------------------------------------------------------------------------------------------------------#

def exibir_time(request):
    cidadao = None
    time_list = None

    if request.method == 'POST':
        cpf = request.POST.get('cpf')  

        try:
            cidadao = Cidadao.objects.get(cpf=cpf)
            time_list = cidadao.time.first()

        except Cidadao.DoesNotExist:
            return redirect('not_found_page')
    else:
        messages.error(request, '')
    
    context = {
        'cidadao': cidadao,
        'time_list': time_list,
        }
    
    return render(request, 'commons/include/exibir_time.html', context)


#view não está sendo utilizada no momento
#-------------------------------------------------------------------------------------------------------#
#
#def atualizar_tempo(request):
   #if request.method == 'POST':
    #   cpf = request.POST.get('cpf')
    #   subtrair_horas = request.POST.get('subtrair_horas')

    #   if not subtrair_horas:
    #       return HttpResponseBadRequest('Erro: dado não fornecido!')

    #   try:
    #       subtrair_horas = int(subtrair_horas)
    #   except ValueError:
    #       return HttpResponseBadRequest('Deve ser inserido um número válido')

    #   arm_time = get_object_or_404(ArmTime, cidadao__cpf=cpf)
    #   arm_time.time -= subtrair_horas  
    #   arm_time.save()

    #   return redirect('sucess_page')

    #context = {
    #    'tempo_atual': 'Informação de tempo não disponível.',
    #}

    #return render(request, 'commons/include/exibir_time.html', context)

        
        
    









    

        































            
           

