class DataProcessor:
    def __init__(self, df):
        self.df = df

    def clean(self):
        df = self.df

        # rename columns
        df = df.rename(columns={
            'TIME': 'state',
            'TIME.1': 'energy_type'
        })

        # remove first row
        df = df.iloc[1:, :].reset_index(drop=True)

        # fix country names
        df = df.replace([
            'European Union - 27 countries (from 2020)',
            'Bosnia and Herzegovina',
            'North Macedonia',
            'T?rkiye',
            'United Kingdom'
        ], [
            'total_EU',
            'Bosnia_Herzegovina',
            'North_Macedonia',
            'Turkey',
            'United_Kingdom'
        ])

        # lowercase
        df['state'] = df['state'].str.lower()
        df['energy_type'] = df['energy_type'].str.lower()

        self.df = df
        return df

    def summary(self):
        return self.df.describe()