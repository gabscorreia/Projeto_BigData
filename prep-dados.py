import pandas as pd #manipulação de arquivos .csv
import openpyxl #manipulação de arquivos .xlsx
#from google.colab import drive # OPCIONAL - usado para importar dados do google drive para ser utilizado no google colab
# drive.mount('/content/drive', True)

caminho = './datasets/' #diretorio principal, onde todos os datasets estarão

dfIbge = pd.read_csv(caminho+'municipios.csv', encoding='latin-1', sep=";") # Primeiro dataset, o de municípios, contendo todos os municípios do Brasil, de acordo com o IBGE


municipios = {} # Inicialização do dicionário de municípios
flags = {} # Inicialização do dicionário de flags (acabou send reutilizado para dados gerais do município)
for row in dfIbge.itertuples(): # Percorre cada uma das linhas do dataset
  codIbge = str(getattr(row, '_2'))[:-1]  # Remove o último dígito do código do município
  if codIbge not in flags: #Insere os dados do município na flag (o if é mais uma precaução)
    flags[codIbge] = { # (-1 indefinido, 0 nao, 1 sim)
      "amazonia": -1, # Catalogado como amazônia legal
      "faixa_fronteira": -1, # Catalogado como faixa de fronteira
      "zona_fronteira": -1, # Catalogado como zona de fronteira
      "semiarido": -1, # Catalogado como clima semiárido
      "pobreza": -1, # Catalogado como município de extrema pobreza
      "nascimentos_ocorrencia": 0, # Quantidade de nascimentos por ocorrência
      "nascimentos_residencia": 0, # quantidade de nascimentos por residência
      "taxa_analfabetismo": 0.0, # Taxa de analfabetismo do municipio
      "escolaridade_fundamental_1": 0.0, # Quantidade de pessoas que não terminaram o fund 1
      "escolaridade_fundamental_2": 0.0, # Quantidade de pessoas que não terminaram fund 2
      "escolaridade_fundamental_2_mais": 0.0, # Quantidade de pessoas que terminaram fund 2 e continuaram estudando
      "escolaridade_nao_determinada": 0.0, # dados sobre escolaridade indeterminados
      "renda_media": 0.0, # renda média por residencia
      "taxa_desemprego": 0.0, # taxa de desemprego
      "taxa_trabalho_infantil": 0.0, # taxa de trabalho infantil
      "pib_per_capita": 0.0, # produto interno bruto per capita
      "pib": 0.0, # produto interno bruto do municipio
      "abastecimento_agua": 0, # quantas pessoas tem abastecimento de agua
      "instalacoes_sanitarias": 0, # quantas pessoas tem instalações sanitarias
      "coleta_lixo": 0, # quantas pessoas constaram que tem coleta de lixo
      "obitos_residencia": 0, # obitos na cidade de residencia dos mortos
      "obitos_ocorrencia": 0 # obitos na cidade de ocorrencia da morte
    }
  for mes in range(1,13): # Cria um dicionário, onde cada município aparece 12 vezes, um para cada mês
    municipios[codIbge+'-'+str(mes)] = {
      #"cidade": getattr(row, '_3'),
      #"mes": mes,
      "populacao": 0, #população
      "cobertura_ocorrencia": 0.0, #cobertura vacinal por ocorrência
      "cobertura_residencia": 0.0, #cobertura vacinal por residência
      "doses_ocorrencia": 0, # doses aplicadas por ocorrencia
      "doses_residencia": 0, # doses aplicadas por residencia
      "amazonia": -1, # flags ja explicadas
      "faixa_fronteira": -1,
      "zona_fronteira": -1,
      "semiarido": -1,
      "pobreza": -1,
      "cor_branca": 0, # quantidade de internações de pessoas brancas
      "cor_preta": 0, # quantidade de internações de pessoas pretas
      "cor_parda": 0, # quantidade de internações de pessoas pardas
      "cor_amarela": 0, # quantidade de internações de pessoas amarelas
      "cor_indigena": 0, # quantidade de internações de pessoas indigenas
      "sexo_masculino": 0, # quantidade de internações do sexo masculino
      "sexo_feminino": 0, # quantidade de internações do sexo feminino
      "faixa_menor_1" : 0, # quantidade de internações de bebes com menos de 1 ano
      "faixa_1_a_4" : 0, # quantidade de internações de 1 a 4 anos de idade
      "faixa_5_a_9" : 0,
      "faixa_10_a_14" : 0,
      "faixa_15_a_19" : 0,
      "faixa_20_a_24" : 0,
      "faixa_25_a_29" : 0,
      "faixa_30_a_34" : 0,
      "faixa_35_a_39" : 0,
      "faixa_40_a_44" : 0,
      "faixa_45_a_49" : 0,
      "faixa_50_a_54" : 0,
      "faixa_55_a_59" : 0,
      "faixa_60_a_64" : 0,
      "faixa_65_a_69" : 0,
      "faixa_70_a_74" : 0,
      "faixa_75_a_79" : 0,
      "faixa_80_mais" : 0,
      "leitos":  0, # quantidade de camas hospitalares disponibilizadas pelo municipio
      "qtd_casos": 0, # quantidade de internações
      "taxa_morbidade": 0.0, # quantidade de internações dividida pela população
      "internacoes": 4, # classificação
    }

