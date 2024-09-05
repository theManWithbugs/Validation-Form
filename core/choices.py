c_sim_nao = (
    ('', 'Selecione'),
    ('SIM', 'Sim'),
    ('NAO', 'Não'),
)

c_perigo = (
    ('', 'Selecione'),
    ('B', 'Baixa'),
    ('M', 'Média'),
    ('A', 'Alta'),
)

c_ativo = (
    ('A', 'Ativo'),
    ('I', 'Inativo')
)

c_sexo = (
    ('', 'Selecione'),
    ('M', 'Masculino'),
    ('F', 'Feminino')
)

c_ori_sex = (
    ('', 'Selecione'),
    ('HET', 'Heterossexual'),
    ('HOM', 'Homossexual'),
    ('BIS', 'Bissexual'),
    ('ASS', 'Assexual'),
    ('PAN', 'Pansexual'),
    ('LGB', 'LGBTQIA+'),
)

c_ident_gen = (
    ('', 'Selecione'),
    ('CIS', 'Cisgênero'),
    ('TRA', 'Transgênero'),
    ('NBN', 'Não-binário'),
    ('OTS', 'Outros'),
)

c_est_civil = (
    ('', 'Selecione'),
    ('CAS', 'Casado(a)'),
    ('DIV', 'Divorciado(a)'),
    ('SEP', 'Separado(a)'),
    ('SOL', 'Solteiro(a)'),
    ('UNI', 'União estável'),
    ('VIU', 'Viúvo(a)'),
)

c_raca_cor = (
    ('', 'Selecione'),
    ('AMARELA', 'Amarela'),
    ('INDIO', 'Índigena'),
    ('BRANCO', 'Branca'),
    ('PARDO', 'Pardo'),
    ('PRETA', 'Preta'),
)

c_grau_instrucao = (
    ('', 'Selecione'),
    ('ANF', 'Não alfabetizado'),
    ('EFI', 'Ensino fundamental incompleto'),
    ('EFC', 'Ensino fundamental completo'),
    ('EMI', 'Ensino médio incompleto'),
    ('EMC', 'Ensino médio completo'),
    ('ESI', 'Ensino superior incompleto'),
    ('ESC', 'Ensino superior completo'),
    ('PSG', 'Pós-graduação'),
    ('MSD', 'Mestrado'),
    ('DRD', 'Doutorado'),
    ('PDR', 'Pós-Doutorado'),
)

c_ufs = (
    ('', 'Selecione'),
    ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
    ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
    ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
    ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
    ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
    ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
    ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
)

c_perioculosidade = (
    ('','Selecione'),
    ('B', 'Baixa'),
    ('M', 'Média'),
    ('A', 'Alta'),
)

DROGAS_CHOICES = (
    ('ALCOOL', 'Álcool'),
    ('CIGARRO', 'Cigarro'),
    ('MACONHA', 'Maconha'),
    ('PASTA BASE', 'Pasta Base'),
    ('COCAINA', 'Cocaína'),
    ('MERLA', 'Merla'),
    ('CRACK', 'Crack'),
    ('OUTRAS DROGAS', 'Outras drogas'),
)

c_sugestao_trabalho = (
    ('DEPENDENCIA QUIMICA', 'DEPENDENCIA QUIMICA'),
    ('MULHERES', 'MULHERES'),
    ('OUTRO DELITOS', 'OUTROS DELITOS'),
    ('PRESTAÇÃO DE SERVÇOS A COMUNIDADE', 'PRESTAÇÃO DE SERVÇOS A COMUNIDADE'),
    ('TRAFICO DE DROGAS', 'TRAFICO DE DROGAS'),
    ('TRANSITO', 'TRANSITO'),
    ('VIOLÊNCIA DOMESTICA', 'VIOLÊNCIA DOMESTICA'),
)

c_sugestao_encaminhamento = (
    ('SASDH', 'SASDH'),
    ('NATERA-MP', 'NATERA-MP'),
    ('GRUPO NAA OU AA', 'GRUPO NAA OU AA'),
    ('INTERNAÇÃO EM COMUNIDADE TERAPÊUTICA', 'INTERNAÇÃO EM COMUNIDADE TERAPÊUTICA'),
    ('RETIRADA DE DOCUMENTOS-IML', 'RETIRADA DE DOCUMENTOS-IML'),
    ('CAPS-AD |||/CAPS-SAMAUMA', 'CAPS-AD |||/CAPS-SAMAUMA'),
    ('OUTROS', 'OUTROS'),
)

c_remuneracao = (
    ('Empregado', 'Empregado'),
    ('Desempregado', 'Desempregado'),
    ('Trabalhador Rural', 'Trabalhador Rural'),
    ('Autônomo', 'Autônomo'),
    ('Funcionario Publico', 'Funcionario Publico'),
    ('Aposentado', 'Aposentado'),
    ('Pensionista', 'Pensionista'),
    ('Afastado/INSS', 'Afastado/INSS'),
    ('Do lar', 'Do lar'),
    ('Estudante', 'Estudante'),
)

