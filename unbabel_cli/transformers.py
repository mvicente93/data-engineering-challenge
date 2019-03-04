import pandas as pd 


class SMADataTransformer:

    def __init__(self, df):
        self.df = df

    def transform(self, params={}):
        
        columns = params.get('columns', [])
        filters = params.get('filters', [])

        if columns and filters and len(columns) == len(filters):
            self.df = self._filter(columns, filters)
        
        return self._aggregate()

    def _filter(self, columns, filters):
    
        boolean_filter = pd.Series([True] * len(self.df))
        for column, value in zip(columns, filters):
            boolean_filter &= (self.df[column] == value)
        
        return self.df[ boolean_filter ]

    def _aggregate(self):
        return self.df[['timestamp', 'duration']].set_index('timestamp')\
                                                 .resample('T')\
                                                 .agg([('events_count', 'count'), ('duration_sum', 'sum')])
    

