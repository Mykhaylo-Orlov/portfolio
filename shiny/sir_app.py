from shiny import App, ui, reactive, render
from projects.sir_model.sir_simulator import SIRSimulator
from projects.sir_model.visualizer import Visualizer

# UI layout
app_ui = ui.page_fluid(
    ui.h2("Interactive SIR Model"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("beta", "Infection rate (β):", min=0, max=1, step=0.05, value=0.2),
            ui.input_slider("mu", "Recovery rate (μ):", min=0, max=1, step=0.05, value=0.1),
            ui.input_slider("I0", "Initial infected fraction (I0):", min=0, max=0.1, step=0.01, value=0.01)
        ),
        ui.output_ui("plot_ui")
    )
)

# Server logic
def server(input, output, session):
    
    @reactive.Calc
    def history():
        sim = SIRSimulator(N=500, I0=input.I0(), beta=input.beta(), mu=input.mu(), t_max=200)
        return sim.run()
    
    @output
    @render.ui
    def plot_ui():
        hist = history()
        viz = Visualizer(hist, title=f"SIR: β={input.beta()}, μ={input.mu()}")
        # Return HTML of plot
        return ui.HTML(viz.to_html())  # We'll add `to_html` in Visualizer

# Initialize app
app = App(app_ui, server)