c_renda_invidual = (
    ('MENOS DE UM SALARIO MINIMO', 'Menos de um salario minimo'),
    ('1 SALARIO MINIMO', '1 salario minimo'),
    ('2 A 3 SALARIOS MINIMOS', '2 a 3 salarios minimos'),
    ('MAIS DE 4 SALARIOS MINIMOS', 'Mais de 4 salarios minimos'),
    ('RECEBO BOLSA FAMILIA', 'Recebo bolsa familia'),
    ('DEPENDO FINANCEIRAMENTE DE OUTRAS PESSOAS', 'Dependo financeiramente de outras pessoas'),
)

c_estado = (
    ('Acre', 'AC'),    
    ('Alagoas', 'AL'),    
    ('Amapá', 'AP'),    
    ('Amazonas', 'AM'),    
    ('Bahia', 'BA'),    
    ('Ceará', 'CE'),    
    ('Distrito Federal', 'DF'),    
    ('Espírito Santo', 'ES'),    
    ('Goiás', 'GO'),    
    ('Maranhão', 'MA'),    
    ('Mato Grosso', 'MT'),    
    ('Mato Grosso do Sul', 'MS'),    
    ('Minas Gerais', 'MG'),    
    ('Pará', 'PA'),    
    ('Paraíba', 'PB'),    
    ('Paraná', 'PR'),    
    ('Pernambuco', 'PE'),    
    ('Piauí', 'PI'),    
    ('Rio de Janeiro', 'RJ'),    
    ('Rio Grande do Norte', 'RN'),    
    ('Rio Grande do Sul', 'RS'),    
    ('Rondônia', 'RO'),    
    ('Roraima', 'RR'),    
    ('Santa Catarina', 'SC'),    
    ('São Paulo', 'SP'),    
    ('Sergipe', 'SE'),    
    ('Tocantins', 'TO'),    
)

c_moradia_situacao = (
    ('PROPIA', 'Propia'),
    ('ALUGADO', 'Alugado'),
    ('CEDIDO', 'Cedido'),
    ('OCUPACAO', 'Ocupação'),
    ('IRREGULAR', 'Irregular'),
    ('SITUACAO DE RUA', 'Situação de rua'),
)

c_moradia_tipo = (
    ('ALVENARIA', 'Alvenaria'),
    ('MADEIRA', 'Madeira'),
    ('MISTA', 'Mista'),
)

c_escolaridade = (
    ('SELECIONE', 'Selecione'),
    ('NAO ESCOLARIZADO', 'Não escolarizado'),
    ('FUNDAMENTAL INCOMPLETO', 'Fundamental incompleto'),
    ('FUNDAMENTAL COMPLETO', 'Fundamental completo'),
    ('MEDIO INCOMPLETO', 'Médio Incompleto'),
    ('MEDIO COMPLETO', 'Médio Completo'),
    ('SUPERIOR INCOMPLETO', 'Superior Incompleto'),
    ('SUPERIOR COMPLETO', 'Superior Completo'),
    ('POS GRADUAÇÃO', 'Pós-Graduação'),
    ('MESTRADO', 'Mestrado'),
    ('DOUTORADO', 'Doutorado'),
    ('POS-DOUTORADO', 'Pós Doutorado'),
    ('NÃO DETERMINADO', 'Não determinado'),
)

c_estado_civil = (
    ('','Selecione'),
    ('SOLTEIRO', 'Solteiro'),
    ('CASADO', 'Casado'),
    ('UNIAO ESTAVEL', 'União Estavel'),
    ('SEPARADO', 'Separado'),
    ('DIVORCIADO', 'Divorciado'),
    ('VIUVO', 'Viúvo'),
)

c_medida_cumprimento = (
    ('', 'Selecione'),
    ('COMPARECIMENTO BIMESTRAL', 'COMPARECIMENTO BIMESTRAL'),
    ('COMPARECIMENTO MENSAL', 'COMPARECIMENTO MENSAL'),
    ('COMPARECIMENTO QUINZENAL', 'COMPARECIMENTO QUINZENAL'),
    ('COMPARECIMENTO SEMANAL', 'COMPARECIMENTO SEMANAL'),
    ('COMPARECIMENTO TRIMESTRAL', 'COMPARECIMENTO TRIMESTRAL'),
    ('GRUPO REFLEXIVO', 'GRUPO REFLEXIVO'),
    ('PSC', 'PSC'),
)

c_tip_penal = (
    ('', 'Selecione'),
    ('VIOLENCIA DOMESTICA', 'VIOLÊNCIA DOMÉSTICA'),
    ('FURTO', 'FURTO'),
    ('CRIME AMBIENTAL', 'CRIME AMBIENTAL'),
    ('RACISMO', 'RACISMO'),
    ('TRANSITO', 'TRÂNSITO'),
    ('CRIME DE DROGAS', 'CRIME DE DROGAS'),
    ('OUTROS CRIMES', 'OUTROS CRIMES'),
    ('LESAO CORPORAL', 'LESÃO CORPORAL'),
    ('CRIME DE ARMA', 'CRIME DE ARMA'),
    ('ESTELIONATO', 'ESTELIONATO'),
)

c_motivo_saida = (
    ('NAO DEFINIDO', 'NÃO DEFINIDO'),
    ('CUMPRIMENTO INTEGRAL', 'CUMPRIMENTO INTEGRAL'),
    ('DESCUMPRIMENTO', 'DESCUMPRIMENTO'),
    ('PRISAO', 'PRISÃO'),
    ('OUTRO', 'OUTRO'),
)









