import dash
from dash import dcc
from dash import html
import plotly.express as plot
import pandas as p


####################################################################################
#ADMIN for reading in Data#
####################################################################################
#Use own absolute path to access data, Example data is my own Github data#
repos = p.read_csv("../Github-API-Access/repos_info.csv")
commits = p.read_csv("../Github-API-Access/commits_info.csv")

commit_number = p.DataFrame(p.merge(repos,commits,how='left',left_on='ID',right_on='Repo ID')).groupby('ID').size().reset_index()
commit_number.columns = ['ID', 'Commits']

combo = p.merge(repos,commit_number,on = 'ID')
repos_info = combo['Name']
commit_info = combo['Commits']
list_of_langs = []
for l in combo['Languages']:
    if type(l) is str:
        for lang in l.split(','):
            list_of_langs.append(lang.strip())
lang_count = p.Series(list_of_langs).value_counts

headerOne = {
    "font-weight" : "bold",
    "text-align" : "center",
}
headerTwo = {
    "font-style" : "italic",
    "text-align" : "center",
}

####################################################################################
#END OF ADMIN#
####################################################################################

app = dash.Dash(__name__)
server = app.server 
app_layout = html.Div(children=[
    html.H1("Github Software Engineering Measurement Graph", style=headerOne),
    html.H2("A Visualisation of " + repos['Owner'][0] + "'s Github Data", style=headerTwo),
    html.Div([
        html.Div([
            dcc.Graph(
                id="commits",
                figure= {
                    'data':[{'x':repos,'y':commits,'type':'bar'}],
                    'layout': {
                        'title':'Commits In Each Repository',
                        'plot_bgcolor':'rgb(0,0,0)',
                        'x-axis': {
                            'title':{
                                'text':'Repos'
                            }
                        },
                        'y-axis':{
                            'title':{
                                'text':'Commits Made'
                            }
                        }
                    }
                }
            )
        ],className="repos_bar"),

        html.Div([
            dcc.Graph(
                id="language",
                figure = {
                    'data':[
                        plot.pie(
                            list_of_langs,
                            names=list_of_langs,
                            values=lang_count,
                        )
                    ],
                    'layout':{
                        'title':'Most Used Languages',
                        'plotbg_color':'rgb(0,0,0)'
                    }
                }
            )
        ],className="language_pie")
    ],className="graphs")
])

if __name__ == '__main__':
    app.run_server(debug=True)


    

