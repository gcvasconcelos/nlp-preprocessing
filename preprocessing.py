# %%
import pandas as pd
import re
from unidecode import unidecode
# %%
example_df = pd.read_csv('example.csv')
# %%
def standardize_dataframe(df, text_column, target_column):
    df[text_column] = df[text_column].str.lower()
    df[text_column] = df[text_column].apply(unidecode)

    df[target_column] = df[target_column].astype(str)
    df[target_column] = df[target_column].str.upper()

    df.columns = [str(col).upper().strip() for col in df.columns]
    print(df.info())


standardize_dataframe(example_df, 'xProd', 'NCM')
