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

    cpf = models.CharField(max_length=11, primary_key=True, verbose_name='Cpf:', unique=True)
    nome = models.CharField(max_length=80, verbose_name='Nome completo:')
    nome_social = models.CharField(max_length=80, blank=True, null=True, verbose_name='Nome social:', default='Não definido')
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
    class Meta:
        indexes = [
            models.Index(fields=['nome']),
        ]

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


    #metodo utilizado para controlar a conversão de dado para JSON quando armazenado na sessão
    def to_dict(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'nome_social': self.nome_social,
            'endereco': self.endereco,
            'moradia_situacao': self.moradia_situacao,
            'moradia_tipo': self.moradia_tipo,
            'cidade': self.cidade,
            'telefone': self.telefone,
            'estado': self.estado,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),  # Formata a data para string
            'idade': self.idade,
            'naturalidade': self.naturalidade,
            'sexo': self.sexo,
            'mae': self.mae,
            'estado_civil': self.estado_civil,
            'remuneracao': self.remuneracao,
            'renda_individual': self.renda_individual,
            'cor_raca': self.cor_raca,
            'escolaridade': self.escolaridade,
            'data_entrada': self.data_entrada.strftime('%Y-%m-%d')  # Formata a data para string
        }

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

    def to_dict(self):
        return {
        'cidadao': self.cidadao.cpf,
        'saude': self.saude,
        'saude_just': self.saude_just,
        'tratamento_psi': self.tratamento_psi,
        'tratamento_psi_jus': self.tratamento_psi_jus,
        'medicacao_controlada': self.medicacao_controlada,
        'medicacao_controlada_jus': self.medicacao_controlada_jus,
        'deficiencia': self.deficiencia,
        'drogas_uso': self.drogas_uso,
        'tratamento': self.tratamento
        }

# FORMULÁRIO 3
class HistoricoCriminal(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='historicos_criminais')
    ja_esteve_preso = models.CharField(max_length=3, choices=c_sim_nao, blank=True, verbose_name='Já esteve preso?:')
    prisao_justificativa = models.CharField(max_length=50, blank=True, null=True, verbose_name='Por qual motivo esteve preso?:')
    prisao_familiar = models.CharField(max_length=3, choices=c_sim_nao, blank=True, verbose_name='Alguém da sua familia já esteve preso?:')
    numero_do_processo = models.CharField(max_length=30, blank=False, verbose_name='Número do processo:')
    juiz_de_origem = models.CharField(max_length=50, blank=True, verbose_name='Juiz de origem:')
    medida_aplicada = models.CharField(max_length=50, blank=True, verbose_name='Medida aplicada:')
    tipo_penal = models.CharField(max_length=50, blank=True, verbose_name='Tipo penal:')
    violencia_domestica = models.CharField(max_length=50, blank=True, verbose_name='Em caso de violência domestica:')
    violencia_dome_nome_vitima = models.CharField(max_length=50, blank=True, verbose_name='Nome da vitima de violência domestica:')
    grau_de_parentesco = models.CharField(max_length=50, blank=True, verbose_name='Grau de parentesco da vitima:')
    reincidencia = models.CharField(max_length=3, choices=c_sim_nao, blank=True, null=True, verbose_name='Relata reincidência?:') 
    sugestao_de_trabalho = models.CharField(max_length=36, choices=c_sugestao_trabalho, blank=True, null=True)
    sugest_encaminhamento = models.CharField(max_length=36, choices=c_sugestao_encaminhamento, blank=True, null=True, verbose_name='Sugestão de encaminhamento:')

    class Meta:
        indexes = [
            models.Index(fields=['numero_do_processo']),
        ]

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

    def to_dict(self):
        return {
            'cidadao': self.cidadao.cpf,
            'ja_esteve_preso': self.ja_esteve_preso,
            'prisao_justificativa': self.prisao_justificativa,
            'prisao_familiar': self.prisao_familiar,
            'numero_do_processo': self.numero_do_processo,
            'juiz_de_origem': self.juiz_de_origem,
            'medida_aplicada': self.medida_aplicada,
            'tipo_penal': self.tipo_penal,
            'violencia_domestica': self.violencia_domestica,
            'violencia_dome_nome_vitima': self.violencia_dome_nome_vitima,
            'grau_de_parentesco': self.grau_de_parentesco,
            'reincidencia': self.reincidencia,
            'sugestao_de_trabalho': self.sugestao_de_trabalho,
            'sugest_encaminhamento': self.sugest_encaminhamento
        }

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

    def to_dict(self):
        return {
            'cidadao': self.cidadao.cpf,
            'quantas_pessoas': self.quantas_pessoas,
            'nome_familiar': self.nome_familiar,
            'parentesco': self.parentesco,
            'idade_familiar': self.idade_familiar,
            'escolaridade_familiar': self.escolaridade_familiar,
            'ocupacao': self.ocupacao,
            'analise_descritiva': self.analise_descritiva,
            'tip_penal': self.tip_penal,
            'medida_cumprimento': self.medida_cumprimento,
            'motivo_saida': self.motivo_saida
        }

