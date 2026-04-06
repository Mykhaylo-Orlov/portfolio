import matplotlib.pyplot as plt
import io
import base64

class Visualizer:
    """Handles plotting of SIR simulation results."""

    def __init__(self, history, title="Simulation"):
        """
        history: list or array of infected fraction over time
        """
        self.history = history
        self.title = title

    def plot_infection(self):
        """Plot fraction of infected over time."""
        plt.figure(figsize=(10,5))
        plt.plot(self.history, color='red', lw=2)
        plt.xlabel("Time")
        plt.ylabel("Fraction Infected")
        plt.title(self.title)
        plt.grid(True)
        plt.show()

    def save_plot(self, filename="plot.png"):
        """Save the plot as an image file."""
        plt.figure(figsize=(10,5))
        plt.plot(self.history, color='red', lw=2)
        plt.xlabel("Time")
        plt.ylabel("Fraction Infected")
        plt.title(self.title)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)

    def to_html(self):
        """Return the matplotlib figure as HTML image string for Shiny"""
        buf = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.plot(self.history, color='red', lw=2)
        plt.xlabel("Time")
        plt.ylabel("Fraction Infected")
        plt.title(self.title)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{img_str}" width="100%"/>'