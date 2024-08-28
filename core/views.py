from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .forms import *
from .forms import CidadaoForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

# variaveis de ambiente
progName = 'CONDUTA'
msgSucesso = 'Operação realizada com sucesso!'
msgError = 'Não foi possivel salvar as alterações solicitadas!'
msgIntegridade = 'Você tentou salvar um registro que já existe! Por favor, verifique e tente novamente.'
iten_rage_page = 30  # registros por página

def login_n(request):
    if request.method == 'POST':
        form = CPFValidationForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']

            user = authenticate(request, username = cpf, password=senha)
            if user is not None:
                login(request, user)
                messages.success(request, msgSucesso)
                return redirect('base')

            else: 
                form.add_error('cpf', 'CPF ou senha incorretos.')
        else:
            messages.error(request, 'Erro no formulario. Por favor, verifique os campos.')
    else:
        form = CPFValidationForm()

    return render(request, 'account/login_n.html', {'form': form})

@login_required
def base_view(request):
    return render(request, 'base.html')

@login_required
def home(request):
    template_name='commons/home.html'
    formName = 'home'
    context={
        'progName': progName,
        'formName': formName,
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
            #armazena o cpf do cidadão na sesão para que possa ser utilizado em uma requisição futura
            request.session['cidadao_cpf'] = cidadao.cpf
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
                return redirect('form4')
            except IntegrityError:
                messages.error(request, 'Já existe um registro de histórico criminal para este cidadão.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = HistoricoCriminalForm()

    return render(request, 'commons/include/form3.html', {'formulario_tecnico': form})

def form4_view(request):
    cidadao_cpf = request.session.get('cidadao_cpf')
    if not cidadao_cpf:
        messages.error(request, 'Dados do cidadão não encontrados.')
        return redirect('form1')
    
    #recupera o objeto ou exibe um erro caso não seja possivel
    cidadao = get_object_or_404(Cidadao, cpf=cidadao_cpf)

    if request.method == 'POST':
        form = InformacoesComplementaresForm(request.POST)
        if form.is_valid():
            informacoes_complementares = form.save(commit=False)
            informacoes_complementares.cidadao = cidadao
            informacoes_complementares.save()
            return redirect('sucess_page')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = InformacoesComplementaresForm()
        
    return render(request, 'commons/include/form4.html', {'formulario_complementar': form})

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
    else:
        messages.error(request, 'Formulario invalido!')

    # Prepara o contexto para o template, incluindo o formulário e as informações recuperadas
    context = {
        'form': form,
        'cidadao': cidadao,
        'historico_saude': historico_saude,
        'historico_criminal': historico_criminal,
        'informacoes_complementares': informacoes_complementares,
    }
    
    # Renderiza o template 'busca_form.html' com o contexto preparado
    return render(request, 'commons/include/busca_form.html', context)

def edit_form_view(request):
    return render(request, 'commons/include/editar_form.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login_new')

def footer_view(request):
    template_name = 'commons/include/footer.html'
    return render(request, template_name)

def usuario_view(request):
    return render(request, 'account/perfil.html')

def notfound_view(request):
    template_name='commons/include/not_found.html'
    return render(request, template_name)

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

#view para atualizar dados do formulario
@login_required
def atualizar_dados(request, cpf):
    try:
        cidadao = Cidadao.objects.get(cpf=cpf)
    except Cidadao.DoesNotExist:
        messages.error(request, 'Cidadao não encontrado')
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
            messages.success(request, 'Dados atualizados com sucesso')
            return redirect('base')
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

@login_required
def capturar_cpf(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        if cpf:
            return redirect('atualizar_dados', cpf=cpf)
        else:
            messages.error(request, 'CPF não fornecido')
    return render(request, 'commons/include/capturar_cpf.html')


def sucess_page_view(request):
    template_name = 'commons/include/sucess_page.html'
    return render(request, template_name)


        































            
           

