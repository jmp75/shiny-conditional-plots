from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.panel_title("Hello Shiny!"),
    ui.input_radio_buttons(
        id="station_id_rb",
        label=None,
        choices=["123456", "999999"],
        inline=True,
    ),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):

    _current_location_rv = reactive.value(None)

    @reactive.effect
    @reactive.event(input.station_id_rb)
    def update_selected_station():
        selected_station = input.station_id_rb()
        _current_location_rv.set(selected_station)

    @render.text
    def txt():
        location = _current_location_rv.get()
        msg = f"Currently selected: {location}" if location else "<not selected>"
        return msg


app = App(app_ui, server)
