class Repository:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repository, cls).__new__(cls)
            cls._instance._tickers_info = []
            cls._instance._ranking = []
            cls._instance._fundamentus = []
        return cls._instance

    def set_tickers_data(self, tickersData):
        self._tickers_info = tickersData
    
    def set_ranking(self, tickersData):
        self._ranking = tickersData

     
    def set_fundamentus(self, fundamentus):
        self._fundamentus = fundamentus
    
    @property
    def tickers(self):
        return self._tickers_info

    @property
    def ranking(self):
        return self._ranking

    @property
    def fundamentus(self):
        return self._fundamentus

