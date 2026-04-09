from shiny import App, ui, reactive, render
from seir_model.seir_simulator import SEIRSimulator
from seir_model.visualizer_seir import VisualizerSEIR

class SEIRShinyApp:
    def __init__(self):
        self.sim = None

    def build_ui(self):
        return ui.page_fluid(
            ui.h2("SEIR Model Simulator"),
            ui.input_slider("N", "Population size", min=100, max=1000, value=500),
            ui.input_slider("I0", "Initial infected fraction", min=0.01, max=0.2, value=0.01),
            ui.input_slider("beta", "Infection rate β", min=0.0, max=1.0, value=0.3),
            ui.input_slider("sigma", "Exposed → Infected rate σ", min=0.0, max=1.0, value=0.2),
            ui.input_slider("mu", "Recovery rate μ", min=0.0, max=1.0, value=0.1),
            ui.output_ui("plot_ui")
        )

    def build_server(self, input, output, session):
        @reactive.Calc
        def run_sim():
            self.sim = SEIRSimulator(
                N=input.N(),
                I0=input.I0(),
                beta=input.beta(),
                sigma=input.sigma(),
                mu=input.mu(),
                t_max=200
            )
            return self.sim.run()

        @output
        @render.ui
        def plot_ui():
            history = run_sim()
            viz = VisualizerSEIR(history, title="SEIR Dynamics")
            return ui.HTML(viz.plot_html())  # render as HTML
        

seir_app = SEIRShinyApp()
app = App(seir_app.build_ui(), seir_app.build_server)