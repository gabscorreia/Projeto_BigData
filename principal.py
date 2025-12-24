import pandas as pd # Manipulação de dataframes
from sklearn.ensemble import RandomForestClassifier # Classificador com base em arvores de decisao
# Métricas de avaliação para modelos de classificação (acurácia, precisão, recall, F1, matriz de confusão)
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.utils import shuffle # Embaralha os dados
from sklearn.datasets import load_iris
# train_test_split divide o conjunto de dados
from sklearn.model_selection import train_test_split, learning_curve
from itertools import product
import seaborn as sns # estilização de grafico
import matplotlib.pyplot as plt # Visualização de dados em gráficos
import numpy as np # Cálculos númericos

# 1. Lendo os arquivos CSV
caminho = './datasets/' # Variável que define o caminho até a pasta contendo os datasets que serão utilizados
combinado = pd.read_csv(caminho+'output.csv', encoding='latin-1', sep=";") # Lê o arquivo com os dados de entrada e guarda na variavel

ultima_coluna = combinado.iloc[:, -2]
# Análise dos dados
print("Mediana da taxa de morbidade:", ultima_coluna.median())
print("Média da taxa de morbidade:", ultima_coluna.mean())
print("Máxima da taxa de morbidade:", ultima_coluna.max())
print("Mínima da taxa de morbidade:", ultima_coluna.min())
print("Desvio padrão da taxa de morbidade:", ultima_coluna.std())
print("Moda da taxa de morbidade:", ultima_coluna.mode())

combinado = shuffle(combinado) # embaralha os dados

# Essa função divide o dataframe em 3 partes
def split_dataframe(df, proportions=[0.5, 0.25, 0.25]): # 50% treino, 25% validação, 25% teste
    df = shuffle(df)
    n = len(df) # Número total de linhas do dataframe
    n1 = int(n * proportions[0]) # Tamanho de df1
    n2 = int(n * proportions[1]) # Tamanho de df2
    df1 = df[:n1] # Parte de Treinamento
    df2 = df[n1:n1+n2] # Parte de Validação
    df3 = df[n1+n2:] # Parte de Teste
    return df1, df2, df3

# Grupo de subconjunto de dados reservados para fins específicos
train_df, val_df, test_df = split_dataframe(combinado)
# 'train_df' = para o Treinamento
# 'val_df' = para a Validação
# 'test_df' = para o Teste Final

X_train = train_df.iloc[:, :-2]
y_train = train_df.iloc[:, -1]

X_val = val_df.iloc[:, :-2]
y_val = val_df.iloc[:, -1]

X_test = test_df.iloc[:, :-2]
y_test = test_df.iloc[:, -1]

# As variáveis começadas em X_: train, val, test; São os dados de entrada (features), de todas as colunas menos as duas últimas ([:-2])
# As variáveis começadas em y_: train, val, test; São os Rótulos (classes para previsão), que estão na última coluna (-1)

clf = RandomForestClassifier() # Algoritmo classificador Random Forest
clf.fit(X_train, y_train) # Treina o modelo com os dados de entrada (X_train) e os rótulos (y_train)

# Labels das classes
class_names = ['1', '2', '3', '4']

val_preds = clf.predict(X_val) # Predições feitas pelo modelo nos dados de validação
print(accuracy_score(y_val, val_preds)) # Acurácia do modelo
print(classification_report(y_val, val_preds)) # Métricas detalhadas (precisão, recall, f1-score)
print(confusion_matrix(y_val, val_preds)) # Matriz de Confusão entre as classes reais e previstas

cm = confusion_matrix(y_val, val_preds) # Armazena a Matriz de Confusão

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names) # Desenha um mapa de calor da Matriz de Confusão
plt.xlabel('Predição') # nome do eixo x
plt.ylabel('Real') # nome do eixo y
plt.title('Mapa de Calor da Matriz  de Confusão (Validação)') # titulo
plt.show() # mostra grafico

test_preds = clf.predict(X_test) # Predição do modelo nos dados de teste
print(accuracy_score(y_test, test_preds))
print(classification_report(y_test, test_preds))
print(confusion_matrix(y_test, test_preds))

cm = confusion_matrix(y_test, test_preds)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predição')
plt.ylabel('Real')
plt.title('Mapa de Calor da Matriz  de Confusão (Teste)')
plt.show()


