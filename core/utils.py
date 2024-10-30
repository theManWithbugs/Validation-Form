from datetime import timedelta
from itertools import count
from django.forms import ValidationError
from requests import request
from .models import *
import re
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#funçãp para validar cpf fora da classe CPFValidationForm
def clean_cpf_out(self):
    cpf = self.cleaned_data.get('cpf', '')
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        raise ValidationError('O CPF deve conter 11 dígitos')

    if cpf == cpf[0] * 11:
         raise ValidationError('CPF inválido')

    def calcular_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    peso1 = list(range(10, 1, -1))
    peso2 = list(range(11, 1, -1))

    digito1 = calcular_digito(cpf[:-2], peso1)
    digito2 = calcular_digito(cpf[:-1] + str(digito1), peso2)

    if not (int(cpf[-2]) == digito1 and int(cpf[-1]) == digito2):
         raise ValidationError('CPF inválido')

    return cpf

#função para realizar calculo da porcentagem de aumento mensal de usuarios 
def calcular_porcent():
    agora = timezone.now()
    
    # Definir o início e fim do mês atual
    inicio_do_mes = agora.replace(day=1)
    fim_do_mes = (inicio_do_mes + timedelta(days=31)).replace(day=1)
    
    # Contar os cadastros do mês atual
    cadastros_este_mes = Cidadao.objects.filter(data_entrada__gte=inicio_do_mes, data_entrada__lt=fim_do_mes).count()
    
    # Definir o início e fim do mês anterior
    inicio_mes_anterior = (inicio_do_mes - timedelta(days=1)).replace(day=1)
    fim_mes_anterior = inicio_do_mes
    
    # Contar os cadastros do mês anterior
    cadastros_mes_anterior = Cidadao.objects.filter(data_entrada__gte=inicio_mes_anterior, data_entrada__lt=fim_mes_anterior).count()
    
    # Evitar divisão por zero e tratar o caso onde o mês anterior não tem cadastros
    if cadastros_mes_anterior == 0:
        return float('inf') if cadastros_este_mes > 0 else 0
    
    # Calcula o aumento percentual
    aumento_percentual = ((cadastros_este_mes - cadastros_mes_anterior) / cadastros_mes_anterior) * 100
    return aumento_percentual

#função para calcular porcentagem de usuarios masculinos e femininos
def calcular_sexo():
    masculino_count = Cidadao.objects.filter(sexo='M', unidade='IAPEN-RB').count()
    feminino_count = Cidadao.objects.filter(sexo='F', unidade='IAPEN-RB').count()

    total_count = masculino_count + feminino_count

    if total_count == 0:
        porcentagem_masculino = 0
        porcentagem_feminino = 0
    else:
        porcentagem_masculino = (masculino_count / total_count) * 100
        porcentagem_feminino = (feminino_count / total_count) * 100

    return porcentagem_masculino, porcentagem_feminino

def contar_ativos():
    ativos = InformacoesComplementares.objects.filter(motivo_saida='ATIVO').count()

    return ativos

def tipo_penal():

    tipos = [
        'VIOLENCIA DOMESTICA', 'FURTO', 'CRIME AMBIENTAL', 'RACISMO', 'TRANSITO',
        'CRIME DE DROGAS', 'OUTROS CRIMES', 'LESAO CORPORAL', 'CRIME DE ARMA', 'ESTELIONATO'
    ]
    resultado = {}
    
    for tipo in tipos:
        resultado[tipo] = InformacoesComplementares.objects.filter(tip_penal=tipo, cidadao__unidade='IAPEN-RB').count()

    total = sum(resultado.values())

    if total > 0:
        porcentagens = {tipo: (count / total) * 100 for tipo, count in resultado.items()}
    else:
        porcentagens = {tipo: 0 for tipo in tipos}

    sorted_porcentagens = sorted(porcentagens.items(), key=lambda x: x[1], reverse=True)

    return sorted_porcentagens

