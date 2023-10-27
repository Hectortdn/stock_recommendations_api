import fundamentus
from utils.index import get_all_commodities_tickers


def get_df_fundamentus_papel():
    commodities_tickers = get_all_commodities_tickers()
    fundamentus_papel  = fundamentus.get_papel(commodities_tickers)

    return fundamentus_papel
