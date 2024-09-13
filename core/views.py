from datetime import date, datetime
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
            # Obter os dados do formulário
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

    return render(request, 'commons/include/forms/form4.html', {'formulario_complementar': form})

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
@login_required
def busca_form_view(request):
    form = BuscarCidadaoForm(request.GET or None)

    cidadao = None
    historico_saude = None
    historico_criminal = None
    informacoes_complementares = None
    form_acomp = None

    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        cpf = form.cleaned_data.get('cpf')

        if nome:
            cidadao_queryset = Cidadao.objects.filter(nome__icontains=nome)
        elif cpf:
            cidadao_queryset = Cidadao.objects.filter(cpf=cpf)
        else:
            cidadao_queryset = Cidadao.objects.none()

        if cidadao_queryset.exists():
            cidadao = cidadao_queryset.first()

            historico_saude = cidadao.historicos_saude.first()
            historico_criminal = cidadao.historicos_criminais.first()
            informacoes_complementares = cidadao.informacoes_complementares.first()
            form_acomp = cidadao.form_acompanhamento_central.first()
        else:
            return redirect('not_found_page')
    else:
        messages.error(request, 'Erro na validação do formulário.')
        print(form.errors)

    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
        'form_acomp_central': form_acomp,
    }

    return render(request, 'commons/include/busca_form.html', context)


def buscar_nome_view(request):
    form = BuscarNomeForm(request.GET or None)

    cidadao = None
    historico_saude = None
    historico_criminal= None
    informacoes_complementares = None

    if form.is_valid():
        nome = request.POST.get('nome')
        nome = form.cleaned_data['nome']

        if nome:
            cidadao__queryset = Cidadao.objects.filter(nome__icontains=nome)
        else:
            cidadao__queryset = Cidadao.objects.none()

        if cidadao__queryset.exists():

            cidadao = cidadao__queryset.first()

            historico_saude = cidadao.historicos_saude.first()
            historico_criminal = cidadao.historicos_criminais.first()
            informacoes_complementares = cidadao.informacoes_complementares.first()
        
        else:
            return redirect('not_found_page')
    else:
        messages.error(request, 'Erro ao validar o formulario')

    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
    }

    return render(request, 'commons/include/buscar_nome.html', context)


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

@login_required
def sucess_page_view(request):
    template_name = 'commons/include/add_pages/sucess_page.html'
    return render(request, template_name)

def notfound_view(request):
    template_name='commons/include/add_pages/not_found.html'
    return render(request, template_name)

def missing_data_view(request):
    return render(request, 'commons/include/add_pages/missing_data.html')

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
        horas_a_subtrair = request.POST.get('horas_a_subtrair')
        
        if not cpf or not horas_a_subtrair:
            return HttpResponse("Parâmetros 'cpf' e 'horas_a_subtrair' não recebidos")
        
        try:
            horas_a_subtrair = float(horas_a_subtrair)
        except ValueError:
            return HttpResponseBadRequest("Horas a subtrair deve ser um número!")

        sucesso = reduzir_tempo(cpf, horas_a_subtrair)

        if sucesso:
            messages.success(request, "O tempo foi reduzido com sucesso.")
        else:
            messages.error(request, "CPF não encontrado ou ocorreu um erro.")
        
        # Redirecionar após a operação
        return redirect('exibir_time')

    # GET request
    cpf = request.GET.get('cpf')
    if cpf:
        try:
            cidadao = Cidadao.objects.get(cpf=cpf)
            time_list = cidadao.time.first()  # Supondo que 'time' é um related_name
        except Cidadao.DoesNotExist:
            return redirect('not_found_page')

    context = {
        'cidadao': cidadao,
        'time_list': time_list,
    }

    return render(request, 'commons/include/exibir_time.html', context)





    







        
        
    









    

        































            
           

