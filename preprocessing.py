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
    df[target_column] = df[target_column].apply(unidecode)

    df.columns = [str(col).upper().strip() for col in df.columns]
    print(df.info())


standardize_dataframe(example_df, 'xProd', 'NCM')
# %%
def clean_text(df, text_column, regex_list = [], stopwords_list = []):
    if regex_list or stopwords_list:
        print('INFO - Início da limpeza do Texto (remoção de padrões por regex e remoção de stopwords)')
    else:
        print("ERRO - Lista de regex e de stopwords vazia!")
        return

    clean_text_column = text_column + '_LIMPO'
    df[clean_text_column] = df[text_column]

    subs_list = [
        *[re.compile(r) for r in regex_list],
        *[re.compile(rf"\b{sw}\b") for sw in stopwords_list]
    ]

    list_size = len(subs_list)
    for idx, sub in enumerate(subs_list):
        df[clean_text_column] = df[clean_text_column].str.replace(
            sub, ' '
        )
        print(f'INFO - Limpeza {idx+1}/{list_size} concluída!')

    df[clean_text_column] = df[clean_text_column].str.strip()

    print(f"INFO - Textos vazios após a limpeza: {(df[clean_text_column].values == '').sum()} ")
    print(df.head(10)[[text_column, clean_text_column]])

example_list = [
    r'[^a-z]+' # deixa apenas letras minusculas
    , r'\b\w{1,2}\b' # remover palavras e numeros com um ou dois caracteres
    , r"\s+" # Limpa espacos em branco (sempre deixar em último)
]

sw_list = [
    'joelho'
    , 'brita'
    , 'tudo'
    , 'korres'
]

clean_text(example_df, 'XPROD', example_list, sw_list)
# %%
def replace_target(df, target_column, replacements_dict):
    if replacements_dict:
        print('INFO - Início da substituição de termos da coluna de Target.')
    else:
        print('ERRO - Dicionário de termos de substituição vazio!')
        return

    clean_target_column = target_column + '_LIMPO'
    df[clean_target_column] = df[target_column]
    df[clean_target_column] = df[clean_target_column].astype(str)

    dict_size = len(replacements_dict)
    for idx, rep in enumerate(replacements_dict):
        df[clean_target_column] = df[clean_target_column].str.replace(
            rf"^{rep}$", replacements_dict[rep]
        )
        print(f'INFO - Substituição {idx+1}/{dict_size} concluída!')
    print(f"INFO - Número de classes original: {df[target_column].nunique()}")
    print(f"INFO - Número de classes pós substituição: {df[clean_target_column].nunique()}")
    print(df[clean_target_column].unique())

dict_example = {
    '39174090': 'a'
    , '69041000': 'b'
    , '49111090': 'a'
}

replace_target(example_df, 'NCM', dict_example)
