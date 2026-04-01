from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.h2("Hello Shiny 👋"),
    ui.input_slider("n", "Choose a number:", 0, 100, 50),
    ui.output_text("txt")
)

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"You selected: {input.n()}"

app = App(app_ui, server)