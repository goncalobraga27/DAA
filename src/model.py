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

# Leitura do dataset dataset.csv 
df = pd.read_csv('../datasets/dataset.csv')

# Remoção das colunas 'Unnamed: 0' e 'id', que conforme se encontra descrito no Kaggle não pertence aos dados do dataset
for col in df.columns:
    if 'Unnamed: 0' in col:
        del df[col]
    if 'id' in col:
        del df[col]

# Inspeção das colunas do dataset 
# print(df.columns)

# Inspeção do número total de linhas e colunas do dataset 
# print(df.shape)

# Inspeção do tipo das colunas do data
print(df.info())

################################################################################ Análise de dados existentes no dataset ###############################################################################
# Análise dos dados - Tendência Central 
print(df.describe())
# Verificação dos missing values no dataset 
print(df.isna().any())
# Análise de duplicados 
print("Este dataset possui os seguintes valores duplicados: %s"%str(df.duplicated().sum()))


################################################################################# Criação do modelo de classificação da coluna - Satisfaction ###########################################################

# Como para os modelos de classificação não podemos ter dados categóricos, iremos retirar os mesmos 
x = df.drop(['Gender','Customer Type','Type of Travel','Class','satisfaction'], axis = 1)
# Iremos colocar o que queremos prever no eixo do y 
y = df['satisfaction'].to_frame()

# Criação do x de teste e treino, tal como, o y de treino e de teste 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2021)

# Criação da árvore de classificação para o modelo de decisão (A seed tem de ser igual à de cima)
clf = DecisionTreeClassifier(criterion = 'gini',max_depth=10,random_state=2021)   # O criterion e o max_depth podem ser alterados 

# Para fazer k-Fold Cross validation
scores = cross_val_score(clf,x,y,cv=10)

print("Os scores são estes:")
print(scores)
print("RESULT: %0.2f accuracy with a standart deviation of %0.2f" % (scores.mean(), scores.std()))

# Treino do modelo de aprendizagem 
clf.fit(x_train, y_train)

# Previsões do modelo de aprendizagem tendo como base o modelo de aprendizagem treinado mais os dados de teste 
predict = clf.predict(x_test)

# Criação da matriz de confusão 
confusion_matrix = confusion_matrix(y_test, predict)

print ("Matriz de confusão :")
print(confusion_matrix)


# Cálculo da accuracy do modelo de aprendizagem
accuracy = accuracy_score(y_test, predict)

print("A accuracy deste modelo é de :")
print(str(accuracy*100)+"%")


# Cálculo da precisão do modelo de aprendizagem
precision = precision_score(y_test, predict, pos_label='neutral or dissatisfied') # Isto aqui pode ser assim, ou só com satisfied

print("A precisão deste modelo é de :")
print(precision)


# Cálculo da recall do modelo de aprendizagem
recall = recall_score(y_test, predict, pos_label='neutral or dissatisfied') # Isto aqui pode ser assim, ou só com satisfied

print("A recall deste modelo é de :")
print(recall)


# Cálculo da f1_macro do modelo de aprendizagem 
f1_macro = f1_score(y_test,predict,average="macro")

print("A f1_macro deste modelo é de :")
print(f1_macro)

