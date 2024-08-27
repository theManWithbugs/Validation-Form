from django.forms import ValidationError
from .models import *
import re

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





