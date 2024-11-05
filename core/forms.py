from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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

#
#  função de calculo de cpf
#  def clean_cpf(self):
#       cpf = self.cleaned_data.get('cpf', '')
#       cpf = re.sub(r'\D', '', cpf)
#
#       if len(cpf) != 11:
#           raise ValidationError('O CPF deve conter 11 dígitos')
#
#       if cpf == cpf[0] * 11:
#           raise ValidationError('CPF inválido')
#
#       def calcular_digito(cpf, peso):
#           soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
#           resto = (soma * 10) % 11
#           return 0 if resto == 10 else resto
#
#       peso1 = list(range(10, 1, -1))
#       peso2 = list(range(11, 1, -1))
#
#       digito1 = calcular_digito(cpf[:-2], peso1)
#       digito2 = calcular_digito(cpf[:-1] + str(digito1), peso2)
#
#       if not (int(cpf[-2]) == digito1 and int(cpf[-1]) == digito2):
#           raise ValidationError('CPF inválido')
#
#       return cpf

#classes para cadastro dos formularios

class CidadaoForm(forms.ModelForm):
    class Meta:
        model = Cidadao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CidadaoForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'

class HistoricoSaudeForm(forms.ModelForm):
    class Meta:
        model = HistoricoSaude
        fields = '__all__'
        exclude = ['cidadao']  

    def __init__(self, *args, **kwargs):
        super(HistoricoSaudeForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'
 
class HistoricoCriminalForm(forms.ModelForm):
    class Meta:
        model = HistoricoCriminal
        fields = '__all__'
        exclude = ['cidadao']   

    def __init__(self, *args, **kwargs):
        super(HistoricoCriminalForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'


class InformacoesComplementaresForm(forms.ModelForm):
    class Meta:
        model = InformacoesComplementares
        fields = '__all__'
        exclude = ['cidadao']  

    def __init__(self, *args, **kwargs):
        super(InformacoesComplementaresForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'

class AcompCentralForm(forms.ModelForm):
    class Meta:
        model = AcompCentral
        fields = '__all__'
        exclude = ['cidadao']
        widgets = {
            'tecnico_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'evolucao_percepcoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AcompCentralForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'

#Essa classe é usada para buscar o cidadão pelo cpf
class BuscarCidadaoForm(forms.Form):
    nome = models.CharField(max_length=80)
    cpf = forms.CharField(label='CPF', max_length=11, required=True)

class BuscarNomeForm(forms.Form):
    nome = forms.CharField(max_length=80, required=True)

class AlterarDadosForm(forms.ModelForm):
    class Meta:
        model = Cidadao
        fields = '__all__'
        exclude = ['unidade']

    def __init__(self, *args, **kwargs):
        super(AlterarDadosForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'

class UserCreationFormCustom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('cpf', 'nome', 'is_active', 'is_staff', 'is_superuser')
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

class UserChangeFormCustom(UserChangeForm):
    class Meta:
        model = User
        fields = ('cpf', 'nome', 'is_active', 'is_staff', 'is_superuser')

class ViolenDomestForm(forms.ModelForm):
    class Meta:
        model = ViolenDomest
        fields= '__all__'
        exclude = ['data_form_viole', 'cidadao']

    def __init__(self, *args, **kwargs):
        super(ViolenDomestForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'

class ViolenDomestFormTwo(forms.ModelForm):
    class Meta:
        model = ViolenDomest
        fields= ('process_referente', 'status_process')
        exclude = ['data_form_viole', 'cidadao']

    def __init__(self, *args, **kwargs):
        super(ViolenDomestFormTwo, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control form-control-sm'
            self.fields['process_referente'].widget.attrs['readonly'] = 'readonly'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']



       








    


        



