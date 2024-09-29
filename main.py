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

def prefer_cheaper_routes(route, graph):
    """Regla: Prefiere rutas más baratas en función del atributo 'cost' de los segmentos."""
    route_cost = 0
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_data = graph.get_edge_data(u, v)
        if edge_data:
            for key in edge_data:
                if 'cost' in edge_data[key]:
                    route_cost += edge_data[key]['cost']
                else:
                    route_cost += 10  # Penalización por falta de datos
    return route_cost


def get_best_route(graph, orig_node, dest_node):
    try:
        all_routes = list(nx.all_shortest_paths(graph, orig_node, dest_node, weight='length'))
    except nx.NetworkXNoPath:
        return None  # Si no hay rutas, devolver None

    valid_routes = []

    for route in all_routes:
        if check_street_maintenance(route, graph) and not avoid_peak_hours():
            valid_routes.append(route)

    if valid_routes:
        # Devuelve la ruta más barata entre las válidas
        return min(valid_routes, key=lambda r: prefer_cheaper_routes(r, graph))
    else:
        # Si no hay rutas válidas, devolver la ruta más corta sin aplicar las reglas
        return min(all_routes, key=lambda r: prefer_cheaper_routes(r, graph))
