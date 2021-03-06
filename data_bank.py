# -*-coding:utf-8-*-
# import all the packages that are needed

import sys
import sqlite3
#import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

# to form the web page

app = dash.Dash(__name__)
#server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout = html.Div(children=[
    html.H2(children=u'CDE收审情况'),
    html.Div([

        dcc.RadioItems(
            id = 'received_reviewed',
            options = [
                {'label': u'受理品种目录浏览', 'value': 'drugs_appl_received'},
                {'label': u'在审品种目录浏览', 'value': 'drugs_in_review'}
            ],
            value = 'drugs_appl_received',
            labelStyle={'display': 'inline-block'}
        ),


        html.Hr(),
        html.Label(u'申请类型'),
        dcc.Dropdown(
            id = 'app_type',
            options = [
                {'label': i, 'value': i} for i in [u'新药', u'补充申请', u'复审', u'仿制', u'进口']
            ],
            value = '%'
        ),

        #html.Hr(),
        html.Label(u'药品类型'),
        dcc.Dropdown(
            id = 'drug_type',
            options = [{'label': i, 'value': i} for i in [u'化药',u'中药',u'治疗用生物制品',u'预防用生物制品']],
            value = '%'
        ),

        html.Hr(),
        html.Label(u' 受理号'),
        dcc.Input(id = 'app_no', value='', type = 'text'),

        html.Br(),
        html.Br(),
        html.Label(u'药品名称：请输入“吸入 氨溴索”试试'),
        dcc.Input(id = 'drug_name', value = '', type = 'text'),

        html.Br(),
        html.Br(),
        html.Label(u'公司名称：请输入“恒瑞 齐鲁”试试'),
        dcc.Input(id = 'corp_name', value = '', type = 'text'),

        html.Br(),


    ], style = {'columnCount': 2, 'width': '48%'}),

    html.Button('Submit', id = 'button'),

    html.Hr(),
    html.Br(),
    html.Div(id = 'query_results')
])


@app.callback(
    dash.dependencies.Output('query_results', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('received_reviewed', 'value'),
     dash.dependencies.State('app_type', 'value'),
     dash.dependencies.State('drug_type', 'value'),
     dash.dependencies.State('app_no', 'value'),
     dash.dependencies.State('drug_name', 'value'),
     dash.dependencies.State('corp_name', 'value'),
     ]
)
def update_table(n_clicks, received_reviewed, app_type, drug_type, app_no, drug_name, corp_name):

    if drug_name != '':
        drug_name = drug_name.strip().split()
        drug_name = ["'%" + d + "%'" for d in drug_name]
        drug_name = ['drug_name like ' + d for d in drug_name]
        drug_name = ' and '.join(drug_name)
    else:
        drug_name = "drug_name like '%'"


    if corp_name != '':
        corp_name = corp_name.strip().split()
        corp_name = ["'%" + d + "%'" for d in corp_name]
        corp_name = ['corp_name like ' + d for d in corp_name]
        corp_name = ' or '.join(corp_name)
    else:
        corp_name = "corp_name like '%'"


    if app_no == '':
        app_no = "%"

    query = "select * from " + received_reviewed + " where app_type like '" + app_type + "' and drug_type like '" + drug_type +\
            "' and app_no like '" + app_no + "' and (" + drug_name + ") and (" + corp_name + ")"

    # connect the database
    # in this database, there are three tables named 'ims_sales', 'drugs_in_review',
    # 'drugs_appl_received'

    db_path = sys.path[0] + "/data/drugsatcde.db"
    #print(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    results = cursor.execute(query)
    results = results.fetchall()
    columns_list = [t[0] for t in cursor.description]
    conn.close()

    return html.Table([html.Tr([html.Th(col) for col in columns_list])] + [html.Tr([html.Td(col) for col in results[i]]) for i in range(len(results))])


if __name__ == '__main__':
    app.run_server(debug = True)
