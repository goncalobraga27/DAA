import pandas as pd

df = pd.read_csv('../../../datasets/parte1/newcastle.csv')

df['location'] = "Newcastle"

df.to_csv('../../../datasets/parte1/newcastle_cleaned.csv', index=False)
