from typing import Any

import plotly.express as px
from shiny import App, module, reactive, render, ui
from shinywidgets import output_widget, render_widget

app_ui = ui.page_fluid(
    ui.panel_title("Hello Shiny!"),
    ui.input_radio_buttons(
        id="station_id_rb",
        label=None,
        choices=["123456", "999999", "abcdef", "None"],
        inline=True,
    ),
    ui.output_ui("toggled_controls"),
)

# Adapting https://www.appsilon.com/post/shiny-for-python-clean-design-for-dynamic-plot-management
@module.ui
def plot_ui(stock_ticker:str, location:str) -> ui.TagChild:
    return output_widget("plot")

@module.server
def plotly_stock_server(input, output, session, stock_ticker:str, location:str):
    @render_widget # https://shiny.posit.co/py/components/outputs/plot-plotly/
    def plot() -> Any:
        df = px.data.stocks()
        fig = px.line(df, x='date', y=stock_ticker, title=f"location: {location}")
        return fig

_current_location = None

def server(input, output, session):

    _current_location_rv = reactive.value(None)

    @reactive.effect
    @reactive.event(input.station_id_rb)
    def update_selected_station():
        global _current_location
        selected_station = input.station_id_rb()
        _current_location_rv.set(selected_station)
        _current_location = selected_station

    @render.ui
    def toggled_controls():
        global _current_location
        location = _current_location_rv.get()
        location = _current_location
        if location is None or location == "None":
            return ui.TagList(
                ui.output_text("location_unknown")
            )
        else:
            location=str(location)
            stock_tickers = ['GOOG','AAPL']
            for s in stock_tickers:
                plotly_stock_server(f"plot_{s}", s, location)
            tag_children=[plot_ui(f"plot_{s}", s, location) for s in stock_tickers]
            return ui.TagList(tag_children)
            # return ui.TagList(
            #     output_widget("first_graph"),
            #     output_widget("second_graph")
            # )

    # @render_widget
    # def first_graph():
    #     # Note: if one adds the following statement to the function body, then you get duplicated graph outputs
    #     # location = _current_location_rv.get()
    #     df = px.data.stocks()
    #     fig = px.line(df, x='date', y="GOOG")
    #     return fig

    # @render_widget
    # def second_graph():
    #     df = px.data.stocks()
    #     fig = px.line(df, x='date', y="AAPL")
    #     return fig

    @render.text
    def location_unknown(): return "location_unknown"
    @render.text
    def location_123456(): return "location is 123456"
    @render.text
    def location_999999(): return "location is 999999"
    @render.text
    def whats_that(): return "Unexpected location!"



app = App(app_ui, server)
