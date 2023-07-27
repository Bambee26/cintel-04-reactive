""" 
Purpose: Provide reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

"""
import pathlib
from shiny import render, reactive
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
from shinywidgets import render_widget
import plotly.express as px

from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_mtcars_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    p = pathlib.Path(__file__).parent.joinpath("data").joinpath("mtcars.csv")
    # logger.info(f"Reading data from {p}")
    original_df = pd.read_csv(p)
    total_count = len(original_df)

    reactive_df = reactive.Value()

    @reactive.Effect
    @reactive.event(
        input.MTCARS_MPG_RANGE,
        input.MTCARS_HP,
        input.MTCARS_GEARS_3,
        input.MTCARS_GEARS_4,
        input.MTCARS_GEARS_5,
        input.MTCARS_TRANS,
    )
    def _():
        """Reactive effect to update the filtered dataframe when inputs change.
        This is the only way to set a reactive value (after initialization).
        It doesn't need a name, because no one calls it directly."""

        # logger.info("UI inputs changed. Updating penguins reactive df")

        df = original_df.copy()

        # MPG is a range
        input_range = input.MTCARS_MPG_RANGE()
        input_min = input_range[0]
        input_max = input_range[1]
        MPG_filter = (df["mpg"] >= input_min) & (
            df["mpg"] <= input_max
        )
        df = df[MPG_filter]

        # HP is a max number
        gross_hp_filter = df["hp"] <= input.MTCARS_HP()
        df = df[gross_hp_filter]

        # Gears is a list of checkboxes (a list of possible values)
        show_gears_list = []
        if input.MTCARS_GEARS_3():
            show_gears_list.append("3")
        if input.MTCARS_GEARS_4():
            show_gears_list.append("4")
        if input.MTCARS_GEARS_5():
            show_gears_list.append("5")
        show_gears_list = show_gears_list or ["3", "4", "5"]
        gears_filter = df["gear"].isin(show_gears_list)
        df = df[gears_filter]

        # Trans is a radio button
        input_trans = input.MTCARS_TRANS()
        trans_dict = {"a": "Automatic", "m": "Manual"}
        if input_trans != "a":
            trans_filter = df["trans"] == trans_dict[input_trans]
            df = df[trans_filter]

        # logger.debug(f"filtered cars df: {df}")
        reactive_df.set(df)


    @output
    @render.text
    def mtcars_record_count_string():
        filtered_df = reactive_df.get()
        filtered_count = len(filtered_df)
        message = f"Showing {filtered_count} of {total_count} records"
        # logger.debug(f"filter message: {message}")
        return message

    @output
    @render.table
    def mtcars_filtered_table():
        filtered_df = reactive_df.get()
        return filtered_df

    @output
    @render_widget
    def mtcars_output_widget1():
        df = reactive_df.get()
        plotly_express_plot = px.scatter(df, x="mpg", y="hp", color="cyl", size="wt")
        plotly_express_plot.update_layout(title="Cars with Plotly Express")
        return plotly_express_plot

    @output
    @render.plot
    def mtcars_plot1():
        df = reactive_df.get()
        matplotlib_fig, ax = plt.subplots()
        plt.title("Cars with matplotlib")
        ax.scatter(df["wt"], df["mpg"])
        return matplotlib_fig

    @output
    @render.plot
    def mtcars_plot2():
        df = reactive_df.get()
        plotnine_plot = (
            ggplot(df, aes("wt", "mpg"))
            + geom_point()
            + ggtitle("Cars with plotnine")
        )

        return plotnine_plot

    # return a list of function names for use in reactive outputs
    return [
        mtcars_record_count_string,
        mtcars_filtered_table,
        mtcars_output_widget1,
        mtcars_plot1,
        mtcars_plot2,
    ]