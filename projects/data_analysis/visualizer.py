import matplotlib.pyplot as plt
import io
import base64

class Visualizer:
    def __init__(self, df, title="Energy Analysis"):
        self.df = df
        self.title = title

    def plot(self):
        plt.figure(figsize=(10,5))
        self.df.groupby("energy_type").size().plot(kind="bar")
        plt.title(self.title)
        plt.xlabel("Energy Type")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
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