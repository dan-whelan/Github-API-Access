import dash
import dash_core_components as core
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as plot
import pandas as p

repos = p.read_csv("Users/dwhelan/Desktop/Computer Science/Sweng/Github-API-Access/data/repos_info.csv")
commits = p.read_csv("Users/dwhelan/Desktop/Computer Science/Sweng/Github-API-Access/data/repos_info.csv")



commit_number = p.DataFrame(p.merge(repos,commits,how='left',left_on='ID',right_on='Repo ID')).groupby('ID').size().reset_index()
commit_number.columns(['ID', 'Commits'])

combo = p.merge(repos,commit_number,on = 'ID')
repos_info = combo['Name']
commit_info = combo['Commit Number']
list_of_langs = []
for l in combo['Languages']:
    if type(l) is str:
        for lang in l.split(','):
            list_of_langs.append(lang.strip())
lang_count = p.Series(list_of_langs).value_counts


title = {
    "font-weight" : "bold",
    "text-align" : "center",
}
subheading = {
    "font-style" : "italic",
    "text-align" : "center",
}

app = dash.Dash(__name__)
app_layout = html.Div(children=[
    html.H1("Github Software Engineering Measurement Graph", style=title),
    html.H2("A Visualisation of " + repos['Owner'][0] + "'s Github Data"),

    html.Div(
        html.Div(
            core.Graph(
                
            )
        )
    )
])



    

