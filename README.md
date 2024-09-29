# Actividad 2 - Búsqueda y sistemas basados en reglas


Este proyecto utiliza **OSMnx**, **NetworkX**, y **Streamlit** para encontrar y visualizar la mejor ruta en la ciudad de Medellín, aplicando diferentes reglas de validación y optimización de rutas.

## Instalación

A continuación, se describen los pasos para configurar el entorno y ejecutar la aplicación.

### Requisitos previos

- Tener instalado **Conda**. Si aún no lo tienes, puedes descargarlo e instalarlo desde [Anaconda](https://www.anaconda.com/products/individual).

### Crear y activar el entorno

```bash
# Crear un entorno de Conda con los paquetes necesarios desde el canal conda-forge
conda create -n ox -c conda-forge --strict-channel-priority osmnx

# Activar el entorno recién creado
conda activate ox

# Instalar las dependencias adicionales necesarias como Streamlit y NetworkX
conda install -c conda-forge streamlit networkx

# Verificar que OSMnx se ha instalado correctamente
python -c "import osmnx; print(osmnx.__version__)"

# Ejecutar la aplicación de Streamlit
streamlit run main.py
