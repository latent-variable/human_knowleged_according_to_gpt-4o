import json
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import datetime
import numpy as np

# Load JSON data
with open('knowledge_graph.json', 'r') as file:
    data = json.load(file)

nodes = data['nodes']

# Extract dynamic categories and assign colors
unique_categories = list(set(node['category'] for node in nodes))
category_colors = {category: f'rgba({i*37 % 255},{i*57 % 255},{i*97 % 255},0.7)' for i, category in enumerate(unique_categories)}

# Convert dates to numerical format (years) and use logarithmic scale for time
for node in nodes:
    if "BC" in node['date']:
        year = -int(node['date'].split('-')[0].replace(' BC', ''))
    else:
        year = int(node['date'].split('-')[0].replace(' AD', ''))
    node['year'] = year
    node['log_year'] = np.log10(abs(year) + 1) * (-1 if year < 0 else 1)
    node['color'] = category_colors[node['category']]

# Create initial scatter plot for nodes without text labels
def create_scatter(selected_categories, use_log_scale):
    filtered_nodes = [node for node in nodes if node['category'] in selected_categories]
    x_values = [node['log_year'] if use_log_scale else node['year'] for node in filtered_nodes]
    scatter = go.Scatter(
        x=x_values,
        y=[node['complexity'] for node in filtered_nodes],
        mode='markers',
        marker=dict(size=10, color=[node['color'] for node in filtered_nodes], line=dict(width=2, color='darkblue')),
        hoverinfo='text',
        text=[node['id'] for node in filtered_nodes]  # Keep text for hover info
    )
    return scatter

# Define initial layout
layout = go.Layout(
    title='2D Visualization of Human Knowledge',
    xaxis=dict(title='Time', type='linear', gridcolor='lightgrey', zerolinecolor='grey'),
    yaxis=dict(title='Complexity', type='linear', gridcolor='lightgrey', zerolinecolor='grey'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    margin=dict(l=40, r=40, b=40, t=40),
    height=800
)

# Initialize figure with all categories selected
initial_categories = unique_categories
use_log_scale = True
scatter = create_scatter(initial_categories, use_log_scale)
fig = go.Figure(data=[scatter], layout=layout)

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Human Knowledge Timeline According to GPT-4o', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': category, 'value': category} for category in unique_categories],
        value=initial_categories,
        multi=True,
        style={'margin': '20px'}
    ),
    dcc.RadioItems(
        id='time-scale-toggle',
        options=[
            {'label': 'Logarithmic Scale', 'value': 'log'},
            {'label': 'Linear Scale', 'value': 'linear'}
        ],
        value='log',
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),
    dcc.Graph(id='2d-graph', figure=fig, config={'displayModeBar': True}),
    html.Div(id='node-info', style={'textAlign': 'center', 'fontSize': 18, 'marginTop': 20})
])

@app.callback(
    Output('2d-graph', 'figure'),
    [Input('category-filter', 'value'),
     Input('time-scale-toggle', 'value'),
     Input('2d-graph', 'relayoutData')]
)
def update_figure(selected_categories, scale_type, relayoutData):
    use_log_scale = (scale_type == 'log')
    filtered_nodes = [node for node in nodes if node['category'] in selected_categories]
    scatter = create_scatter(selected_categories, use_log_scale)

    annotations = []
    show_text = False
    x_range = None
    y_range = None
    
    if relayoutData:
        if 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            x_range = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]
            show_text = (x_range[1] - x_range[0]) < 2  # Adjust this threshold as needed

        if 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            y_range = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']]

    for node in filtered_nodes:
        annotations.append(dict(
            x=node['log_year'] if use_log_scale else node['year'],
            y=node['complexity'],
            xref='x',
            yref='y',
            text=node['id'] if show_text else '',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-20,
            font=dict(color=node['color'])
        ))

    fig = go.Figure(data=[scatter], layout=layout)
    fig.update_layout(annotations=annotations)
    fig.update_xaxes(title='Logarithmic Scale' if use_log_scale else 'Linear Scale', type='linear')

    if x_range:
        fig.update_xaxes(range=x_range)
    if y_range:
        fig.update_yaxes(range=y_range)
    
    return fig

@app.callback(
    Output('node-info', 'children'),
    [Input('2d-graph', 'clickData')]
)
def display_node_info(clickData):
    if clickData:
        node_id = clickData['points'][0]['text']
        node = next(item for item in nodes if item['id'] == node_id)
        return [
            html.H2(node['id'], style={'color': node['color']}),
            html.P(f"Category: {node['category']}"),
            html.P(f"Complexity: {node['complexity']}"),
            html.P(f"Date: {node['date']}")
        ]
    return "Click a node to see more information here."

if __name__ == '__main__':
    app.run_server(debug=True)
