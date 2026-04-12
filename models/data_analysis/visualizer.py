import matplotlib.pyplot as plt
import io
import base64

class Visualizer:
    def __init__(self, df, title="Energy Analysis"):
        self.df = df
        self.title = title

    def plot(self):
        # keep only EU total or one country (example: EU-27 Total)
        df = self.df[self.df["GEO"] == "European Union - 27 countries (from 2020)"]

        # convert wide → long format (years into rows)
        years = [str(y) for y in range(1990, 2023)]

        df_long = df.melt(
            id_vars=["energy_type"],
            value_vars=years,
            var_name="year",
            value_name="value"
        )

        df_long["year"] = df_long["year"].astype(int)
        df_long["value"] = df_long["value"].astype(str).str.replace(",", ".").astype(float)

        plt.figure(figsize=(12,6))

        for energy in df_long["energy_type"].unique():
            subset = df_long[df_long["energy_type"] == energy]
            plt.plot(subset["year"], subset["value"], label=energy)

        plt.title(self.title)
        plt.xlabel("Year")
        plt.ylabel("Energy consumption (ktoe)")
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