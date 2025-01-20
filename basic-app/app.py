from shiny import App, reactive, render, ui

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
                ui.output_text("location_known", "Location is None - no UI")
            )
        elif location == "123456":
            return ui.TagList(
                ui.output_text("location_123456", "hard coded control for 123456")
            )
        elif location == "999999":
            return ui.TagList(
                ui.output_text("location_999999", "hard coded control for 999999")
            )
        else:
            return ui.TagList(
                ui.output_text("whats_that", "Unexpected station ID")
            )


app = App(app_ui, server)
