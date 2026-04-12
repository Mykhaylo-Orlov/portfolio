from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import io
import base64

class VisualizerBase(ABC):
    """Abstract base class for visualizers."""

    def __init__(self, history, title="Simulation"):
        self.history = history
        self.title = title

    @abstractmethod
    def plot(self):
        """Plot the simulation results."""
        pass

    @abstractmethod
    def to_html(self):
        """Return the plot as HTML (for Shiny/Quarto)."""
        pass


class VisualizerSIR(VisualizerBase):
    """Handles plotting of SIR simulation results."""

    def plot(self):
        plt.figure(figsize=(10,5))
        plt.plot(self.history, color='red', lw=2, label="Infected")
        plt.xlabel("Time")
        plt.ylabel("Fraction Infected")
        plt.title(self.title)
        plt.grid(True)
        plt.legend()
        plt.show()

    def to_html(self):
        buf = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.plot(self.history, color='red', lw=2, label="Infected")
        plt.xlabel("Time")
        plt.ylabel("Fraction Infected")
        plt.title(self.title)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{img_str}" width="100%"/>'

