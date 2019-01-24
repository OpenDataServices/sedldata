import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import sedldata

session = sedldata.Session()

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className="container", children=[

    html.Div(className="row", children=[
        html.Div(className="col-4", children=[
            html.Div(className="sticky-top pt-2", children=[
                html.H3(className="", children='SEDL Dashboard'),
                html.Br(),
                html.Div(className = "", children=[
                    html.Label('Select Datasets:', style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'CSU', 'value': 'CSU'},
                            {'label': 'KEY Fund', 'value': 'key-fund-005'},
                        ],
                        multi=True,
                        placeholder="All datasets",
                        id='collection-dropdown'
                    ),

                ]),
                html.Div(children=[
                    html.Label('Select Values:', style={'margin-top': '15px', "font-weight": "bold"}),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Number', 'value': 'number'},
                            {'label': 'Amount', 'value': 'amount'},
                            {'label': 'Average amount', 'value': 'average-amount'},
                        ],
                        id='value-type',
                        labelStyle={'margin-right': '10px'},
                        value='number'
                    ),
                ]),
                html.Div(children=[
                    html.Label('Select Investment Type:', style={'margin-top': '15px', "font-weight": "bold"}),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Whole Deal', 'value': 'deal'},
                            {'label': 'Equity', 'value': 'equity'},
                            {'label': 'Grant', 'value': 'grant'},
                            {'label': 'Credit', 'value': 'credit'},
                        ],
                        id='investment-type',
                        labelStyle={'margin-right': '10px'},
                        #inputStyle={'margin-top': '-3px'},
                        value='deal'
                    ),
                ]),
                html.Div(children=[
                    html.Label('Select Year Range:', style={'margin-top': '15px', "font-weight": "bold"}),
                    dcc.RangeSlider(
                        id='year-range',
                        min=2014,
                        max=2019,
                        marks = {num: str(num) for num in range(2014, 2020)},
                        value=[2014, 2019]
                    ),
                ]),
            ]),
        ]),
        html.Div(className="col-8", children=[
            html.Div(className="card mt-2 text-center", children=[
                html.H5(className="card-header", children='Yearly Breakdown'),
                dcc.Graph(id='by-year-graph',
                    config={
                        'displayModeBar': False
                    },
                )
            ]),
            html.Div(id='classification-card', className="card mt-2 text-center", children=[
                html.H5(className="card-header", children='Project Classification'),
                dcc.Graph(id='classification-graph',
                    config={
                        'displayModeBar': False
                    },
                )
            ]),
        ])
    ])
])


## YEAR GRAPH

def single_category_query(collections=None, year_range=None, aggregate='', order='asc'):
    collections = collections or tuple()
    year_range = year_range or (2000, 9999)
    query = '''
    with year_summary as (select deal_summary.*,
    deal ->> 'id' deal_id,
    deal -> 'projects' -> 0 ->> 'id' project_id,
    convert_to_numeric(left(greatest(
    deal -> 'projects' -> 0 ->> 'startDate',
    deal -> 'projects' -> 0 ->> 'endDate',
    deal ->> 'dealDate',
    deal -> 'investments' -> 'equity' -> 0 ->> 'dateAgreed',
    deal -> 'investments' -> 'equity' -> 0 ->> 'dateOffered',
    deal -> 'investments' -> 'credit' -> 0 ->> 'dateAgreed',
    deal -> 'investments' -> 'credit' -> 0 ->> 'dateOffered',
    deal -> 'investments' -> 'grants' -> 0 ->> 'dateAgreed',
    deal -> 'investments' -> 'grants' -> 0 ->> 'dateOffered',
    deal -> 'offers' -> 0 ->> 'startDate',
    deal -> 'offers' -> 0 ->> 'endDate'
    ),4)) display_date
    from deal_summary) 
                                       
    select 
            {aggregate} "category",
            sum(equity_count) equity_count, sum(equity_value) equity_value, sum(case when equity_estimated_value <> 0 then equity_estimated_value else equity_value end) estimated_equity_value,
            sum(credit_count) credit_count, sum(credit_value) credit_value, sum(case when credit_estimated_value <> 0 then credit_estimated_value else credit_value end) estimated_credit_value, 
            sum(grant_count) grant_count, 
            sum(case when grant_amount_disbursed > 0 then grant_amount_disbursed else grant_amount_committed end) grant_value,
            sum(case when grant_amount_requested > 0 then grant_amount_requested else case when grant_amount_disbursed > 0 then grant_amount_disbursed else grant_amount_committed end end) estimated_grant_value,
            sum(value) deal_value,
            count(*) deal_count
    from year_summary 
    left join 
            (select collection, project_id, max(display_date) as display_date 
         from year_summary where display_date is not null group by 1,2) project_year using(project_id, collection) 
    where 
         {aggregate} is not null and coalesce(year_summary.display_date, project_year.display_date) between %s and %s {collection} 
    group by 1 order by 1 {order} 
    '''
    collection_part = ('and collection in (' + ','.join(['%s']*len(collections)) + ')') if collections else ''
    query = query.format(aggregate=aggregate, collection=collection_part, order=order)
    return session.get_results(query, params=year_range + collections) 


