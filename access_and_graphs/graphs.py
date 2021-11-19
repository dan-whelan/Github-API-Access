import dash
import dash_core_components as core
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as plot
import pandas as p

repos = p.read_csv("Users/dwhelan/Desktop/Computer Science/Sweng/Github-API-Access/data/repos_info.csv")
commits = p.read_csv("Users/dwhelan/Desktop/Computer Science/Sweng/Github-API-Access/data/repos_info.csv")



commit_graph = p.DataFrame(p.merge(repos,commits,how='left',left_on='ID',right_on='Repo ID')).groupby('ID').size().reset_index()
commit_graph.columns(['ID', 'Commits'])

