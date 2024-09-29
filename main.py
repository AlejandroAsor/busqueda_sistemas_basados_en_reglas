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


def main():
    st.title("Mejor Ruta en el Transporte - Medellín")

    graph = ox.graph_from_place("Medellín, Colombia", network_type='drive')

    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.write("Introduce las coordenadas de origen:")
        src_lat = st.number_input("Latitud de origen", value=6.244203, format="%.6f")
        src_lon = st.number_input("Longitud de origen", value=-75.5812119, format="%.6f")

    with col2:
        st.write("Introduce las coordenadas de destino:")
        dest_lat = st.number_input("Latitud de destino", value=6.25184, format="%.6f")
        dest_lon = st.number_input("Longitud de destino", value=-75.56457, format="%.6f")

    if st.button('Verificar ubicaciones en el mapa'):
        map_data = pd.DataFrame({'lat': [src_lat, dest_lat], 'lon': [src_lon, dest_lon]})
        st.map(map_data)
        st.write("Si las ubicaciones son correctas, procede a obtener la mejor ruta.")

    if st.button('Obtener Mejor Ruta'):
        if (src_lat, src_lon) != (dest_lat, dest_lon):
            src_node = ox.distance.nearest_nodes(graph, src_lon, src_lat)
            dest_node = ox.distance.nearest_nodes(graph, dest_lon, dest_lat)

            shortest_path = get_best_route(graph, src_node, dest_node)

            if shortest_path:
                fig, ax = ox.plot_graph_route(graph, shortest_path, route_color="r", route_linewidth=3, node_size=0,
                                              figsize=(15, 15))
                st.pyplot(fig)
            else:
                st.write("No se encontró ninguna ruta posible.")
        else:
            st.write("El origen y el destino no pueden ser los mismos.")


if _name_ == "_main_":
    main()