class AcompCentral(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='form_acompanhamento_central')
    tecnico_responsavel = models.CharField(max_length=80, verbose_name='Técnico responsavel:', blank=False, null=False)
    evolucao_percepcoes = models.CharField(max_length=400, verbose_name='Evolução/ Demanda/ Percepções:')
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tecnico_responsavel
    
    def save(self, *args, **kwargs):
        self.tecnico_responsavel = self.tecnico_responsavel.upper()
        super().save(*args, **kwargs)

class ArmTime(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='time')
    time = models.IntegerField(default='', verbose_name='Tempo:')

    class Meta:
        indexes = [
            models.Index(fields=['time']),
        ]
    
    def __str__(self):
        return self.time

class ViolenDomest(models.Model):

    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, to_field='cpf', related_name='form_violencia_domes')
    process_referente = models.CharField(max_length=30, blank=False, verbose_name='A qual processo isso se refere?', unique=True)
    status_process = models.CharField(
                                    default='NAO INFORMADO',
                                    choices=c_status_process,
                                    max_length=13,
                                    verbose_name='Status do processo'
                                    )
    
    data_form_viole = models.DateField(auto_now_add=True)
    enteados = models.CharField(
                                default='Selecione',
                                choices=c_sim_nao,
                                max_length=9,
                                verbose_name='Tem enteados?'
                                 )
    
    religiao = models.CharField(
                                blank=True,
                                null=True,
                                max_length=80,
                                verbose_name='Pratica alguma religião? Qual?'
                                )
    
    trab_vitima = models.CharField(max_length=80, blank=True, null=True, verbose_name='A vitima trabalhava qual era a profissão?')
    dependencia_fin = models.CharField(
                                        default='Selecione',
                                        choices=c_sim_nao,
                                        max_length=80,
                                        verbose_name='A vitima dependia financeiramente de você?'
                                        )
    
    autor_alcool = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name='O autor faz uso de álcool?',
                                    max_length=9
                                    )
    
    uso_drogas_viole = models.CharField(
                                        max_length=80,
                                        blank= True,
                                        null=True,
                                        verbose_name='O autor faz uso de drogas? Qual?'
                                        )
    
    raça_ident = models.CharField(
                                    default='Selecione',
                                    choices=c_raca_cor,
                                    verbose_name='Com qual cor/raça você se identifica?',
                                    max_length=8
                                )

    filhos_agress = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name='Os filhos já presenciaram alguma agressão?',
                                    max_length=9
                                    )
    
    ameacar_suicidio = models.CharField(
                                        default='Selecione',
                                        choices=c_sim_nao,
                                        verbose_name='O autor já tentou ou ameçou suicidar-se?',
                                        max_length=9
                                        )
    
    dificul_finan = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name='O autor está desempregado ou possui dificuldades financeira graves?',
                                    max_length=9
                                    )
    
    acesso_armas = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name='O autor tem acesso a armas de fogo?',
                                    max_length=9
                                    )
    
    relacao_vit = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name ='Que tipo de relação mantém atualmente com a vitima?',
                                    max_length=9
                                    )
    
    reconhe_violencia = models.CharField(
                                        default='Selecione',
                                        choices=c_sim_nao,
                                        verbose_name='Você reconhece que usou de violência(física, psicológica, entre outras) em relação à vitima?',
                                        max_length=9
                                        )
    
    arrepen = models.CharField(
                                default='Selecione',
                                choices=c_sim_nao,
                                verbose_name='Você se sente arrependido?',
                                max_length=9
                                )
    
    sentim_vitim = models.CharField(
                                    blank=True,
                                    null=True,
                                    verbose_name='Qual seu sentimento em relação à vitima?',
                                    max_length=300,
                                    )
    
    passagen_ant = models.CharField(
                                    default='Selecione',
                                    choices=c_sim_nao,
                                    verbose_name='Já passou por esse grupo que trata sobre violência doméstica?',
                                    max_length=9
                                    )
    
    tecnico_responsavel_vio = models.CharField(
                                            blank=False,
                                            null=False,
                                            verbose_name='Tecnico reponsavel:',
                                            max_length=80
                                            )
    
    def __str__(self):
        return f"Historico Violência domestica {self.cidadao.cpf}"


    
  

    
    

    
        



      


