"""CSC111 Winter 2023: Final Project
Creates the visualizations.
===============================
This module contains a collection of Python classes and functions that we used
represent a series of trees and graphs.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Stefan Ateljevic, Veda Kesarwani, Sydelle Mago, and Vrinda Subhash.
"""
from __future__ import annotations

# import csv
# from datetime import date, datetime
# from python_ta.contracts import check_contracts
import pandas as pd
import folium
from igraph import Graph
import plotly.graph_objects as go
from node import Node
from data_computations import get_total_cases


###############################################################################
# Visualization
###############################################################################

def map_canada_with_cases(root: Node) -> folium.Map:
    """A method that creates a map of Canada and displays the provinces' COVID-19 information.
    """
    canada_map = folium.Map(location=[56.13, -106.35], tiles="OpenStreetMap", zoom_start=3)

    data = pd.DataFrame({
        'lon': [53.9333, 53.7267, 53.7609, 46.5653, 53.1355, 64.8255, 44.6816, 66.1605, 51.2538, 46.5107, 46.8033,
                52.9399, 64.2823],
        'lat': [-116.5765, -127.6476, -98.8139, -66.4619, -57.6604, -124.8457, -63.7443, -153.3691, -85.3232, -63.4168,
                -71.1631, -106.4509, -135.0000],
        'name': ['Alberta', 'BC', 'Manitoba', 'New Brunswick', 'NL',
                 'NWT', 'Nova Scotia', 'Nunavut', 'Ontario', 'PEI',
                 'Quebec', 'Saskatchewan', 'Yukon'],
        'cases': [get_total_cases(root, 'Alberta'), get_total_cases(root, 'BC'),
                  get_total_cases(root, 'Manitoba'), get_total_cases(root, 'New Brunswick'),
                  get_total_cases(root, 'NL'), get_total_cases(root, 'NWT'),
                  get_total_cases(root, 'Nova Scotia'), get_total_cases(root, 'Nunavut'),
                  get_total_cases(root, 'Ontario'), get_total_cases(root, 'PEI'),
                  get_total_cases(root, 'Quebec'), get_total_cases(root, 'Saskatchewan'),
                  get_total_cases(root, 'Yukon')]
    })

    for _, row in data.iterrows():
        folium.Marker([row['lon'], row['lat']], popup=row['name'] + ' ' + str(row['cases'])).add_to(canada_map)

    canada_map.save('canada-covid-cases.html')
    return canada_map


# TREE VISUAL
def plot_tree(root: Node) -> None:
    """A function that creates a tree-plot of the provinces in Canada and their COVID-19 information.
    # >>> canada = Node('Canada', 0)
    # >>> create_provinces(canada)
    # >>> populate_canada_data('datasets/alberta_small_data_set.csv', canada)
    # >>> plot_tree(canada)
    """
    province = [get_total_cases(root, 'Ontario'), get_total_cases(root, 'Quebec'),
                get_total_cases(root, 'BC'), get_total_cases(root, 'Alberta'),
                get_total_cases(root, 'Manitoba'), get_total_cases(root, 'Saskatchewan'),
                get_total_cases(root, 'Nova Scotia'), get_total_cases(root, 'New Brunswick'),
                get_total_cases(root, 'NL'), get_total_cases(root, 'PEI'),
                get_total_cases(root, 'Nunavut'), get_total_cases(root, 'NWT'),
                get_total_cases(root, 'Yukon')]

    v_label = [sum([i for i in province if i is not None]), get_total_cases(root, 'Ontario'),
               get_total_cases(root, 'Quebec'),
               get_total_cases(root, 'BC'), get_total_cases(root, 'Alberta'),
               get_total_cases(root, 'Manitoba'), get_total_cases(root, 'Saskatchewan'),
               get_total_cases(root, 'Nova Scotia'), get_total_cases(root, 'New Brunswick'),
               get_total_cases(root, 'NL'), get_total_cases(root, 'PEI'),
               get_total_cases(root, 'Nunavut'), get_total_cases(root, 'NWT'),
               get_total_cases(root, 'Yukon')]

    graph = Graph.Tree(len(root.children), 13)

    pos = {k: graph.layout('rt')[k] for k in range(len(root.children))}
    y_values = [graph.layout('rt')[k][1] for k in range(len(root.children))]

    x_n = [pos[k][0] for k in pos]
    y_n = [2 * max(y_values) - pos[k][1] for k in pos]
    x_e = []
    y_e = []
    for edge in [e.tuple for e in graph.es]:
        x_e += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_e += [2 * max(y_values) - pos[edge[0]][1], 2 * max(y_values) - pos[edge[1]][1], None]

    labels = v_label

    # creating Plotly traces

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_e,
                             y=y_e,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=x_n,
                             y=y_n,
                             mode='markers',
                             name='provinces',
                             marker=dict(symbol='circle-dot',
                                         size=75,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             hovertemplate='%{text}<br>' + 'Cases',
                             opacity=0.8
                             ))

    # Making annotations
    def make_annotations(pos: dict, text: list, font_size: int = 10, font_color: str = 'rgb(250,250,250)') -> \
            list[dict[str, int | str | dict[str, str | int | bool]]]:
        """This method names the subtrees in the tree.
        """
        names = []
        province = ['Ontario', 'Quebec', 'BC', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia',
                    'New Brunswick', 'NL', 'PEI', 'Nunavut', 'NWT', 'Yukon']

        names.append(
            dict(
                text='Canada',
                x=pos[0][0], y=2 * max(y_values) - pos[0][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )

        for k in range(1, len(root.children)):
            names.append(
                dict(
                    text=province[k - 1],
                    x=pos[k][0], y=2 * max(y_values) - pos[k][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )

        return names

    # Adding axis specifications and creating the layout
    axis = dict(showline=True,  # hide axis line, grid, ticklabels and  title
                zeroline=True,
                showgrid=True,
                showticklabels=True,
                )

    fig.update_layout(title='COVID-19 Spread in Canada During the 2020-2021 Holiday Season',
                      annotations=make_annotations(pos=pos, text=v_label),  # This is where parameter text is used.
                      font_size=12,
                      showlegend=True,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()