def medida_cumprimento_calc():
    tipos = [
        'COMPARECIMENTO BIMESTRAL', 'COMPARECIMENTO MENSAL', 'COMPARECIMENTO QUINZENAL',
        'COMPARECIMENTO SEMANAL', 'COMPARECIMENTO TRIMESTRAL', 'GRUPO REFLEXIVO', 'PSC'
    ]

    resultado_medida = {}

    for tipo in tipos:
        resultado_medida[tipo] = InformacoesComplementares.objects.filter(medida_cumprimento=tipo, cidadao__unidade='IAPEN-RB').count()
    
    return resultado_medida

def medida_cumprimento_saida():
    tipos = [
        'NAO DEFINIDO', 'ATIVO', 'CUMPRIMENTO INTEGRAL', 'DESCUMPRIMENTO', 'PRISAO', 'OUTRO'
    ]

    resultado_medida_saida = {}

    for tipo in tipos:
        resultado_medida_saida[tipo] = InformacoesComplementares.objects.filter(motivo_saida=tipo, cidadao__unidade='IAPEN-RB').count()
    
    return resultado_medida_saida

def tipo_penal_quant():
    tipos = [
        'VIOLENCIA DOMESTICA', 'FURTO', 'CRIME AMBIENTAL', 'RACISMO', 'TRANSITO',
        'CRIME DE DROGAS', 'OUTROS CRIMES', 'LESAO CORPORAL', 'CRIME DE ARMA', 'ESTELIONATO'
    ]
    resultado = {}

    for tipo in tipos:
        resultado[tipo] = InformacoesComplementares.objects.filter(tip_penal=tipo, cidadao__unidade='IAPEN-RB').count()

    return resultado

def contar_faixa_etaria():
    faixa_etarias = {
        "18 a 24": Cidadao.objects.filter(idade__gte=18, idade__lte=24, unidade='IAPEN-RB').count(),
        "25 a 29": Cidadao.objects.filter(idade__gte=25, idade__lte=29, unidade='IAPEN-RB').count(),
        "30 a 34": Cidadao.objects.filter(idade__gte=30, idade__lte=34, unidade='IAPEN-RB').count(),
        "35 a 59": Cidadao.objects.filter(idade__gte=35, idade__lte=59, unidade='IAPEN-RB').count(),
    }
    
    return faixa_etarias

def contar_faixa_etaria_porcentagem_sta():
    media1 = Cidadao.objects.filter(idade__gte=18, idade__lte=24, unidade='IAPEN-RB').count() 
    media2 = Cidadao.objects.filter(idade__gte=25, idade__lte=29, unidade='IAPEN-RB').count() 
    media3 = Cidadao.objects.filter(idade__gte=30, idade__lte=34, unidade='IAPEN-RB').count()
    media4 = Cidadao.objects.filter(idade__gte=35, idade__lte=59, unidade='IAPEN-RB').count()  

    total = media1 + media2 + media3 + media4

    if total > 0:
        porcentagens = {
            '18-24': (media1 / total) * 100,
            '25-29': (media2 / total) * 100,
            '30-34': (media3 / total) * 100,
            '35-39': (media4 / total) * 100,
        }
    else:
        porcentagens = {
            '18-24': 0,
            '25-29': 0,
            '30-34': 0,
            '35-39': 0,
        }

    return porcentagens

def contar_faixa_etaria_porcentagem():
    media1 = Cidadao.objects.filter(idade__gte=18, idade__lte=24, unidade='IAPEN-RB').count() 
    media2 = Cidadao.objects.filter(idade__gte=25, idade__lte=29, unidade='IAPEN-RB').count() 
    media3 = Cidadao.objects.filter(idade__gte=30, idade__lte=34, unidade='IAPEN-RB').count()
    media4 = Cidadao.objects.filter(idade__gte=35, idade__lte=39, unidade='IAPEN-RB').count()  

    total = media1 + media2 + media3 + media4

    if total > 0:
        porcentagens = [
            ['De 18-24', round((media1 / total) * 100, 2)],
            ['De 25-29', round((media2 / total) * 100, 2)],
            ['De 30-34', round((media3 / total) * 100, 2)],
            ['De 35-39', round((media4 / total) * 100, 2)],
        ]
    else:
        porcentagens = [
            ['De 18-24', 0.00],
            ['De 25-29', 0.00],
            ['De 30-34', 0.00],
            ['De 35-39', 0.00],
        ]

    return porcentagens

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Tivemos alguns errors <pre>' + html + '</pre>')
    return response

