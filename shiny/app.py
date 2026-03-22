from shiny import App, ui, render, reactive
import pandas as pd
import plotly.express as px

# sample data
df = pd.DataFrame({
    "x": range(1, 101),
    "y": [i**2 for i in range(1, 101)]
})

app_ui = ui.page_fluid(
    ui.h2("Shiny Python demo"),
    ui.input_slider("n", "Points to show", min=10, max=100, value=50),
    ui.output_plot("plot"),
    ui.output_text("summary")
)

def server(input, output, session):
    @reactive.Calc
    def df_filtered():
        n = input.n()
        return df.head(n)

    @output
    @render.plot
    def plot():
        d = df_filtered()
        fig = px.scatter(d, x="x", y="y", title=f"First {input.n()} points")
        return fig

    @output
    @render.text
    def summary():
        d = df_filtered()
        return f"Showing {len(d)} rows. y mean = {d['y'].mean():.2f}"

app = App(app_ui, server)