feature_names = { # Catalogação das variaveis (ordem das variáveis passadas para o modelo)
        "populacao_2": "População 2 meses antes",
        "populacao_1": "População 1 mês antes",
        "populacao_atual": "População",
        "cobertura_ocorrencia_2": "Cobertura por Ocorrência 2 meses antes",
        "cobertura_ocorrencia_1": "Cobertura por Ocorrência 1 mês antes",
        "cobertura_ocorrencia_atual": "Cobertura por Ocorrência",
        "cobertura_residencia_2": "Cobertura por Residência 2 meses antes",
        "cobertura_residencia_1": "Cobertura por Residência 1 mês antes",
        "cobertura_residencia_atual": "Cobertura por Residência",
        "doses_recorrencia_2": "Doses por Recorrência 2 meses antes",
        "doses_recorrencia_1": "Doses por Recorrência 1 mês antes",
        "doses_recorrencia_atual": "Doses por Recorrência",
        "doses_residencia_2": "Doses por Residência 2 meses antes",
        "doses_residencia_1": "Doses por Residência 1 mês antes",
        "doses_residencia_atual": "Doses por Residência",
        "amazonia": "Amazônia Legal",
        "faixa_fronteira": "Faixa Fronteira",
        "zona_fronteira": "Zona Fronteira",
        "semiarido": "Semiárido",
        "pobreza": "Pobreza",
        "cor_branca_2": "Internações de brancos 2 meses antes",
        "cor_branca_1": "Internações de brancos 1 mês antes",
        #"cor_branca_atual": "Internações de brancos",
        "cor_preta_2": "Internações de pretos 2 meses antes",
        "cor_preta_1": "Internações de pretos 1 mês antes",
        #"cor_preta_atual": "Internações de pretos",
        "cor_parda_2": "Internações de pardos 2 meses antes",
        "cor_parda_1": "Internações de pardos 1 mês antes",
        #"cor_parda_atual": "Internações de pardos",
        "cor_amarela_2": "Internações de amarelos 2 meses antes",
        "cor_amarela_1": "Internações de amarelos 1 mês antes",
        #"cor_amarela_atual": "Internações de amarelos",
        "cor_indigena_2": "Internações de indigenas 2 meses antes",
        "cor_indigena_1": "Internações de indigenas 1 mês antes",
        #"cor_indigena_atual": "Internações de indigenas"
        #"sexo_masculino_2": "Internações do sexo masculino 2 meses antes",
        #"sexo_masculino_1": "Internações do sexo masculino 1 mês antes",
        #"sexo_masculino_atual": "Internações do sexo masculino",
        #"sexo_feminino_2": "Internações do sexo feminino 2 meses antes",
        #"sexo_feminino_1": "Internações do sexo feminino 1 mês antes",
        #"sexo_feminino_atual": "Internações do sexo feminino",
        "faixa_menor_1_2": "Internações de menores de 1 ano 2 meses antes",
        "faixa_menor_1_1": "Internações de menores de 1 ano 1 mês antes",
        #"faixa_menor_1_atual": "Internações de menores de 1 ano",
        "faixa_1_a_4_2": "Internações de 1 a 4 anos 2 meses antes",
        "faixa_1_a_4_1": "Internações de 1 a 4 anos 1 mês antes",
        #"faixa_1_a_4_atual": "Internações de 1 a 4 anos",
        "faixa_5_a_9_2": "Internações de 5 a 9 anos 2 meses antes",
        "faixa_5_a_9_1": "Internações de 5 a 9 anos 1 mês antes",
        #"faixa_5_a_9_atual": "Internações de 5 a 9 anos",
        "faixa_10_a_14_2": "Internações de 10 a 14 anos 2 meses antes",
        "faixa_10_a_14_1": "Internações de 10 a 14 anos 1 mês antes",
        #"faixa_10_a_14_atual": "Internações de 10 a 14 anos
        "faixa_15_a_19_2": "Internações de 15 a 19 anos 2 meses antes",
        "faixa_15_a_19_1": "Internações de 15 a 19 anos 1 mês antes",
        #"faixa_15_a_19_atual": "Internações de 15 a 19 anos",
        "faixa_20_a_24_2": "Internações de 20 a 24 anos 2 meses antes",
        "faixa_20_a_24_1": "Internações de 20 a 24 anos 1 mês antes",
        #"faixa_20_a_24_atual": "Internações de 20 a 24 anos
        "faixa_25_a_29_2": "Internações de 25 a 29 anos 2 meses antes",
        "faixa_25_a_29_1": "Internações de 25 a 29 anos 1 mês antes",
        #"faixa_25_a_29_atual": "Internações de 25 a 29 anos",
        "faixa_30_a_34_2": "Internações de 30 a 34 anos 2 meses antes",
        "faixa_30_a_34_1": "Internações de 30 a 34 anos 1 mês antes",
        #"faixa_30_a_34_atual": "Internações de 30 a 34 anos
        "faixa_35_a_39_2": "Internações de 35 a 39 anos 2 meses antes",
        "faixa_35_a_39_1": "Internações de 35 a 39 anos 1 mês antes",
        #"faixa_35_a_39_atual": "Internações de 35 a 39 anos",
        "faixa_40_a_44_2": "Internações de 40 a 44 anos 2 meses antes",
        "faixa_40_a_44_1": "Internações de 40 a 44 anos 1 mês antes",
        #"faixa_40_a_44_atual": "Internações de 40 a 44 anos",
        "faixa_45_a_49_2": "Internações de 45 a 49 anos 2 meses antes",
        "faixa_45_a_49_1": "Internações de 45 a 49 anos 1 mês antes",
        #"faixa_45_a_49_atual": "Internações de 45 a 49 anos",
        "faixa_50_a_54_2": "Internações de 50 a 54 anos 2 meses antes",
        "faixa_50_a_54_1": "Internações de 50 a 54 anos 1 mês antes",
        #"faixa_50_a_54_atual": "Internações de 50 a 54 anos",
        "faixa_55_a_59_2": "Internações de 55 a 59 anos 2 meses antes",
        "faixa_55_a_59_1": "Internações de 55 a 59 anos 1 mês antes",
        #"faixa_55_a_59_atual": "Internações de 55 a 59 anos",
        "faixa_60_a_64_2": "Internações de 60 a 64 anos 2 meses antes",
        "faixa_60_a_64_1": "Internações de 60 a 64 anos 1 mês antes",
        #"faixa_60_a_64_atual": "Internações de 60 a 64 anos
        "faixa_65_a_69_2": "Internações de 65 a 69 anos 2 meses antes",
        "faixa_65_a_69_1": "Internações de 65 a 69 anos 1 mês antes",
        #"faixa_65_a_69_atual": "Internações de 65 a 69 anos",
        "faixa_70_a_74_2": "Internações de 70 a 74 anos 2 meses antes",
        "faixa_70_a_74_1": "Internações de 70 a 74 anos 1 mês antes",
        #"faixa_70_a_74_atual": "Internações de 70 a 74 anos",
        "faixa_75_a_79_2": "Internações de 75 a 79 anos 2 meses antes",
        "faixa_75_a_79_1": "Internações de 75 a 79 anos 1 mês antes",
        #"faixa_75_a_79_atual": "Internações de 75 a 79 anos",
        "faixa_80_mais_2": "Internações de 80 anos ou mais 2 meses antes",
        "faixa_80_mais_1": "Internações de 80 anos ou mais 1 mês antes",
        #"faixa_80_mais_atual": "Internações de 80 anos ou mais",
        "leitos_2": "Leitos 2 meses antes",
        "leitos_1": "Leitos 1 mês antes",
        "leitos_atual": "Leitos",
        "nascimentos_ocorrencia": "Nascimentos por ocorrência",
        "nascimentos_residencia": "Nascimentos por residência",
        "taxa_analfabetismo": "Taxa de Analfabetismo",
        "escolaridade_fundamental_1": "Escolaridade - Fundamental 1 Incompleto",
        "escolaridade_fundamental_2": "Escolaridade - Fundamental 2 Incompleto",
        "escolaridade_fundamental_2_mais": "Escolaridade - Fundamental 2 Completo",
        "escolaridade_nao_determinada": "Escolaridade - Não Determinada",
        "renda_media": "Renda Média per capita",
        "taxa_desemprego": "Taxa de Desemprego",
        "taxa_trabalho_infantil": "Taxa de Trabalho Infantil",
        "pib_per_capita": "PIB per capita",
        "pib": "PIB",
        "abastecimento_agua": "Residências com Abastecimento de água",
        "instalacoes_sanitarias": "Residências com Instalações Sanitárias",
        "coleta_lixo": "Residências com Coleta de Lixo",
        "obitos_ocorrencia": "Obitos por ocorrência",
        "obitos_residencia": "Obitos por residência",
        #"qtd_casos_2": "Quantidade de casos 2 meses antes",
        #"qtd_casos_1": "Quantidade de casos 1 mês antes",
        #"internacoes_2": "Classificação da internação 2 meses antes",
        #"internacoes_1": "Classificação da internação 1 mês antes",
        #"taxa_morbidade": "Taxa de Morbidade",
        #"internacoes": "Classificação da internação"
    }


print(len(feature_names)) # Quantidade de variáveis

feature_names = list(feature_names.values()) # Vira lista
importances = clf.feature_importances_ # Importância de cada variável na predição do modelo
forest_importances = pd.Series(importances, index=feature_names) # Importância por nome de variável

forest_importances.sort_values().plot(kind='barh', figsize=(8, 20)) # Gráfico de barras horizontal organizado pela importância da variável
plt.title('Importância das Variáveis') # Título
plt.xlabel('Importância') # Nome do eixo x
plt.show() # Mostra

sns.histplot(test_preds, kde=True) # Distribuição da confiança das previsões (histograma)
plt.title('Distribuição da Confiança das Previsões')
plt.xlabel('Probabilidade Máxima')
plt.ylabel('Frequência')
plt.show()