from datetime import timedelta
from django.forms import ValidationError
from .models import *
import re
from django.utils import timezone

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
    masculino_count = Cidadao.objects.filter(sexo='M').count()
    feminino_count = Cidadao.objects.filter(sexo='F').count()

    total_count = masculino_count + feminino_count

    if total_count == 0:
        porcentagem_masculino = 0
        porcentagem_feminino = 0
    else:
        porcentagem_masculino = (masculino_count / total_count) * 100
        porcentagem_feminino = (feminino_count / total_count) * 100

    return porcentagem_masculino, porcentagem_feminino

def reduzir_tempo(cpf, horas_a_subtrair):
    try:
        arm_time = ArmTime.objects.get(cidadao__cpf=cpf)
        arm_time.time -= horas_a_subtrair
        arm_time.save()
        return True
    except ArmTime.DoesNotExist:
        return False


    




    



    
    

    
    




