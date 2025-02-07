"""
Purpose: Provide user interaction options for the Cars dataset.

 - Choose checkboxes when the options are independent of each other.
 - Choose radio buttons when a set of options are mutually exclusive.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

"""

from shiny import ui


def get_mtcars_inputs():
    return ui.panel_sidebar(
        ui.h2("Cars Interaction"),
        ui.tags.hr(),
        ui.input_slider(
            "MTCARS_MPG_RANGE",
            "Miles per Gallon (MPG)",
            min=10,
            max=35,
            value=[10, 35],
        ),
        ui.input_numeric("MTCARS_HP", "Gross Horsepower", value=335),
        ui.input_radio_buttons(
            "MTCARS_TRANS",
            "Transmission Type",
            {"a": "Automatic", "m": "Manual"},
            selected="a",
        ),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
