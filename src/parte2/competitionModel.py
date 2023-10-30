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
