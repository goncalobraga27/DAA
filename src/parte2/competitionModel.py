import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


# O OBJETIVO DESTE MODELO É DE PREVER A quantidade de energia injectada na rede eléctrica QUE SE ENCONTRA NA COLUNA Injeção na rede (kWh) DO DATASET DE ENERGIA 

# Leitura dos datasets com dados relativos a 09/2021 - 12/2021
df_meteo = pd.read_csv("../../datasets/parte2/treino/meteo_202109-202112.csv")
df_energia = pd.read_csv("../../datasets/parte2/treino/energia_202109-202112.csv",na_filter=False)
############################################################################ Tratamento de dados do dataset df_meteo ###################################################
# Passagem da coluna dt_iso para as duas colunas Data e Hora para depois podermos dar merge dos dois datasets
df_meteo['dt_iso'] = pd.to_datetime(df_meteo['dt_iso'].str.replace(' UTC', ''), format='%Y-%m-%d %H:%M:%S %z')
df_meteo['Data'] = df_meteo['dt_iso'].dt.strftime('%Y-%m-%d')
df_meteo['Hora'] = df_meteo['dt_iso'].dt.strftime('%H')
df_meteo['Hora'] = df_meteo['Hora'].astype(int)
# Eliminar a coluna 'dt_iso' do dataset df_meteo pois os dados relevantes dessa coluna estão na nova coluna 'Data' e 'Hora' 
df_meteo = df_meteo.drop('dt_iso',axis = 1)
# Limpeza das colunas que não acrescentam muita informação relativa ao dataset  
valoresDif = df_meteo['city_name'].value_counts()
# print("Valores diferentes na coluna: "+ str(valoresDif)) # Como são todos os valores iguais a local, podemos simplesmente remover a coluna
df_meteo = df_meteo.drop('city_name', axis = 1)
df_meteo = df_meteo.drop('sea_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados
df_meteo = df_meteo.drop('grnd_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados
df_meteo = df_meteo.drop('dt', axis = 1) # Como os valores não acrescentam informação relevante para o conexto do problema podem ser retirados 

############################################################################# Tratamento de dados do dataset df_energia #################################################
# Alteração da coluna 'Hora' do dataset df_energia para o tipo int
df_energia['Hora'] = df_energia['Hora'].astype(int)
############################################################################# Junção dos datasets df_meteo e df_energia de 09/2021 - 12/2021 para a utilização de Random Forests ###########
# Podemos agora juntar os dois datasets pelas colunas 'Data' e 'Hora' presentes em ambos os datasets
df_2021= pd.merge(df_meteo, df_energia, on=['Data','Hora'], how='inner')



# Leitura dos datasets com dados relativos a 01/2022 - 12/2022
df_meteo = pd.read_csv("../../datasets/parte2/treino/meteo_202201-202212.csv")
df_energia = pd.read_csv("../../datasets/parte2/treino/energia_202201-202212.csv",na_filter=False)

df_meteo['dt_iso'] = pd.to_datetime(df_meteo['dt_iso'].str.replace(' UTC', ''), format='%Y-%m-%d %H:%M:%S %z')
df_meteo['Data'] = df_meteo['dt_iso'].dt.strftime('%Y-%m-%d')
df_meteo['Hora'] = df_meteo['dt_iso'].dt.strftime('%H')
df_meteo['Hora'] = df_meteo['Hora'].astype(int)
# Eliminar a coluna 'dt_iso' do dataset df_meteo pois os dados relevantes dessa coluna estão na nova coluna 'Data' e 'Hora' 
df_meteo = df_meteo.drop('dt_iso',axis = 1)
# Limpeza das colunas que não acrescentam muita informação relativa ao dataset  
valoresDif = df_meteo['city_name'].value_counts()
# print("Valores diferentes na coluna: "+ str(valoresDif)) # Como são todos os valores iguais a local, podemos simplesmente remover a coluna
df_meteo = df_meteo.drop('city_name', axis = 1)
df_meteo = df_meteo.drop('sea_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados
df_meteo = df_meteo.drop('grnd_level', axis = 1) # Como os valores são sempre NaN e não são úteis para o contexto do problema podem ser retirados
df_meteo = df_meteo.drop('dt', axis = 1) # Como os valores não acrescentam informação relevante para o conexto do problema podem ser retirados 

############################################################################# Tratamento de dados do dataset df_energia #################################################
# Alteração da coluna 'Hora' do dataset df_energia para o tipo int
df_energia['Hora'] = df_energia['Hora'].astype(int)

############################################################################# Junção dos datasets df_meteo e df_energia de 09/2021 - 12/2021 para a utilização de Random Forests ###########
# Podemos agora juntar os dois datasets pelas colunas 'Data' e 'Hora' presentes em ambos os datasets
df_2022= pd.merge(df_meteo, df_energia, on=['Data','Hora'], how='inner')


########################################################################### Junção dos datasets com informação de 2021 e 2022 ###########################################
# AQUI TEMOS O DATASET PRONTO PARA SUBMETER NA RANDOM FOREST 
df = pd.concat([df_2021,df_2022],ignore_index = True)
# Criação do label encoding para codificarmos a coluna weather_description
label_encoder = LabelEncoder()
df['weather_description_encoded'] = label_encoder.fit_transform(df['weather_description'])
df = df.drop('weather_description', axis = 1)
df = df.drop('Data', axis = 1)
# Temos de tratar aqui dos missing values existentes no df ......
media_Rain_1h = df['rain_1h'].mean()
df['rain_1h'].fillna(media_Rain_1h, inplace=True)
# Criação da variavel que queremos prever 
x = df.drop('Injeção na rede (kWh)', axis = 1)
y = df['Injeção na rede (kWh)']
# Divisão do dataset em treino e teste 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.204793028, random_state=42)
# Criação do modelo de random forest, com 100 árvores 
model = RandomForestClassifier(n_estimators=10000, random_state=42)
# Treino do modelo 
model.fit(x_train, y_train)
# Previsões do modelo 
y_pred = model.predict(x_test)

df_predicoes = pd.DataFrame({'Result': y_pred})
df_predicoes['RowId'] = range(1, len(y_pred) + 1)
df_predicoes = df_predicoes[['RowId', 'Result']]

df_predicoes.to_csv('../../datasets/parte2/teste/previsoes.csv', index=False)

