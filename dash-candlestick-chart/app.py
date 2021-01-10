import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import stockprice_df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6("Stock price"),
    html.Div(["Stock Code: ",
              dcc.Input(id='stockcode-input', value='', type='text')]),
    dcc.RadioItems(
        id='frequency-type',
        options=[
            {'label': 'Daily', 'value': 'D'},
            {'label': 'Weekly', 'value': 'W'},
            {'label': 'Monthly', 'value': 'M'},
            {'label': 'Yearly', 'value': 'Y'}
        ],
        value='D',
        labelStyle={'display': 'inline-block'}
    ),
    html.Br(),
    html.Div(id='stock-links'),
    dcc.Graph(id='stock-graph'),
    html.Div(id='data-table')

])


@app.callback(
    Output(component_id='stock-links', component_property='children'),
    [Input(component_id='stockcode-input', component_property='value')]
)
def update_links_Div(input_value):
    if (len(input_value) == 3):
        return html.Div([html.A('Yahoo Finance Quote for %s' % input_value, href='https://au.finance.yahoo.com/quote/%s.AX/' % input_value, target='_blank'),
                         html.Br(),
                         html.A('ASX Quote for %s' % input_value, href='https://www2.asx.com.au/markets/company/%s' % input_value, target='_blank'),
                         html.Br(),
                         html.A('Google Finance Quote %s' % input_value, href='https://www.google.com/search?q=google+finance+%s+ASX' % input_value, target='_blank')])


@app.callback(
    Output(component_id='data-table', component_property='children'),
    [Input(component_id='stockcode-input', component_property='value'),
     Input(component_id='frequency-type', component_property='value')]
)
def update_table(input_value, frequency_type):
    if (len(input_value) == 3):
        # setup dataframe
        df = stockprice_df.get_stock_df(input_value, frequency_type)

        return html.H6(stockprice_df.get_dash_table_header(frequency_type)), \
               html.Div(
                   [
                       dash_table.DataTable(
                           data=df.to_dict("rows"),
                           columns=[{"id": x, "name": x} for x in df.columns],
                       )
                   ]
               )


@app.callback(
    Output('stock-graph', 'figure'),
    [Input(component_id='stockcode-input', component_property='value'),
     Input(component_id='frequency-type', component_property='value')]
)
def update_figure(input_value, frequency_type):
    candlestick = {}
    volumeBar = {}

    if (len(input_value) == 3):
        app.logger.info("3 characters entered " + input_value + ' with frequency set as ' + frequency_type)
        df = stockprice_df.get_stock_df(input_value, frequency_type)

        # define graph objects
        candlestick = go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name=input_value)

        volumeBar = go.Bar(x=df['Date'], y=df['Volume'], name="Volume")

    # declare figure
    fig = make_subplots(rows=2, cols=1)
    # Add graph objects to figure
    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(volumeBar, row=2, col=1)

    fig.update_layout(
        title=input_value + " Share Price",
        yaxis_title="Price",
        legend_title="Legend",
        xaxis_rangeslider_visible=False,
        height=1200
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