#---------------------------------------------------------------------------------------------------------------------#

def calcular_sexo_ativos():

    #É possível usar o doublescore __ para referenciar modelos diferentes quando existe uma chave primaria
    #interligando os dois modelos.
    masculino_count = Cidadao.objects.filter(sexo='M', informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count()
    feminino_count = Cidadao.objects.filter(sexo='F', informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count()

    total_count = masculino_count + feminino_count

    if total_count == 0:
        porcentagem_masculino = 0
        porcentagem_feminino = 0
    else:
        porcentagem_masculino = (masculino_count / total_count) * 100
        porcentagem_feminino = (feminino_count / total_count) * 100

    return porcentagem_masculino, porcentagem_feminino

def tipo_penal_ativos():
    tipos = [
        'VIOLENCIA DOMESTICA', 'FURTO', 'CRIME AMBIENTAL', 'RACISMO', 'TRANSITO',
        'CRIME DE DROGAS', 'OUTROS CRIMES', 'LESAO CORPORAL', 'CRIME DE ARMA', 'ESTELIONATO'
    ]
    resultado = {}
    
    for tipo in tipos:
        resultado[tipo] = InformacoesComplementares.objects.filter(tip_penal=tipo, motivo_saida='ATIVO', cidadao__unidade='IAPEN-RB').count()

    total = sum(resultado.values())

    if total > 0:
        porcentagens = {tipo: (count / total) * 100 for tipo, count in resultado.items()}
    else:
        porcentagens = {tipo: 0 for tipo in tipos}

    sorted_porcentagens = sorted(porcentagens.items(), key=lambda x: x[1], reverse=True)

    return sorted_porcentagens

def medida_cumprimento_calc_ativos():
    tipos = [
        'COMPARECIMENTO BIMESTRAL', 'COMPARECIMENTO MENSAL', 'COMPARECIMENTO QUINZENAL',
        'COMPARECIMENTO SEMANAL', 'COMPARECIMENTO TRIMESTRAL', 'GRUPO REFLEXIVO', 'PSC'
    ]

    resultado_medida = {}

    for tipo in tipos:
        resultado_medida[tipo] = InformacoesComplementares.objects.filter(medida_cumprimento=tipo, motivo_saida='ATIVO', cidadao__unidade='IAPEN-RB').count()
    
    return resultado_medida

def contar_faixa_etaria_porcentagem_ativos():
    media1 = Cidadao.objects.filter(idade__gte=18, idade__lte=24, informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count() 
    media2 = Cidadao.objects.filter(idade__gte=25, idade__lte=29, informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count() 
    media3 = Cidadao.objects.filter(idade__gte=30, idade__lte=34, informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count()
    media4 = Cidadao.objects.filter(idade__gte=35, idade__lte=59, informacoes_complementares__motivo_saida='ATIVO', unidade='IAPEN-RB').count()  

    total = media1 + media2 + media3 + media4

    if total > 0:
        porcentagens = [
            ['De 18-24', round((media1 / total) * 100, 2)],
            ['De 25-29', round((media2 / total) * 100, 2)],
            ['De 30-34', round((media3 / total) * 100, 2)],
            ['De 35-39', round((media4 / total) * 100, 2)],
        ]
    else:
        porcentagens = [
            ['De 18-24', 0.00],
            ['De 25-29', 0.00],
            ['De 30-34', 0.00],
            ['De 35-39', 0.00],
        ]

    return porcentagens






    


    




    



    
    

    
    




