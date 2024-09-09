from tkinter import CASCADE
from django.conf import settings
from django.utils import timezone
from django.db import models
from core.choices import *  # Certifique-se de que todas as escolhas estão corretamente definidas
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF deve ser fornecido')
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.cpf
    
# FORMULÁRIO 1
class Cidadao(models.Model):

    cpf = models.CharField(max_length=11, primary_key=True, verbose_name='Cpf:')
    nome = models.CharField(max_length=80, verbose_name='Nome completo:')
    nome_social = models.CharField(max_length=80, blank=True, null=True, default='Não informado', verbose_name='Nome social:')
    endereco = models.CharField(max_length=80, verbose_name='Endereço:')
    moradia_situacao = models.CharField(
                        max_length=15,
                        choices=c_moradia_situacao,
                        verbose_name='Situação de moradia, tipo de ocupação:',
                        blank=True,
                        null=True
                    )
    
    moradia_tipo = models.CharField(
                        max_length=9,
                        choices=c_moradia_tipo,
                        verbose_name='Tipo de moradia:',
                        blank=True,
                        null=True
                    )

    cidade = models.CharField(max_length=20, verbose_name='Cidade:')
    telefone = models.CharField(max_length=13, verbose_name='Telefone:')
    estado = models.CharField(
                    choices=c_estado,
                    verbose_name='Estado:',
                    max_length=19,
                    blank=False,
                    null=False,
                     )
    data_nascimento = models.DateField(blank=False, verbose_name='Data de Nascimento:')
    idade = models.CharField(max_length=3, verbose_name='Idade:')  
    naturalidade = models.CharField(max_length=50, verbose_name='Naturalidade:')
    sexo = models.CharField(max_length=1, choices=c_sexo, default='selecione', verbose_name='Sexo:')
    mae = models.CharField(max_length=50, verbose_name='Nome da mãe:')
    estado_civil = models.CharField(choices=c_estado_civil,
                                    default='selecione',
                                    max_length=20)
    remuneracao = models.CharField(max_length=20, choices=c_remuneracao, blank=True, verbose_name='Remuneração:')
    renda_individual = models.CharField(max_length=50, choices=c_renda_invidual)
    cor_raca = models.CharField(max_length=8, choices=c_raca_cor, verbose_name='Cor/Raça:')
    escolaridade = models.CharField(
                                choices=c_escolaridade,
                                max_length=22,
                                default='selecione'
                                    )
    data_entrada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Converte os campos de texto para maiúsculas
        self.nome = self.nome.upper()
        self.nome_social = self.nome_social.upper()
        self.endereco = self.endereco.upper()
        self.cidade = self.cidade.upper()
        self.estado = self.estado.upper()
        self.naturalidade = self.naturalidade.upper()
        self.mae = self.mae.upper()
        self.estado_civil = self.estado_civil.upper()
        self.remuneracao = self.remuneracao.upper()
        self.cor_raca = self.cor_raca.upper()
        self.escolaridade = self.escolaridade.upper()
        super().save(*args, **kwargs)

# FORMULÁRIO 2
class HistoricoSaude(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='historicos_saude')
    saude = models.CharField(
                            choices=c_sim_nao,
                            max_length=3,
                            default='Selecione',
                            verbose_name='Apresenta problemas de saude?'
                             )
    saude_just = models.CharField(max_length=80, verbose_name='Se apresenta problema de saúde qual?', blank=True, null=True)
    

    tratamento_psi = models.CharField(
                                    choices=c_sim_nao,
                                    max_length=3, 
                                    verbose_name='Faz ou fez tratamento psiquiatrico?',
                                    default='Selecione'
                                    )
    tratamento_psi_jus = models.CharField(max_length=80, verbose_name='Especifique o tratamento psiquiatrico:')

    medicacao_controlada = models.CharField(
                                            choices=c_sim_nao,
                                            max_length=3, 
                                            default='Selecione', 
                                            verbose_name='Faz uso de alguma medicação controlada?')
    
    medicacao_controlada_jus = models.CharField(max_length=80, blank=True, null=True, verbose_name='Especifique o tipo de medicação controlada:')

    deficiencia = models.CharField(
        choices=c_sim_nao,
        max_length=3, 
        verbose_name='É portador de alguma deficiência:')
    
    drogas_uso = models.CharField(
        max_length=20,
        choices=DROGAS_CHOICES, 
        blank=True,
        null=True,
        verbose_name='Faz ou já fez uso de:'
    )
    tratamento = models.CharField(
                                choices=c_sim_nao,
                                max_length=3, 
                                default='', 
                                verbose_name='Já procurou tratamento?')  # Definido como não-nulo com valor padrão
    
    def __str__(self):
        return f"Histórico de Saúde do Cidadão {self.cidadao.cpf}"
    
    def save(self, *args, **kwargs):
        self.saude = self.saude.upper()
        self.saude_just = self.saude_just.upper()
        self.tratamento_psi = self.tratamento_psi.upper()
        self.tratamento_psi_jus = self.tratamento_psi_jus.upper()
        self.medicacao_controlada = self.medicacao_controlada.upper()
        self.medicacao_controlada_jus = self.medicacao_controlada_jus.upper()
        self.deficiencia = self.deficiencia.upper()
        self.tratamento = self.tratamento.upper()
        super().save(*args, **kwargs)

