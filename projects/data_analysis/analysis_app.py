from data_loader import DataLoader
from processor import DataProcessor
from visualizer import Visualizer

class AnalysisApp:
    def __init__(self, path):
        self.loader = DataLoader(path)
        self.df = None

    def run(self):
        # load
        self.df = self.loader.load()

        # process
        processor = DataProcessor(self.df)
        self.df = processor.clean()

        # visualize
        viz = Visualizer(self.df)
        viz.plot()

        return self.df