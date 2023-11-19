class Repository:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repository, cls).__new__(cls)
            cls._instance._ranking = []
            cls._instance._yfinance = None
            cls._instance._tickers_info = []
            cls._instance._fundamentus = None
        return cls._instance

    def set_tickers_data(self, tickersData):
        self._tickers_info = tickersData

    def set_ranking(self, ranking):
        self._ranking = ranking

    def set_fundamentus(self, fundamentus_data):
        self._fundamentus = fundamentus_data
    
    def set_yfinance(self, yfinance_data):
        self._yfinance = yfinance_data

    @property
    def tickers(self):
        return self._tickers_info

    @property
    def ranking(self):
        return self._ranking

    @property
    def fundamentus(self):
        return self._fundamentus


    @property
    def yfinance(self):
        return self._yfinance

