import matplotlib.pyplot as plt
import io
import base64

class Visualizer:
    def __init__(self, df, title="Energy Analysis in EU"):
        self.df = df
        self.title = title

    def plot(self):

        df = self.df

        # filter EU total
        df = df[df["state"] == "total_eu"]

        # detect year columns automatically
        year_cols = [c for c in df.columns if c.isdigit()]

        # convert to numeric
        df[year_cols] = df[year_cols].replace(",", ".", regex=True)
        df[year_cols] = df[year_cols].astype(float)

        # plot energy types over time
        plt.figure(figsize=(12,6))

        for energy in df["energy_type"].unique():
            row = df[df["energy_type"] == energy][year_cols].T
            plt.plot(year_cols, row.values.flatten(), label=energy)

        plt.title(self.title)
        plt.xlabel("Year")
        plt.ylabel("Energy consumption")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    def to_html(self):
        buf = io.BytesIO()
        plt.figure(figsize=(10,5))
        self.df.groupby("energy_type").size().plot(kind="bar")
        plt.title(self.title)
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{img_str}" width="100%"/>'