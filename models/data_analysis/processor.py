import numpy as np
import pandas as pd

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def clean(self):

        df = self.df.rename(columns={'TIME': 'state', 'TIME.1': 'energy_type'})
        df = df.iloc[1:, :].reset_index(drop=True)
        df = df.copy()

        # -------------------------
        # 1. Standardize country names
        # -------------------------
        df = df.replace({
            'European Union - 27 countries (from 2020)': 'total_eu',
            'Bosnia and Herzegovina': 'bosnia_herzegovina',
            'North Macedonia': 'north_macedonia',
            'T?rkiye': 'turkey',
            'United Kingdom': 'united_kingdom'
        })

        # -------------------------
        # 2. Normalize text columns
        # -------------------------
        df['state'] = df['state'].astype(str).str.lower().str.strip()
        df['energy_type'] = df['energy_type'].astype(str).str.lower().str.strip()

        # -------------------------
        # 3. Remove invalid rows
        # -------------------------
        invalid_states = ['nan', ':', 'special value']
        df = df[~df['state'].isin(invalid_states)]

        # -------------------------
        # 4. Detect year columns safely
        # -------------------------
        year_cols = [c for c in df.columns if str(c).isdigit()]

        # -------------------------
        # 5. Clean numeric values (robust)
        # -------------------------
        for col in year_cols:
            df[col] = (
                df[col]
                .astype(str)
                .replace({':': np.nan, ';': np.nan, 'nan': np.nan})
                .str.replace(',', '.', regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # -------------------------
        # 6. Drop empty columns/rows
        # -------------------------
        df = df.dropna(how='all', subset=year_cols)
        df = df.dropna(axis=1, how='all')

        # optional: drop last row if it's garbage (safe version)
        df = df.reset_index(drop=True)

        self.df = df
        return df

    def summary(self):
        return self.df.describe(include='all')