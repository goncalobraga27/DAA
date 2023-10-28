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
# print(df.info())

################################################################################ Análise de dados existentes no dataset ###############################################################################33
# Análise dos dados - Tendência Central 
print(df.describe())
# Verificação dos missing values no dataset 
print(df.isna().any())
# Análise de duplicados 
print(df.duplicated().sum())

