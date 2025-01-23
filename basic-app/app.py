import plotly.express as px
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget

app_ui = ui.page_fluid(
    ui.panel_title("Hello Shiny!"),
    ui.input_radio_buttons(
        id="station_id_rb",
        label=None,
        choices=["123456", "999999"],
        inline=True,
    ),
    ui.output_ui("toggled_controls"),
)


def server(input, output, session):

    _current_location_rv = reactive.value(None)

    @reactive.effect
    @reactive.event(input.station_id_rb)
    def update_selected_station():
        selected_station = input.station_id_rb()
        _current_location_rv.set(selected_station)

    @render.ui
    def toggled_controls():
        location = _current_location_rv.get()
        if location is None:
            return ui.TagList(
                ui.output_text("location_unknown")
            )
        else:
            return ui.TagList(
                output_widget("first_graph"),
                output_widget("second_graph")
            )

    @render_widget
    def first_graph():
        # Note: if one adds the following statement to the function body, then you get duplicated graph outputs
        # location = _current_location_rv.get()
        df = px.data.stocks()
        fig = px.line(df, x='date', y="GOOG")
        return fig

    @render_widget
    def second_graph():
        df = px.data.stocks()
        fig = px.line(df, x='date', y="AAPL")
        return fig

    @render.text
    def location_unknown(): return "location_unknown"
    @render.text
    def location_123456(): return "location is 123456"
    @render.text
    def location_999999(): return "location is 999999"
    @render.text
    def whats_that(): return "Unexpected location!"



app = App(app_ui, server)
