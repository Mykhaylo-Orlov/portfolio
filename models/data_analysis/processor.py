import numpy as np
import pandas as pd
import warnings
warnings.simplefilter("ignore", pd.errors.SettingWithCopyWarning)

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def clean(self):

        df = self.df.copy()


        # 1. Rename columns
        
        df = df.rename(columns={
            "TIME": "state",
            "TIME.1": "energy_type"
        })

        
        # 2. Remove metadata row safely
        
        df = df.iloc[1:].reset_index(drop=True)

        
        # 3. Standardize text
        
        df["state"] = df["state"].astype(str).str.lower().str.strip()
        df["energy_type"] = df["energy_type"].astype(str).str.lower().str.strip()

        df = df.replace({
            "european union - 27 countries (from 2020)": "total_eu",
            "bosnia and herzegovina": "bosnia_herzegovina",
            "north macedonia": "north_macedonia",
            "t?rkiye": "turkey",
            "united kingdom": "united_kingdom"
        })

        
        # 4. Remove invalid labels
        
        df = df[~df["state"].isin(["nan", ":", "special value"])]

        
        # 5. Detect numeric columns (years)
        
        year_cols = [c for c in df.columns if str(c).isdigit()]

        
        # 6. Convert to numeric safely
        
        df[year_cols] = (
            df[year_cols]
            .replace({":": np.nan, ";": np.nan, "nan": np.nan})
            .replace(",", ".", regex=True)
            .apply(pd.to_numeric, errors="coerce")
        )

        
        # 7. Final cleanup
        
        df = df.dropna(how="all", subset=year_cols).reset_index(drop=True)

        self.df = df
        return df


    def summary(self):
        return self.df.describe()