nascimentosOcorrencia = pd.read_csv(caminho+'nascidos_ocorrencia.csv', encoding='latin-1', sep=";", skiprows=4) # quantidade de nascimentos por ocorrencia
chegouTotal = False # determina se chegou à linha de total de nascimentos (dataset acabou)
for row in nascimentosOcorrencia.itertuples(): # itera pelas linhas do dataset
  codIbge = row[1].split(' ')[0] # armazena codigo do ibge na variavel (e tira nome do municipio)
  if (codIbge == "Total"): # se a linha n for um codigo, mas sim uma string total
    chegouTotal = True # realmente chegou ao total
  if chegouTotal:
    continue # para de iterar pelas linhas
  flags[codIbge]['nascimentos_ocorrencia'] = int(row[2]) # adiciona a quantidade de nascimentos por ocorrencia do municipio nas flags


nascimentosResidencia = pd.read_csv(caminho+'nascidos_residencia.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in nascimentosResidencia.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['nascimentos_residencia'] = int(row[2])

taxaAnalfabetismo = pd.read_csv(caminho+'taxa_analfabetismo.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in taxaAnalfabetismo.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['taxa_analfabetismo'] = float(taxa)

taxaEscolaridade = pd.read_csv(caminho+'taxa_escolaridade.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in taxaEscolaridade.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['escolaridade_fundamental_1'] = float(taxa)
  taxa  = row[3].replace(",", ".")
  flags[codIbge]['escolaridade_fundamental_2'] = float(taxa)
  taxa  = row[4].replace(",", ".")
  flags[codIbge]['escolaridade_fundamental_2_mais'] = float(taxa)
  taxa  = row[5].replace(",", ".")
  flags[codIbge]['escolaridade_nao_determinada'] = float(taxa)

rendaMedia = pd.read_csv(caminho+'renda_media.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in rendaMedia.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  renda  = row[2].replace(",", ".")
  flags[codIbge]['renda_media'] = float(renda)

taxaDesemprego = pd.read_csv(caminho+'taxa_desemprego.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in taxaDesemprego.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['taxa_desemprego'] = float(taxa)

taxaTrabalhoInfantil = pd.read_csv(caminho+'taxa_trabalho_infantil.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in taxaTrabalhoInfantil.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['taxa_trabalho_infantil'] = float(taxa)

pibPerCapita = pd.read_csv(caminho+'pib_per_capita.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in pibPerCapita.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['pib_per_capita'] = float(taxa)

pib = pd.read_csv(caminho+'pib.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in pib.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  taxa  = row[2].replace(",", ".")
  flags[codIbge]['pib'] = float(taxa)

abastecimentoAgua = pd.read_csv(caminho+'abastecimento_agua.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in abastecimentoAgua.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['abastecimento_agua'] = int(row[2])

instalacoesSanitarias = pd.read_csv(caminho+'instalacoes_sanitarias.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in instalacoesSanitarias.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['instalacoes_sanitarias'] = int(row[2])

coletaLixo = pd.read_csv(caminho+'coleta_lixo.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in coletaLixo.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['coleta_lixo'] = int(row[2])

obitosOcorrencia = pd.read_csv(caminho+'obitos_ocorrencia.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in obitosOcorrencia.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['obitos_ocorrencia'] = int(row[2])

obitosResidencia = pd.read_csv(caminho+'obitos_residencia.csv', encoding='latin-1', sep=";", skiprows=4)
chegouTotal = False
for row in obitosResidencia.itertuples():
  codIbge = row[1].split(' ')[0]
  if (codIbge == "Total"):
    chegouTotal = True
  if chegouTotal:
    continue
  flags[codIbge]['obitos_residencia'] = int(row[2])

# Lê a planilha de dados por local de ocorrência
ocorrencias = openpyxl.load_workbook(caminho+"ocorrencia.xlsx") # nao fez skip rows (cabeçalho ainda existe)
sheet = ocorrencias.worksheets[0] # apenas primeira aba

# Atualiza os dados de cobertura e doses com base no local de ocorrência
i = 0
for row in sheet:
  i += 1
  if i <= 4:
      continue  # Ignora os cabeçalhos
  colunaInicial = 2 # indice do dado do mês
  for mes in range(1,13):
    cobertura = row[colunaInicial].value
    cobertura = round(cobertura , 2) # arredonda valor
    codMes = row[1].value+'-'+str(mes) # codigo do municipio
    municipios[codMes]["cobertura_ocorrencia"] = cobertura # cobertura por ocorrencia do municipio
    municipios[codMes]["doses_ocorrencia"] = row[colunaInicial+1].value # doses por ocorrencia do municipio
    municipios[codMes]["populacao"] = row[colunaInicial+2].value # população do municipio
    colunaInicial += 3

# Lê a planilha de dados por local de residência
residencia = openpyxl.load_workbook(caminho+"residencia.xlsx")
sheet = residencia.worksheets[0]

# Atualização dos dados de cobertura e doses com base na residência
i = 0
for row in sheet:
  i += 1
  if i <= 4:
      continue  # Ignora os cabeçalhos
  colunaInicial = 2
  for mes in range(1,13):
    cobertura = row[colunaInicial].value
    cobertura = round(cobertura , 2)
    codMes = row[1].value+'-'+str(mes)
    municipios[codMes]["cobertura_residencia"] = cobertura
    municipios[codMes]["doses_residencia"] = row[colunaInicial+1].value
    colunaInicial += 3
    # nao precisamos adicionar o dado da população pois ele ja existe

for mes in range(1, 13): # todos os dados disponiveis naquele mes
  ##### INÍCIO LEITURA DAS INTERNAÇÕES #####
  df = pd.read_csv(f'{caminho}internacoes/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)

  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0] # codigo do municipio
    if (codIbge == "Total"):
      chegouTotal = True
    if chegouTotal:
      continue
    codIbge = codIbge + '-' + str(mes) # codigo do municipio - mes
    internacoes = int(getattr(row, 'Internações'))
    if internacoes:
      municipios[codIbge]["qtd_casos"] = internacoes

    if(municipios[codIbge]["populacao"] > 0): # se a populaçao do municipio > 0, está garantido que nao haverá divisao por 0
      taxaMorbidade = internacoes / (municipios[codIbge]["populacao"] * 1000) # internações divididas pela população bruta
    else:
      taxaMorbidade = 0.0

    municipios[codIbge]["taxa_morbidade"] = taxaMorbidade

    if taxaMorbidade > 0.0006: # se um municipio tem taxa de morbidade acima do dobro da media, classe 1 (mais grave)
      resultado = 1
    elif taxaMorbidade > 0.0003: # media da taxa de morbidade (meio termo)
      resultado = 2
    elif taxaMorbidade > 0.00015: # entre a media e metade da media
      resultado = 3
    else:
      resultado = 4 # menor que a metade da media

    #municipios[codIbge]["taxa_morbidade"] = taxaMorbidade
    municipios[codIbge]["internacoes"] = resultado
  ##### FIM LEITURA DAS INTERNAÇÕES #####
  ##### INÍCIO LEITURA DOS LEITOS#####
  df = pd.read_csv(f'{caminho}leitos/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    codIbge = codIbge + '-' + str(mes)
    municipios[codIbge]["leitos"] = int(row[2])
  ##### FIM LEITURA DOS LEITOS #####
  ##### INÍCIO LEITURA DE COR #####
  df = pd.read_csv(f'{caminho}cor/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    codIbge = codIbge + '-' + str(mes)
    if row[2] != '-':
      municipios[codIbge]["cor_branca"] = int(row[2])
    if row[3] != '-':
      municipios[codIbge]["cor_preta"] = int(row[3])
    if row[4] != '-':
      municipios[codIbge]["cor_parda"] = int(row[4])
    if row[5] != '-':
      municipios[codIbge]["cor_amarela"] = int(row[5])
    if row[6] != '-':
      municipios[codIbge]["cor_indigena"] = int(row[6])
  ##### FIM LEITURA DE COR #####
  ##### INÍCIO LEITURA DA AMAZONIA (SIM) #####
  df = pd.read_csv(f'{caminho}amazonia/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["amazonia"] = 1
  ##### FIM LEITURA DA AMAZONIA (SIM) #####
  ##### INÍCIO LEITURA DA AMAZONIA (NÃO) #####
  df = pd.read_csv(f'{caminho}amazonia/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["amazonia"] = 0
  ##### FIM LEITURA DA AMAZONIA (NÃO) #####
  ##### INÍCIO LEITURA DA FAIXA FRONTEIRA (SIM) #####
  df = pd.read_csv(f'{caminho}faixa_fronteira/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["faixa_fronteira"] = 1
  ##### FIM LEITURA DA FAIXA FRONTEIRA (SIM) #####
  ##### INÍCIO LEITURA DA FAIXA FRONTEIRA (NÃO) #####
  df = pd.read_csv(f'{caminho}faixa_fronteira/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["faixa_fronteira"] = 0
  ##### FIM LEITURA DA FAIXA FRONTEIRA (NÃO) #####
  ##### INÍCIO LEITURA DA ZONA FRONTEIRA (SIM) #####
  df = pd.read_csv(f'{caminho}zona_fronteira/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["zona_fronteira"] = 1
  ##### FIM LEITURA DA ZONA FRONTEIRA (SIM) #####
  ##### INÍCIO LEITURA DA ZONA FRONTEIRA (NÃO) #####
  df = pd.read_csv(f'{caminho}zona_fronteira/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["zona_fronteira"] = 0
  ##### FIM LEITURA DA ZONA FRONTEIRA (NÃO) #####
  ##### INÍCIO LEITURA DE SEMIARIDOS (SIM) #####
  df = pd.read_csv(f'{caminho}semiarido/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["semiarido"] = 1
  ##### FIM LEITURA DE SEMIARIDOS (SIM) #####
  ##### INÍCIO LEITURA DE SEMIARIDOS (NÃO) #####
  df = pd.read_csv(f'{caminho}semiarido/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["semiarido"] = 0
  ##### FIM LEITURA DE SEMIARIDOS (NÃO) #####
    ##### INÍCIO LEITURA DE SEMIARIDOS (SIM) #####
  df = pd.read_csv(f'{caminho}semiarido/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["semiarido"] = 1
  ##### FIM LEITURA DE SEMIARIDOS (SIM) #####
  ##### INÍCIO LEITURA DE SEMIARIDOS (NÃO) #####
  df = pd.read_csv(f'{caminho}semiarido/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=5)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["semiarido"] = 0
  ##### FIM LEITURA DE SEMIARIDOS (NÃO) #####
  ##### INÍCIO LEITURA DE POBREZA (SIM) #####
  df = pd.read_csv(f'{caminho}pobreza/sim/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["pobreza"] = 1
  ##### FIM LEITURA DE POBREZA (SIM) #####
  ##### INÍCIO LEITURA DE POBREZA (NÃO) #####
  df = pd.read_csv(f'{caminho}pobreza/nao/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    flags[codIbge]["pobreza"] = 0
  ##### FIM LEITURA DE POBREZA (NÃO) #####
  ##### INÍCIO LEITURA DO SEXO #####
  df = pd.read_csv(f'{caminho}sexo/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
        chegouTotal = True
    if chegouTotal:
      continue
    codIbge = codIbge + '-' + str(mes)
    if row[2] != '-':
      municipios[codIbge]["sexo_masculino"] = int(row[2])
    if row[3] != '-':
      municipios[codIbge]["sexo_feminino"] = int(row[3])
  ##### FIM LEITURA DO SEXO #####
  ##### INÍCIO LEITURA DAS FAIXAS ETÁRIAS #####
  df = pd.read_csv(f'{caminho}faixas_etarias/{mes}.csv', encoding='latin-1', sep=";", skiprows=4)
  chegouTotal = False
  for row in df.itertuples():
    codIbge = row[1].split(' ')[0]
    if (codIbge == "Total"):
      chegouTotal = True
    if chegouTotal:
      continue
    codIbge = codIbge + '-' + str(mes)
    if row[2] != '-':
      municipios[codIbge]["faixa_menor_1"] = int(row[2])
    if row[3] != '-':
      municipios[codIbge]["faixa_1_a_4"] = int(row[3])
    if row[4] != '-':
      municipios[codIbge]["faixa_5_a_9"] = int(row[4])
    if row[5] != '-':
      municipios[codIbge]["faixa_10_a_14"] = int(row[5])
    if row[6] != '-':
      municipios[codIbge]["faixa_15_a_19"] = int(row[6])
    if row[7] != '-':
      municipios[codIbge]["faixa_20_a_24"] = int(row[7])
    if row[8] != '-':
      municipios[codIbge]["faixa_25_a_29"] = int(row[8])
    if row[9] != '-':
      municipios[codIbge]["faixa_30_a_34"] = int(row[9])
    if row[10] != '-':
      municipios[codIbge]["faixa_35_a_39"] = int(row[10])
    if row[11] != '-':
      municipios[codIbge]["faixa_40_a_44"] = int(row[11])
    if row[12] != '-':
      municipios[codIbge]["faixa_45_a_49"] = int(row[12])
    if row[13] != '-':
      municipios[codIbge]["faixa_50_a_54"] = int(row[13])
    if row[14] != '-':
      municipios[codIbge]["faixa_55_a_59"] = int(row[14])
    if row[15] != '-':
      municipios[codIbge]["faixa_60_a_64"] = int(row[15])
    if row[16] != '-':
      municipios[codIbge]["faixa_65_a_69"] = int(row[16])
    if row[17] != '-':
      municipios[codIbge]["faixa_70_a_74"] = int(row[17])
    if row[18] != '-':
      municipios[codIbge]["faixa_75_a_79"] = int(row[18])
    if row[19] != '-':
      municipios[codIbge]["faixa_80_mais"] = int(row[19])
  ##### FIM LEITURA DAS FAIXAS ETÁRIAS #####

for mes in range(1, 13): # dados das flags nos dados gerais dos municipios por mes
  for codIbge in flags:
    municipios[codIbge+'-'+str(mes)]["amazonia"] = flags[codIbge]["amazonia"]
    municipios[codIbge+'-'+str(mes)]["faixa_fronteira"] = flags[codIbge]["faixa_fronteira"]
    municipios[codIbge+'-'+str(mes)]["zona_fronteira"] = flags[codIbge]["zona_fronteira"]
    municipios[codIbge+'-'+str(mes)]["semiarido"] = flags[codIbge]["semiarido"]
    municipios[codIbge+'-'+str(mes)]["pobreza"] = flags[codIbge]["pobreza"]
    municipios[codIbge+'-'+str(mes)]["nascimentos_ocorrencia"] = flags[codIbge]["nascimentos_ocorrencia"]
    municipios[codIbge+'-'+str(mes)]["nascimentos_residencia"] = flags[codIbge]["nascimentos_residencia"]
    municipios[codIbge+'-'+str(mes)]["taxa_analfabetismo"] = flags[codIbge]["taxa_analfabetismo"]
    municipios[codIbge+'-'+str(mes)]["escolaridade_fundamental_1"] = flags[codIbge]["escolaridade_fundamental_1"]
    municipios[codIbge+'-'+str(mes)]["escolaridade_fundamental_2"] = flags[codIbge]["escolaridade_fundamental_2"]
    municipios[codIbge+'-'+str(mes)]["escolaridade_fundamental_2_mais"] = flags[codIbge]["escolaridade_fundamental_2_mais"]
    municipios[codIbge+'-'+str(mes)]["escolaridade_nao_determinada"] = flags[codIbge]["escolaridade_nao_determinada"]
    municipios[codIbge+'-'+str(mes)]["renda_media"] = flags[codIbge]["renda_media"]
    municipios[codIbge+'-'+str(mes)]["taxa_desemprego"] = flags[codIbge]["taxa_desemprego"]
    municipios[codIbge+'-'+str(mes)]["taxa_trabalho_infantil"] = flags[codIbge]["taxa_trabalho_infantil"]
    municipios[codIbge+'-'+str(mes)]["pib_per_capita"] = flags[codIbge]["pib_per_capita"]
    municipios[codIbge+'-'+str(mes)]["pib"] = flags[codIbge]["pib"]
    municipios[codIbge+'-'+str(mes)]["abastecimento_agua"] = flags[codIbge]["abastecimento_agua"]
    municipios[codIbge+'-'+str(mes)]["instalacoes_sanitarias"] = flags[codIbge]["instalacoes_sanitarias"]
    municipios[codIbge+'-'+str(mes)]["coleta_lixo"] = flags[codIbge]["coleta_lixo"]
    municipios[codIbge+'-'+str(mes)]["obitos_ocorrencia"] = flags[codIbge]["obitos_ocorrencia"]
    municipios[codIbge+'-'+str(mes)]["obitos_residencia"] = flags[codIbge]["obitos_residencia"]

dadoTratado = {} # alterações no resultado final
for mes in range(3,13): # março a dezembro
  for codIbge in flags:
    dadoMaisAntigo = municipios[codIbge+'-'+str(mes-2)] # dado de dois meses atras
    dadoAntigo = municipios[codIbge+'-'+str(mes-1)] # dado de um mes atras
    dadoAtual = municipios[codIbge+'-'+str(mes)] # dado do mes atual
    #if dadoAtual["qtd_casos"] == 0 and dadoAntigo["qtd_casos"] == 0 and dadoMaisAntigo["qtd_casos"] == 0:
      #continue
    dadoTratado[codIbge+'-'+str(mes)] = {
        "populacao_2": dadoMaisAntigo["populacao"],
        "populacao_1": dadoAntigo["populacao"],
        "populacao_atual": dadoAtual["populacao"],
        "cobertura_ocorrencia_2": dadoMaisAntigo["cobertura_ocorrencia"],
        "cobertura_ocorrencia_1": dadoAntigo["cobertura_ocorrencia"],
        "cobertura_ocorrencia_atual": dadoAtual["cobertura_ocorrencia"],
        "cobertura_residencia_2": dadoMaisAntigo["cobertura_residencia"],
        "cobertura_residencia_1": dadoAntigo["cobertura_residencia"],
        "cobertura_residencia_atual": dadoAtual["cobertura_residencia"],
        "doses_recorrencia_2": dadoMaisAntigo["doses_ocorrencia"],
        "doses_recorrencia_1": dadoAntigo["doses_ocorrencia"],
        "doses_recorrencia_atual": dadoAtual["doses_ocorrencia"],
        "doses_residencia_2": dadoMaisAntigo["doses_residencia"],
        "doses_residencia_1": dadoAntigo["doses_residencia"],
        "doses_residencia_atual": dadoAtual["doses_residencia"],
        "amazonia": dadoAtual["amazonia"],
        "faixa_fronteira": dadoAtual["faixa_fronteira"],
        "zona_fronteira": dadoAtual["zona_fronteira"],
        "semiarido": dadoAtual["semiarido"],
        "pobreza": dadoAtual["pobreza"],
        "cor_branca_2": dadoMaisAntigo["cor_branca"],
        "cor_branca_1": dadoAntigo["cor_branca"],
        #"cor_branca_atual": dadoAtual["cor_branca"],
        "cor_preta_2": dadoMaisAntigo["cor_preta"],
        "cor_preta_1": dadoAntigo["cor_preta"],
        #"cor_preta_atual": dadoAtual["cor_preta"],
        "cor_parda_2": dadoMaisAntigo["cor_parda"],
        "cor_parda_1": dadoAntigo["cor_parda"],
        #"cor_parda_atual": dadoAtual["cor_parda"],
        "cor_amarela_2": dadoMaisAntigo["cor_amarela"],
        "cor_amarela_1": dadoAntigo["cor_amarela"],
        #"cor_amarela_atual": dadoAtual["cor_amarela"],
        "cor_indigena_2": dadoMaisAntigo["cor_indigena"],
        "cor_indigena_1": dadoAntigo["cor_indigena"],
        #"cor_indigena_atual": dadoAtual["cor_indigena"],
        #"sexo_masculino_2": dadoMaisAntigo["sexo_masculino"],
        #"sexo_masculino_1": dadoAntigo["sexo_masculino"],
        #"sexo_masculino_atual": dadoAtual["sexo_masculino"],
        #"sexo_feminino_2": dadoMaisAntigo["sexo_feminino"],
        #"sexo_feminino_1": dadoAntigo["sexo_feminino"],
        #"sexo_feminino_atual": dadoAtual["sexo_feminino"],
        "faixa_menor_1_2": dadoMaisAntigo["faixa_menor_1"],
        "faixa_menor_1_1": dadoAntigo["faixa_menor_1"],
        #"faixa_menor_1_atual": dadoAtual["faixa_menor_1"],
        "faixa_1_a_4_2": dadoMaisAntigo["faixa_1_a_4"],
        "faixa_1_a_4_1": dadoAntigo["faixa_1_a_4"],
        #"faixa_1_a_4_atual": dadoAtual["faixa_1_a_4"],
        "faixa_5_a_9_2": dadoMaisAntigo["faixa_5_a_9"],
        "faixa_5_a_9_1": dadoAntigo["faixa_5_a_9"],
        #"faixa_5_a_9_atual": dadoAtual["faixa_5_a_9"],
        "faixa_10_a_14_2": dadoMaisAntigo["faixa_10_a_14"],
        "faixa_10_a_14_1": dadoAntigo["faixa_10_a_14"],
        #"faixa_10_a_14_atual": dadoAtual["faixa_10_a_14"],
        "faixa_15_a_19_2": dadoMaisAntigo["faixa_15_a_19"],
        "faixa_15_a_19_1": dadoAntigo["faixa_15_a_19"],
        #"faixa_15_a_19_atual": dadoAtual["faixa_15_a_19"],
        "faixa_20_a_24_2": dadoMaisAntigo["faixa_20_a_24"],
        "faixa_20_a_24_1": dadoAntigo["faixa_20_a_24"],
        #"faixa_20_a_24_atual": dadoAtual["faixa_20_a_24"],
        "faixa_25_a_29_2": dadoMaisAntigo["faixa_25_a_29"],
        "faixa_25_a_29_1": dadoAntigo["faixa_25_a_29"],
        #"faixa_25_a_29_atual": dadoAtual["faixa_25_a_29"],
        "faixa_30_a_34_2": dadoMaisAntigo["faixa_30_a_34"],
        "faixa_30_a_34_1": dadoAntigo["faixa_30_a_34"],
        #"faixa_30_a_34_atual": dadoAtual["faixa_30_a_34"],
        "faixa_35_a_39_2": dadoMaisAntigo["faixa_35_a_39"],
        "faixa_35_a_39_1": dadoAntigo["faixa_35_a_39"],
        #"faixa_35_a_39_atual": dadoAtual["faixa_35_a_39"],
        "faixa_40_a_44_2": dadoMaisAntigo["faixa_40_a_44"],
        "faixa_40_a_44_1": dadoAntigo["faixa_40_a_44"],
        #"faixa_40_a_44_atual": dadoAtual["faixa_40_a_44"],
        "faixa_45_a_49_2": dadoMaisAntigo["faixa_45_a_49"],
        "faixa_45_a_49_1": dadoAntigo["faixa_45_a_49"],
        #"faixa_45_a_49_atual": dadoAtual["faixa_45_a_49"],
        "faixa_50_a_54_2": dadoMaisAntigo["faixa_50_a_54"],
        "faixa_50_a_54_1": dadoAntigo["faixa_50_a_54"],
        #"faixa_50_a_54_atual": dadoAtual["faixa_50_a_54"],
        "faixa_55_a_59_2": dadoMaisAntigo["faixa_55_a_59"],
        "faixa_55_a_59_1": dadoAntigo["faixa_55_a_59"],
        #"faixa_55_a_59_atual": dadoAtual["faixa_55_a_59"],
        "faixa_60_a_64_2": dadoMaisAntigo["faixa_60_a_64"],
        "faixa_60_a_64_1": dadoAntigo["faixa_60_a_64"],
        #"faixa_60_a_64_atual": dadoAtual["faixa_60_a_64"],
        "faixa_65_a_69_2": dadoMaisAntigo["faixa_65_a_69"],
        "faixa_65_a_69_1": dadoAntigo["faixa_65_a_69"],
        #"faixa_65_a_69_atual": dadoAtual["faixa_65_a_69"],
        "faixa_70_a_74_2": dadoMaisAntigo["faixa_70_a_74"],
        "faixa_70_a_74_1": dadoAntigo["faixa_70_a_74"],
        #"faixa_70_a_74_atual": dadoAtual["faixa_70_a_74"],
        "faixa_75_a_79_2": dadoMaisAntigo["faixa_75_a_79"],
        "faixa_75_a_79_1": dadoAntigo["faixa_75_a_79"],
        #"faixa_75_a_79_atual": dadoAtual["faixa_75_a_79"],
        "faixa_80_mais_2": dadoMaisAntigo["faixa_80_mais"],
        "faixa_80_mais_1": dadoAntigo["faixa_80_mais"],
        #"faixa_80_mais_atual": dadoAtual["faixa_80_mais"],
        "leitos_2": dadoMaisAntigo["leitos"],
        "leitos_1": dadoAntigo["leitos"],
        "leitos_atual": dadoAtual["leitos"],
        "nascimentos_ocorrencia": dadoAtual["nascimentos_ocorrencia"],
        "nascimentos_residencia": dadoAtual["nascimentos_residencia"],
        "taxa_analfabetismo": dadoAtual["taxa_analfabetismo"],
        "escolaridade_fundamental_1": dadoAtual["escolaridade_fundamental_1"],
        "escolaridade_fundamental_2": dadoAtual["escolaridade_fundamental_2"],
        "escolaridade_fundamental_2_mais": dadoAtual["escolaridade_fundamental_2_mais"],
        "escolaridade_nao_determinada": dadoAtual["escolaridade_nao_determinada"],
        "renda_media": dadoAtual["renda_media"],
        "taxa_desemprego": dadoAtual["taxa_desemprego"],
        "taxa_trabalho_infantil": dadoAtual["taxa_trabalho_infantil"],
        "pib_per_capita": dadoAtual["pib_per_capita"],
        "pib": dadoAtual["pib"],
        "abastecimento_agua": dadoAtual["abastecimento_agua"],
        "instalacoes_sanitarias": dadoAtual["instalacoes_sanitarias"],
        "coleta_lixo": dadoAtual["coleta_lixo"],
        "obitos_ocorrencia": dadoAtual["obitos_ocorrencia"],
        "obitos_residencia": dadoAtual["obitos_residencia"],
        #"qtd_casos_2": dadoMaisAntigo["qtd_casos"],
        #"qtd_casos_1": dadoAntigo["qtd_casos"],
        #"internacoes_2": dadoMaisAntigo["internacoes"],
        #"internacoes_1": dadoAntigo["internacoes"],
        "taxa_morbidade": dadoAtual["taxa_morbidade"], # utilizado para validações
        "internacoes": dadoAtual["internacoes"]
    }

# Converte o dicionário para o DataFrame e altera (municípios como linhas)
exportar = pd.DataFrame(dadoTratado)
df_transposed = exportar.T

# Salva os dados consolidade em um novo arquivo CSV
df_transposed.to_csv(caminho+'output.csv', index=False, sep=";", encoding="latin-1")