# FORMULÁRIO 3
class HistoricoCriminal(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='historicos_criminais')
    ja_esteve_preso = models.CharField(max_length=3, choices=c_sim_nao, blank=True)
    prisao_justificativa = models.CharField(max_length=50, blank=True, null=True)
    prisao_familiar = models.CharField(max_length=3, choices=c_sim_nao, blank=True)
    numero_do_processo = models.CharField(max_length=30, blank=False)
    juiz_de_origem = models.CharField(max_length=50, blank=True)
    medida_aplicada = models.CharField(max_length=50, blank=True)
    tipo_penal = models.CharField(max_length=50, blank=True)
    violencia_domestica = models.CharField(max_length=50, blank=True, verbose_name='Em caso de violência domestica:')
    violencia_dome_nome_vitima = models.CharField(max_length=50, blank=True, verbose_name='Nome da vitima de violência domestica:')
    grau_de_parentesco = models.CharField(max_length=50, blank=True, verbose_name='Grau de parentesco da vitima:')
    reincidencia = models.CharField(max_length=3, choices=c_sim_nao, blank=True, null=True, verbose_name='Relata reincidência?:') 
    sugestao_de_trabalho = models.CharField(max_length=36, choices=c_sugestao_trabalho, blank=True, null=True)
    sugest_encaminhamento = models.CharField(max_length=36, choices=c_sugestao_encaminhamento, blank=True, null=True, verbose_name='Sugestão de encaminhamento:')

    def __str__(self):
        return f"Histórico Criminal do Cidadão {self.cidadao.cpf}"
    
    def save(self, *args, **kwargs):
        self.juiz_de_origem = self.juiz_de_origem.upper()
        self.medida_aplicada = self.medida_aplicada.upper()
        self.tipo_penal = self.tipo_penal.upper()
        self.violencia_domestica = self.violencia_domestica.upper()
        self.violencia_dome_nome_vitima = self.violencia_dome_nome_vitima.upper()
        self.grau_de_parentesco = self.grau_de_parentesco.upper()
        super().save(*args, **kwargs)

# FORMULÁRIO 4
class InformacoesComplementares(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='informacoes_complementares')
    quantas_pessoas = models.CharField(max_length=2, verbose_name='Quantas pessoas moram com você ? (inclua você na contagem)')
    nome_familiar = models.CharField(max_length=70, verbose_name='Nome de um familiar:')
    parentesco = models.CharField(max_length=100, default='', verbose_name='Grau de parentesco:')
    idade_familiar = models.CharField(max_length=3, verbose_name='Idade do familiar:', blank=True)  # Valor padrão definido
    escolaridade_familiar = models.CharField(  
                                            choices=c_escolaridade,
                                            max_length=30, 
                                            default='selecione',
                                            verbose_name='Grau de Escolaridade do familiar:')
    
    ocupacao = models.CharField(max_length=100, verbose_name='Ocupação:')
    analise_descritiva = models.CharField(max_length=300, verbose_name='Análise descritiva:')
    tip_penal = models.CharField( 
                                    default='selecione',
                                    choices=c_tip_penal,
                                    max_length=30,
                                    verbose_name='Tipificação penal:'
                                )
    
    medida_cumprimento = models.CharField(      
                                            default='selecione',
                                            max_length=50,
                                            choices=c_medida_cumprimento,
                                            verbose_name='Medida de cumprimento:',
                                            )
    motivo_saida = models.CharField(
                                    default='nao definido',
                                    choices=c_motivo_saida,
                                    max_length=40,
                                    verbose_name='Motivo de saida:'
                                    )
    
    def __str__(self):
        return self.nome_familiar
    
    def save(self, *args, **kwargs):
        self.quantas_pessoas = self.quantas_pessoas.upper()
        self.nome_familiar = self.nome_familiar.upper()
        self.parentesco = self.parentesco.upper()
        self.idade_familiar = self.idade_familiar.upper()
        self.escolaridade_familiar = self.escolaridade_familiar.upper()
        self.ocupacao = self.ocupacao.upper()
        self.analise_descritiva = self.analise_descritiva.upper()
        super().save(*args, **kwargs)

class AcompCentral(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='form_acompanhamento_central')
    tecnico_responsavel = models.CharField(max_length=80, verbose_name='Técnico responsavel:')
    evolucao_percepcoes = models.CharField(max_length=400, verbose_name='Evolução/ Demanda/ Percepções:')
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tecnico_responsavel
    
    def save(self, *args, **kwargs):
        self.tecnico_responsavel = self.tecnico_responsavel.upper()
        super().save(*args, **kwargs)

class ArmTime(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='time')
    time = models.IntegerField()

    
        



      


