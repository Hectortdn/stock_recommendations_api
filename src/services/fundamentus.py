import fundamentus
import pandas as pd 
import requests
import yfinance as ys 
from bs4 import BeautifulSoup
from utils.index import perc_to_float_fundamentus, rename_cols_fundamentus

url = 'https://fundamentus.com.br/resultado.php'
hdr = {"User-Agent": "Mozzila/5.0"}


def get_fundamentus_result() -> pd.DataFrame:
    content = requests.get(url, headers=hdr)
    df = pd.read_html(content.text, decimal=",", thousands='.')[0]

      ## Fix: percent string
    df['Div.Yield']     = perc_to_float_fundamentus( df['Div.Yield']     )
    df['Mrg Ebit']      = perc_to_float_fundamentus( df['Mrg Ebit']      )
    df['Mrg. Líq.']     = perc_to_float_fundamentus( df['Mrg. Líq.']     )
    df['ROIC']          = perc_to_float_fundamentus( df['ROIC']          )
    df['ROE']           = perc_to_float_fundamentus( df['ROE']           )
    df['Cresc. Rec.5a'] = perc_to_float_fundamentus( df['Cresc. Rec.5a'] )

    ## index by 'Papel', instead of 'int'
    df.index = df['Papel']
    df.drop('Papel', axis='columns', inplace=True)
    df.sort_index(inplace=True)

    ## naming
    df.name = 'Fundamentus: HTML names'
    df.columns.name = 'Multiples'
    df.index.name = 'papel'

    df_rename = rename_cols_fundamentus(df)

    df = df_rename.drop_duplicates(keep='first')
    
    return df 
