import osmnx as ox
import networkx as nx
import streamlit as st
import pandas as pd
from datetime import datetime

def check_street_maintenance(route, graph):
    """Regla: Si una calle está en mantenimiento, la ruta no es válida."""
    closed_streets = ['Calle 50', 'Avenida Principal']

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_data = graph.get_edge_data(u, v)
        if edge_data:
            for key in edge_data:
                if 'name' in edge_data[key] and edge_data[key]['name'] in closed_streets:
                    return False

    return True


def avoid_peak_hours():
    """Regla: Evita áreas congestionadas en horas pico."""
    now = datetime.now()
    if 7 <= now.hour <= 9 or 17 <= now.hour <= 19:
        return True
    return False
