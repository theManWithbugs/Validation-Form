from urllib import request
from django import forms
from django.shortcuts import redirect, render
from .models import *
from django.core.exceptions import ValidationError
import re

#classe de validação de cpf
class CPFValidationForm(forms.Form):
    cpf = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        label='CPF'
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        label='Senha'
    )

    #função de calculo de cpf
    def clean_cpf(self):
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

#classes para cadastro dos formularios
class CidadaoForm(forms.ModelForm):
    class Meta:
        model = Cidadao
        fields = '__all__'
class HistoricoSaudeForm(forms.ModelForm):
    class Meta:
        model = HistoricoSaude
        fields = '__all__'
        exclude = ['cidadao']  # Excluindo o campo cidadao do formulário
 
class HistoricoCriminalForm(forms.ModelForm):
    class Meta:
        model = HistoricoCriminal
        fields = '__all__'
        exclude = ['cidadao']  # Excluindo o campo cidadao do formulário


class InformacoesComplementaresForm(forms.ModelForm):
    class Meta:
        model = InformacoesComplementares
        fields = '__all__'
        exclude = ['cidadao']  # Excluindo o campo cidadao do formulário

#Essa classe é usada para buscar o cidadão pelo cpf
class BuscarCidadaoForm(forms.Form):
    cpf = forms.CharField(label='CPF', max_length=11, required=True)

#-------------------------------------------------------------------#
class AlterarDadosForm(forms.ModelForm):
    class Meta:
        model = Cidadao
        fields = '__all__'






    


        



