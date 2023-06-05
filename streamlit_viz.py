import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def get_data() -> pd.DataFrame:
    data = pd.read_csv('MARKET_Car_Prices.csv')
    data.dropna(inplace=True)

    numbers_mapping = {'two': 2, 'four': 4, 'six': 6,
                       'five': 5, 'three': 3, 'twelve': 12, 'eight': 8}
    for col in ['num_of_doors', 'num_of_cylinders']:
        col_str = data[col].astype(str)
        col_nums = [numbers_mapping.get(w, w) for w in col_str]
        data[col] = col_nums
    return data


def create_plot(df, plot_type, X, Y, color):
    fig = None

    X_name = ' '.join(X.split('_')).capitalize()
    Y_name = ' '.join(Y.split('_')).capitalize() if Y else Y
    title = f'{X_name} vs {Y_name}' if Y_name else f'The distribution of {X_name}'

    if plot_type == 'Histogram':
        n_bins = st.sidebar.number_input(label='Number of bins', min_value=10)
        fig = px.histogram(df, x=X, color=color, marginal='rug', nbins=n_bins, title=title)
    elif Y and plot_type == 'Scatter Plot':
        color = None if not color else color
        fig = px.scatter(df, x=X, y=Y, color=color, title=title)
    elif Y and plot_type == 'Box Plot':
        fig = px.box(df, x=X, y=Y, color=color, title=title)
    elif plot_type == 'Bar Plot':
        group_by = st.sidebar.selectbox(options=[''] + categorical_columns, label='Group by?')
        if group_by:
            X = [X, group_by]
        if color:
            fig = px.histogram(df, x=X, color=color, barmode='group', histfunc='count', title=title)
        else:
            fig = px.histogram(df, x=X, histfunc='count', title=title)
    if fig:
        st.plotly_chart(fig)
    else:
        st.spinner('Please, complete filling the required fields.')


st.title('Market Car Prices')

df = get_data()


st.dataframe(df.head())


numeric_columns = list(df.columns[df.dtypes != 'object'])
categorical_columns = list(df.columns[df.dtypes == 'object'])
all_columns = list(df.columns)

st.sidebar.title('What kind of visualization do you want to make?')
plot_type = st.sidebar.selectbox(options=['', 'Histogram', 'Scatter Plot', 'Box Plot', 'Bar Plot'],
                                 label='Select chart type')

X, Y, color = None, None, None
add_kde = False

if plot_type:
    if plot_type in ['Histogram', 'Scatter Plot']:
        X_cols = numeric_columns
    elif plot_type == 'Bar Plot':
        X_cols = categorical_columns
    else:
        X_cols = all_columns

    X = st.sidebar.selectbox(options=[''] + X_cols, label='Select X axis')

    if X:
        if plot_type in ['Scatter Plot', 'Box Plot']:
            if plot_type == 'Box Plot' and X in numeric_columns:
                Y_cols = categorical_columns
            else:
                Y_cols = numeric_columns

            if X in Y_cols:
                Y_cols.remove(X)
            Y = st.sidebar.selectbox(options=[''] + Y_cols, label='Select Y axis')

            if Y and plot_type == 'Scatter Plot':
                color = st.sidebar.selectbox(options=[''] + all_columns,
                                             label='Select Color factor')

        # Create the plot
        create_plot(df, plot_type, X, Y, color)



