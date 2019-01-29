from urllib.parse import unquote

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import defaultdict

import sedldata

session = sedldata.Session()

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'SEDL Dashboard'

results = session.get_results('select dashboard.collection from dashboard join collection_summary using(collection)')

options = [{'label': result['collection'], 'value': result['collection']} for result in results['data']]

app.layout = html.Div(className="container", children=[
    dcc.Location(id='url', refresh=False),
    html.Div(className="row", children=[
        html.Div(className="col-4", children=[
            html.Div(className="sticky-top pt-2", children=[
                html.Div(id="hide-when-url", children=[
                    html.H3(className="", children=[
                        html.Img(alt="Social Economy Data Lab", src="http://socialeconomydatalab.org/img/logos/sedl_logo_nobkgd.svg",
                                 style= {"width": "30px", "margin-right": "10px", "padding-bottom": "5px"}),
                        'SEDL Dashboard'
                    ]),
                    html.Br(),
                    html.Div(className = "", children=[
                        html.Label('Select Datasets:', style={"font-weight": "bold"}),
                        dcc.Dropdown(
                            options=options,
                            multi=True,
                            placeholder="All datasets",
                            id='collection-dropdown'
                        ),
                    ]),
                ]),
                html.Div(children=[
                    html.Label('Select Part of Deal:', style={'margin-top': '15px', "font-weight": "bold"}),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Whole Deal', 'value': 'deal'},
                            {'label': 'Offer', 'value': 'offer'},
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
                html.H5(className="card-header", children='Summary'),
                html.Div(className="card-body ", children=[
                    html.H5(className="card-title", children='Total', id='total-text'),
                    dcc.Graph(id='by-year-graph',
                        config={
                            'displayModeBar': False
                        },
                    )
                ]),
            ]),
            html.Div(id='classification-card', className="card mt-2 text-center", children=[
                html.H5(className="card-header", children='Project Classification'),
                html.Div(className="card-body ", children=[
                    dcc.Graph(id='classification-graph',
                        config={
                            'displayModeBar': False
                        },
                    )
                ]),
            ]),
            html.Div(className="card mt-2 text-center", children=[
                html.H5(className="card-header", children='Indices of Deprivation'),
                html.Div(className="row", children=[
                    html.Div(className="col-6", children=[
                        html.Label('Select Country:', style={"font-weight": "bold"}),
                        dcc.Dropdown(
                            options=[
                                {'label': 'England', 'value': 'imd_england'},
                                {'label': 'Scotland', 'value': 'imd_scotland'},
                            ],
                            id='imd-country-dropdown',
                            value='imd_england',
                            searchable=False,
                            clearable=False
                        ),
                    ]),
                    html.Div(className="col-6", children=[
                        html.Label('Select ranking:', style={"font-weight": "bold"}),
                        dcc.Dropdown(
                            id='imd-index-dropdown',
                            searchable=False,
                            clearable=False
                        ),
                    ]),
                ]),
                html.Div(children=[
                    html.Div(className="card-body ", children=[
                        dcc.Graph(id='deprivation-graph',
                            config={
                                'displayModeBar': False
                            },
                        )
                    ]),
                ]),
            ]),
            html.Div(className="card mt-2 text-center", children=[
                html.H5(className="card-header", children='Region'),
                html.Div(className="card-body ", children=[
                    dcc.Graph(id='region-graph',
                        config={
                            'displayModeBar': False
                        },
                    )
                ]),
            ]),
        ])
    ])
])


@app.callback(
    Output(component_id='hide-when-url', component_property='style'),
    [Input(component_id='url', component_property='search')])
def hide_when_url(url):
    if url and url.startswith('?collection='):
        return {"display": 'none'}
    return {}


@app.callback(
    Output(component_id='collection-dropdown', component_property='value'),
    [Input(component_id='url', component_property='search')])
def select_collection_from_search(url):
    if url and url.startswith('?collection='):
        return [unquote(url.split('=')[1])]
    return []


@app.callback(
    Output(component_id='value-type', component_property='options'),
    [Input(component_id='investment-type', component_property='value')])
def change_value_type_options(investment_type):
    if investment_type == 'deal':
        return [
            {'label': 'Number', 'value': 'number'},
            {'label': 'Amount', 'value': 'amount'},
            {'label': 'Estimated Amount', 'value': 'estimated-amount'},
            {'label': 'Average amount', 'value': 'average-amount'},
            {'label': 'Amount by investment type', 'value': 'amount-by-investment'}
        ]
    if investment_type == 'grant':
        return [
            {'label': 'Number', 'value': 'number'},
            {'label': 'Amount', 'value': 'amount'},
            {'label': 'Amount Requested ', 'value': 'estimated-amount'},
            {'label': 'Average amount', 'value': 'average-amount'},
        ]
    if investment_type == 'offer':
        return [
            {'label': 'Offer Count', 'value': 'number'},
            {'label': 'Investment Target', 'value': 'amount'},
            {'label': 'Average Investment Target', 'value': 'average-amount'},
        ]

    return [
            {'label': 'Number', 'value': 'number'},
            {'label': 'Amount', 'value': 'amount'},
            {'label': 'Estimated Amount', 'value': 'estimated-amount'},
            {'label': 'Average amount', 'value': 'average-amount'},
        ]


@app.callback(
    Output(component_id='value-type', component_property='value'),
    [Input(component_id='investment-type', component_property='value')]
)
def change_value_type_value(investment_type):
    return 'number'


def single_category_query(collections=None, year_range=None, aggregate='', order='asc', extra_params=None):
    collections = collections or tuple()
    extra_params = extra_params or tuple()
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
            sum(offer_count) offer_count, 
            sum(investment_target) total_investment_target, 
            case when sum(case when investment_target > 0 then 1 else 0 end) = 0 then 0 else sum(investment_target)/sum(case when investment_target > 0 then 1 else 0 end) end average_investment_target,
            sum(equity_count) equity_count, sum(equity_value) equity_value, sum(case when equity_estimated_value <> 0 then equity_estimated_value else equity_value end) estimated_equity_value,
            sum(credit_count) credit_count, sum(credit_value) credit_value, sum(case when credit_estimated_value <> 0 then credit_estimated_value else credit_value end) estimated_credit_value, 
            sum(grant_count) grant_count, 
            sum(case when grant_amount_disbursed > 0 then grant_amount_disbursed else grant_amount_committed end) grant_value,
            sum(case when grant_amount_requested > 0 then grant_amount_requested else case when grant_amount_disbursed > 0 then grant_amount_disbursed else grant_amount_committed end end) estimated_grant_value,
            sum(case when estimated_value > 0 then estimated_value else value end) estimated_value,
            sum(value) deal_value,
            count(*) deal_count
    from year_summary 
    left join 
            (select collection, project_id, max(display_date) as display_date 
         from year_summary where display_date is not null group by 1,2) project_year using(project_id, collection) 
    join dashboard on dashboard.collection = year_summary.collection 
    where 
         {aggregate} is not null and coalesce(year_summary.display_date, project_year.display_date) between %s and %s {collection} 
    group by 1 order by 1 {order} 
    '''
    collection_part = ('and year_summary.collection in (' + ','.join(['%s']*len(collections)) + ')') if collections else ''
    query = query.format(aggregate=aggregate, collection=collection_part, order=order)
    return session.get_results(query, params=extra_params * 2 + year_range + collections) 


def gather_measure_data(results, value_type, investment_type):

    categories = []
    #estimated_values = []
    values = defaultdict(list)
    for result in results['data']:
        categories.append(str(result['category']))
        if value_type == 'amount':
            if investment_type == 'deal':
                #estimated_values.append(result['estimated_value'])
                values['Amounts'].append(result['equity_value'] + result['credit_value'] + result['grant_value'])
            elif investment_type == 'offer':
                values['Amounts'].append(result['total_investment_target'])
            else:
                #estimated_values.append(result['estimated_{}_value'.format(investment_type)])
                values['Amounts'].append(result['{}_value'.format(investment_type)])

        if value_type == 'number':
            if investment_type == 'deal':
                values['Amounts'].append(result['deal_count'])
            elif investment_type == 'offer':
                values['Amounts'].append(result['offer_count'])
            else:
                values['Amounts'].append(result['{}_count'.format(investment_type)])

        if value_type == 'average-amount':
            if investment_type == 'deal':
                values['Amounts'].append((result['equity_value'] + result['credit_value'] + result['grant_value']) / result['deal_count'])
                #estimated_values.append((result['estimated_equity_value'] + result['estimated_credit_value'] + result['estimated_grant_value']) / result['deal_count'])
            elif investment_type == 'offer':
                values['Amounts'].append(result['average_investment_target'])
            else:
                if not result['{}_count'.format(investment_type)]:
                    #estimated_values.append(0)
                    values['Amounts'].append(0)
                    continue
                values['Amounts'].append(result['{}_value'.format(investment_type)] / result['{}_count'.format(investment_type)])
                #estimated_values.append(result['estimated_{}_value'.format(investment_type)] / result['{}_count'.format(investment_type)])

        if value_type == 'estimated-amount':
            if investment_type == 'deal':
                values['Estimated Amounts'].append(result['estimated_value'])
                values['Amounts'].append(result['equity_value'] + result['credit_value'] + result['grant_value'])
            else:
                values['Estimated Amounts'].append(result['estimated_{}_value'.format(investment_type)])
                values['Amounts'].append(result['{}_value'.format(investment_type)])

        if value_type == 'amount-by-investment':
            if investment_type == 'deal':
                values['Equity'].append(result['equity_value'])
                values['Credit'].append(result['credit_value'])
                values['Grant'].append(result['grant_value'])


    return categories, values


human_titles = {
    "deal": "{} of Deals",
    "credit": "{} of Credits",
    "equity": "{} of Equities",
    "grant": "{} of Grants",
    "offer": "{} of Offers",
}

def get_titles(value_type, investment_type):

    if value_type in ('amount', 'amount-by-investment'):
        if investment_type == 'offer':
            axis_title = 'Investment Target'
        else:
            axis_title = 'Amount'

    if value_type == 'number':
        axis_title = 'Number'

    if value_type == 'average-amount':
        if investment_type == 'offer':
            axis_title = 'Average Investment Target'
        else:
            axis_title = 'Amount'

    if value_type == 'estimated-amount':
        if investment_type == 'grant':
            axis_title = 'Requesed Amount'
        else:
            axis_title = 'Estimated Amount'

    return axis_title, human_titles[investment_type].format(axis_title)


@app.callback(
    Output(component_id='total-text', component_property='children'),
    [Input(component_id='collection-dropdown', component_property='value'),
     Input(component_id='value-type', component_property='value'),
     Input(component_id='investment-type', component_property='value'),
     Input(component_id='year-range', component_property='value')]
)
def total(collections, value_type, investment_type, year_range):
    collections = collections or []
    year_range = year_range or [2000, 9999]
    results = single_category_query(tuple(collections), tuple(year_range), "'total'")

    if value_type == 'amount-by-investment':
        value_type = 'amount'
    categories, values = gather_measure_data(results, value_type, investment_type)

    estimated_amounts = values.get('Estimated Amounts')
    amounts = values.get('Amounts')
    if estimated_amounts:
        result = estimated_amounts[0]
    elif amounts:
        result = amounts[0]
    else:
        result = 0

    axis_title, title  = get_titles(value_type, investment_type)

    prefix = '' if 'average' in value_type else 'Total '
    currency = '£' if 'amount' in value_type else ''

    return '{}{}: {}{:,.0f}'.format(prefix, title, currency, result)



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

    categories, values = gather_measure_data(results, value_type, investment_type)

    data = []

    for key, value in values.items():
        data.append(go.Bar(
            x=categories,
            y=value,
            name=key
        ))

    axis_title, title  = get_titles(value_type, investment_type)


    if value_type == 'amount-by-investment':
        barmode = 'stack'
    else:
        barmode = 'group'

    layout = go.Layout(
        title=title,
        barmode=barmode,
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

    categories, values = gather_measure_data(results, value_type, investment_type)

    data = []
    for key, value in values.items():
        data.append(go.Bar(
            y=categories,
            x=value,
            name=key,
            orientation = 'h'
        ))

    axis_title, title  = get_titles(value_type, investment_type)

    if value_type == 'amount-by-investment':
        barmode = 'stack'
    else:
        barmode = 'group'

    layout = go.Layout(
        title=title,
        barmode=barmode,
        xaxis=dict(
            title=axis_title
        ),
        yaxis=dict(
        ),
        margin=dict(l=200)
    )
    return dict(data=data, layout=layout)


@app.callback(
    Output(component_id='imd-index-dropdown', component_property='options'),
    [Input(component_id='imd-country-dropdown', component_property='value')]
)
def imd_index_options(country):

    if country == 'imd_england':
        options=[
            {"value": "Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)", "label": "Index of Multiple Deprivation"},
            {"value": "Crime Decile (where 1 is most deprived 10% of LSOAs)", "label": "Crime"}, 
            {"value": "Income Decile (where 1 is most deprived 10% of LSOAs)", "label": "Income"},
            {"value": "Employment Decile (where 1 is most deprived 10% of LSOAs)", "label": "Employment"},
            {"value": "Living Environment Decile (where 1 is most deprived 10% of LSOAs)", "label": "Living Environment"},
            {"value": "Education, Skills and Training Decile (where 1 is most deprived 10% of LSOAs)", "label": "Education, Skills and Training"},
            {"value": "Barriers to Housing and Services Decile (where 1 is most deprived 10% of LSOAs)", "label": "Barriers to Housing and Services"},
            {"value": "Geographical Barriers Sub-domain Decile (where 1 is most deprived 10% of LSOAs)", "label": "Geographical Barriers Sub-domain"},
            {"value": "Health Deprivation and Disability Decile (where 1 is most deprived 10% of LSOAs)", "label": "Health Deprivation and Disability"},
            {"value": "Income Deprivation Affecting Older People (IDAOPI) Decile (where 1 is most deprived 10% of LSOAs)", "label": "Income (Older People)"},
            {"value": "Income Deprivation Affecting Children Index (IDACI) Decile (where 1 is most deprived 10% of LSOAs)", "label": "Income (Children)"}
        ]
    elif country == 'imd_scotland':
        options=[
            {"value": "Overall_SIMD16_Decile", "label": "Index of Multiple Deprivation"},
            {"value": "Crime_domain_2016_decile", "label": "Crime"},
            {"value": "Access_domain_2016_decile", "label": "Access"},
            {"value": "Health_domain_2016_decile", "label": "Health"},
            {"value": "Income_Domain_2016_Decile", "label": "Income"},
            {"value": "Housing_domain_2016_decile", "label": "Housing"},
            {"value": "Education_domain_2016_decile", "label": "Education"},
            {"value": "Employment_domain_2016_decile", "label": "Employment"}
        ]
    return options

@app.callback(
    Output(component_id='imd-index-dropdown', component_property='value'),
    [Input(component_id='imd-country-dropdown', component_property='value')]
)
def imd_index_initial_value(country):
    if country == 'imd_england':
        return 'Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)'
    elif country == 'imd_scotland':
        return 'Overall_SIMD16_Decile'


@app.callback(
    Output(component_id='deprivation-graph', component_property='figure'),
    [Input(component_id='collection-dropdown', component_property='value'),
     Input(component_id='value-type', component_property='value'),
     Input(component_id='investment-type', component_property='value'),
     Input(component_id='year-range', component_property='value'),
     Input(component_id='imd-index-dropdown', component_property='value'),
    ]
)
def imd_graph(collections, value_type, investment_type, year_range, index):
    if collections:
        collections = tuple(collections)

    results = single_category_query(collections, tuple(year_range), '''imd_data ->> %s ''', 'asc', (index,))

    categories, values = gather_measure_data(results, value_type, investment_type)

    deciles = [str(x) for x in range(1,11)]

    data = []
    for key, value in values.items():
        decile_values = [0] * 10
        for decile, decile_value in zip(categories, value):
            decile_values[int(decile) - 1] = decile_value

        data.append(go.Bar(
            x=deciles,
            y=decile_values,
            name=key,
        ))

    axis_title, title  = get_titles(value_type, investment_type)

    if value_type == 'amount-by-investment':
        barmode = 'stack'
    else:
        barmode = 'group'

    layout = go.Layout(
        title=title,
        barmode=barmode,
        yaxis=dict(
            title=axis_title
        ),
        xaxis=dict(
            title='Decile (1 most deprived, 10 least deprived)',
            type='category'
        ),
    )
    return dict(data=data, layout=layout)


@app.callback(
    Output(component_id='region-graph', component_property='figure'),
    [Input(component_id='collection-dropdown', component_property='value'),
     Input(component_id='value-type', component_property='value'),
     Input(component_id='investment-type', component_property='value'),
     Input(component_id='year-range', component_property='value')]
)
def region_clasification(collections, value_type, investment_type, year_range):
    if collections:
        collections = tuple(collections)
    results = single_category_query(collections, tuple(year_range), '''nuts1''', 'desc')

    categories, values = gather_measure_data(results, value_type, investment_type)

    data = []
    for key, value in values.items():
        data.append(go.Bar(
            y=categories,
            x=value,
            name=key,
            orientation = 'h'
        ))

    axis_title, title  = get_titles(value_type, investment_type)

    if value_type == 'amount-by-investment':
        barmode = 'stack'
    else:
        barmode = 'group'

    layout = go.Layout(
        title=title,
        barmode=barmode,
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
