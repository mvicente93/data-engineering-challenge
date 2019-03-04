import pandas as pd 


class SMADataTransformer:

    def __init__(self, df):
        self.df = df

    def transform(self, params=[]):
        
        self.df = self._filter(params)

        return self._aggregate()

    def _filter(self, filters):
    
        boolean_filter = pd.Series([True] * len(self.df))
        for column, value in filters:
            boolean_filter &= (self.df[column] == value)
        
        return self.df[ boolean_filter ]

    def _aggregate(self):
        return self.df[['timestamp', 'duration']].set_index('timestamp')\
                                                 .resample('T')\
                                                 .agg([('events_count', 'count'), ('duration_sum', 'sum')])
    

