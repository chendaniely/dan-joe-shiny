import pandas as pd
from shiny import App, render, reactive, ui

app_ui = ui.page_fixed(
    ui.output_ui("table_day_filter"),
    ui.output_ui("table_time_filter"),
    ui.output_data_frame("render_df"),
)

def server(input, output, session):

    @reactive.calc #<<
    def filter_idx(): #<<
        df = df_tips() #<<
        idx = set(df.index) #<<

        if input.filter_day(): #<<
            current_idx = df.loc[df["day"].isin(input.filter_day())].index #<<
            idx = idx.intersection(set(current_idx)) #<<

        if input.filter_time(): #<<
            current_idx = df.loc[df["time"].isin(input.filter_time())].index #<<
            idx = idx.intersection(set(current_idx)) #<<

        # convert to list because you get this error #<<
        # when passing into .loc[] #<<
        # TypeError: Passing a set as an indexer is not supported. Use a list instead. #<<
        return list(idx) #<<


    # filtered dataframe from filters
    @reactive.calc
    def data_filtered():
        df = df_tips().loc[filter_idx()] #<<
        return df

    # dataframe to view in app
    @render.data_frame
    def render_df():
        return render.DataGrid(data_filtered())

    # table day filter
    @render.ui
    def table_day_filter():
        return ui.input_selectize(
            "filter_day",
            "table day filter:",
            df_tips()["day"].unique().tolist(),
            multiple=True,
            remove_button=True,
            options={"plugins": ["clear_button"]},
        )

    # table time filter
    @render.ui
    def table_time_filter():
        return ui.input_selectize(
            "filter_time",
            "table time filter:",
            df_tips()["time"].unique().tolist(),
            multiple=True,
            remove_button=True,
            options={"plugins": ["clear_button"]},
        )

    # placeholder for joined dataframe
    @reactive.calc
    def df_tips():
        # fmt: off
        data = {
            'total_bill': [
                16.99, 10.34, 21.01, 23.68, 24.59,
                25.29, 8.77, 26.88, 15.04, 14.78
            ],
            'tip': [
                1.01, 1.66, 3.50, 3.31, 3.61,
                4.71, 2.00, 3.12, 3.52, 3.00
            ],
            'sex': [
                'Female', 'Male', 'Male', 'Male', 'Female',
                'Male', 'Male', 'Male', 'Male', 'Female'
            ],
            'smoker': [
                'No', 'No', 'No', 'No', 'Yes',
                'No', 'No', 'Yes', 'No', 'Yes'
            ],
            'day': [
                'Sun', 'Fri', 'Sun', 'Thu', 'Sun',
                'Sun', 'Sat', 'Sat', 'Sat', 'Sat'
            ],
            'time': [
                'Dinner', 'Dinner', 'Lunch', 'Dinner', 'Lunch',
                'Dinner', 'Lunch', 'Dinner', 'Lunch', 'Dinner'
            ],
            'size': [2, 3, 3, 2, 4, 4, 2, 4, 2, 2]
        }
        # fmt: on

        df = pd.DataFrame(data)
        return df


app = App(app_ui, server)
