import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from sklearn.metrics import fbeta_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

# O OBJETIVO DESTE MODELO É DE PREVER A quantidade de energia injectada na rede eléctrica QUE SE ENCONTRA NA COLUNA Injeção na rede (kWh) DO DATASET DE ENERGIA 

# Leitura dos datasets com dados relativos a 09/2021 - 12/2021
df_meteo = pd.read_csv("../../datasets/parte2/treino/meteo_202109-202112.csv")
df_energia = pd.read_csv("../../datasets/parte2/treino/energia_202109-202112.csv")
############################################################################ Tratamento de dados do dataset df_meteo ###################################################
# Passagem da coluna dt_iso para as duas colunas Data e Hora para depois podermos dar merge dos dois datasets
df_meteo['dt_iso'] = pd.to_datetime(df_meteo['dt_iso'].str.replace(' UTC', ''), format='%Y-%m-%d %H:%M:%S %z')
df_meteo['Data'] = df_meteo['dt_iso'].dt.strftime('%Y-%m-%d')
df_meteo['Hora'] = df_meteo['dt_iso'].dt.strftime('%H')

# Eliminar a coluna 'dt_iso' do dataset df_meteo pois os dados relevantes dessa coluna estão na nova coluna 'Data' e 'Hora' 
for col in df_meteo.columns:
    if 'dt_iso' in col:
        del df_meteo[col]

# Limpeza das colunas que não acrescentam muita informação relativa ao dataset  
valoresDif = df_meteo['city_name'].value_counts()
print("Valores diferentes na coluna: "+ str(valoresDif)) # Como são todos os valores iguais a local, podemos simplesmente remover a coluna

df_meteo = df_meteo.drop('city_name', axis = 1)
df_meteo = df_meteo.drop('sea_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados
df_meteo = df_meteo.drop('grnd_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados

print(df_meteo.head())
############################################################################# Tratamento de dados do dataset df_energia #################################################
# Alteração da coluna 'Hora' do dataset df_energia para o tipo object 
df_energia['Hora'] = df_energia['Hora'].astype('object')

# Podemos agora juntar os dois datasets pelas colunas 'Data' e 'Hora' presentes em ambos os datasets
# df_2021= pd.merge(df_meteo, df_energia, on=['Data','Hora'], how='right')