def gather_measure_data(results, value_type, investment_type):

    categories = []
    estimated_values = []
    values = []
    for result in results['data']:
        categories.append(str(result['category']))
        if value_type == 'amount':
            if investment_type == 'deal':
                estimated_values.append(result['estimated_equity_value'] + result['estimated_credit_value'] + result['estimated_grant_value'])
                values.append(result['equity_value'] + result['credit_value'] + result['grant_value'])
            else:
                estimated_values.append(result['estimated_{}_value'.format(investment_type)])
                values.append(result['{}_value'.format(investment_type)])

        if value_type == 'number':
            if investment_type == 'deal':
                values.append(result['deal_count'])
            else:
                values.append(result['{}_count'.format(investment_type)])

        if value_type == 'average-amount':
            if investment_type == 'deal':
                values.append((result['equity_value'] + result['credit_value'] + result['grant_value']) / result['deal_count'])
                estimated_values.append((result['estimated_equity_value'] + result['estimated_credit_value'] + result['estimated_grant_value']) / result['deal_count'])
            else:
                if not result['{}_count'.format(investment_type)]:
                    estimated_values.append(0)
                    values.append(0)
                    continue
                values.append(result['{}_value'.format(investment_type)] / result['{}_count'.format(investment_type)])
                estimated_values.append(result['estimated_{}_value'.format(investment_type)] / result['{}_count'.format(investment_type)])

    return categories, estimated_values, values


human_titles = {
    "deal": "{} of Deals",
    "credit": "{} of Credits",
    "equity": "{} of Equities",
    "grant": "{} of Grants",
}

def get_titles(value_type, investment_type):
    if value_type == 'amount':
        axis_title = 'Amount(£)'
    if value_type == 'number':
        axis_title = 'Number'
    if value_type == 'average-amount':
        axis_title = 'Average Amount(£)'
    return axis_title, human_titles[investment_type].format(axis_title)

@app.callback(
    Output(component_id='by-year-graph', component_property='figure'),
    [Input(component_id='collection-dropdown', component_property='value'),
     Input(component_id='value-type', component_property='value'),
     Input(component_id='investment-type', component_property='value'),
     Input(component_id='year-range', component_property='value')]
)
def year_graph(collections, value_type, investment_type, year_range):
    collections = collections or []
    year_range = year_range or [2000, 9999]
    results = single_category_query(tuple(collections), tuple(year_range), 'coalesce(year_summary.display_date, project_year.display_date)')

    categories, estimated_values, values = gather_measure_data(results, value_type, investment_type)

    data = []
    if estimated_values:
        data.append(go.Bar(
            x=categories,
            y=estimated_values,
            name='Estimated Amounts'
        ))

    data.append(go.Bar(
        x=categories,
        y=values,
        name='Amounts'
    ))

    axis_title, title  = get_titles(value_type, investment_type)

    layout = go.Layout(
        title=title,
        barmode='group',
        yaxis=dict(
            title=axis_title
        ),
        xaxis=dict(
            title='year',
            type='category'
        )
    )

    return dict(data=data, layout=layout)


## Project Classification


def project_classification_exists_query(collections=None, year_range=None):
    collections = collections or tuple()
    query = ''' select count(*) deal_count from deal_summary where deal->'projects'->0->'classification'->0->>'title' is not null {} '''
    if collections:
        query = query.format('and collection in (' + ','.join(['%s']*len(collections)) + ')')
    else:
        query = query.format('')
    return session.get_results(query, params=collections) 


@app.callback(
    Output(component_id='classification-card', component_property='style'),
    [Input(component_id='collection-dropdown', component_property='value')]
)
def project_clasification_appear(collections):
    if collections:
        collections = tuple(collections)
    results = project_classification_exists_query(collections)
    if results['data'][0]['deal_count']:
        return {'display': 'inherit'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='classification-graph', component_property='figure'),
    [Input(component_id='collection-dropdown', component_property='value'),
     Input(component_id='value-type', component_property='value'),
     Input(component_id='investment-type', component_property='value'),
     Input(component_id='year-range', component_property='value')]
)
def project_clasification(collections, value_type, investment_type, year_range):
    if collections:
        collections = tuple(collections)
    results = single_category_query(collections, tuple(year_range), '''trim(deal->'projects'->0->'classification'->0->>'title')''', 'desc')

    categories, estimated_values, values = gather_measure_data(results, value_type, investment_type)

    data = []
    if estimated_values:
        data.append(go.Bar(
            y=categories,
            x=estimated_values,
            orientation = 'h',
            name='Estimated Amounts'
        ))

    data.append(go.Bar(
        y=categories,
        x=values,
        orientation = 'h',
        name='Amounts'
    ))
    
    axis_title, title  = get_titles(value_type, investment_type)

    layout = go.Layout(
        title=title,
        barmode='group',
        xaxis=dict(
            title=axis_title
        ),
        yaxis=dict(
        ),
        margin=dict(l=200)
    )
    return dict(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
