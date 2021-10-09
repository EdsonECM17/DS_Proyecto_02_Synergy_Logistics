import pandas as pd
import os

from processing.sl_filters import SynergyLogisticsFilters
from utils.graph_utils import Summary_Chart
from services.synergy_services import Service

# Definir constantes
DIRECCIONES = [None, "Imports", "Exports"] # None se refiere a ambas dirrecciones juntas
PERIODO_TIEMPO = [None, 2015, 2016, 2017, 2018, 2019, 2020] # Con None se analizan todos los años
OUTPUT_INITIAL_PATH = "exploration"

# Crear objeto de la clase Services para las consultas
service = Service()

# Opcion 1: 10 rutas más demandas
# Analisis para todas las rutas (import + export)
# Consultar rutas difentes
all_routes = service.get_routes_list()
print(f"Hay {len(all_routes)} rutas diferentes.")
# Analizar para cada dirección, cada periodo, y cada ruta
for direction in DIRECCIONES:
    # Init main summaries (year, pct of transacction, pct of value)
    year_list = []
    value_pct_list = []
    frecuency_pct_list = []
    # Manejo de casos none (volver str)
    if direction is None:
        direction_str = "All"
    else:
        direction_str = direction
    
    # Ruta para almacenar resultados
    output_folder = f"{OUTPUT_INITIAL_PATH}/opcion1/{direction_str}"
    
    for year in PERIODO_TIEMPO:
        # Init dict to store results
        route_frecuency = {}
        route_value = {}
        route_frecuency_pct = {}
        route_value_pct =  {}
        # Calcular total para caso analizado (para usar en  porcentajes de rutas)
        total_cases = service.get_total_elements(direction=direction, year=year) 
        total_value = service.get_total_value(direction=direction, year=year)
        for route in all_routes:
            # Para cada ruta consultar frencuencia y valor total
            route_frecuency[route] = service.get_route_frecuency(route, direction=direction, year=year)
            route_value[route] = service.get_route_value(route, direction=direction, year=year)
            # Calcular porcentaje de resultados de ruta respecto a totales para el caso
            route_frecuency_pct[route] = round((route_frecuency[route]/total_cases)*100, 2)
            route_value_pct[route] = round((route_value[route]/total_value)*100, 2)

        # Obtener top ten en valor y frecuencia
        top_ten_frecuency = service.get_top_ten(route_frecuency)
        top_ten_value = service.get_top_ten(route_value)
        top_ten_frecuency_pct = service.get_top_ten(route_frecuency_pct)
        top_ten_value_pct = service.get_top_ten(route_value_pct)
        # Manejo de casos none (volver str)           
        if year is None:
            year_str = "All"
        else:
            year_str = str(year)
        # Imprimir rutas con mejor valor y más uso
        print(f"Opción 1 - Direccion: {direction_str}, Año: {year_str} ")
        print("Rutas más utilizadas:")
        i=1
        for route in top_ten_frecuency.keys():
            print(f"{i}.- {route}: {top_ten_frecuency[route]}")
            i+=1
        print("Rutas mejor valoradas:")
        i=1
        for route in top_ten_value.keys():
            print(f"{i}.- {route}: {top_ten_value[route]}")
            i+=1
        print("")
         # Definir folder para almacenar resultados y crear si no existe
        output_folder_year = f"{output_folder}/{year_str}"
        if not os.path.exists(f"{output_folder_year}"):
            os.makedirs(f"{output_folder_year}")
        # Almacenar resultados como CSV
        # Todas las rutas
        data = {'route': list(route_frecuency.keys()), 'frecuency':list(route_frecuency.values()),
                'frecuency_pct':list(route_frecuency_pct.values()), 'total_value':list(route_value.values()),
                'total_value_pct':list(route_value_pct.values())}
        pd.DataFrame(data).to_csv(output_folder_year+"/results.csv", index=False)
        # Top 10 en frecuency
        data = {'route': list(top_ten_frecuency.keys()), 'frecuency':list(top_ten_frecuency.values()), 'frecuency_pct':list(top_ten_frecuency_pct.values())}
        pd.DataFrame(data).to_csv(output_folder_year+"/top10_frec.csv", index=False)
        # Top 10 en valor
        data = {'route': list(top_ten_value.keys()), 'total_value':list(top_ten_value.values()), 'total_value_pct':list(top_ten_value_pct.values())}
        pd.DataFrame(data).to_csv(output_folder_year+"/top10_value.csv", index=False)
        # Graficar resultados
        plot = Summary_Chart(output_folder_year)
        plot.h_bar_summary(top_ten_frecuency, f"Rutas con mayor demanda", "No. de Apariciones",
                           "Rutas", "ruta_frec")
        plot.h_bar_summary(top_ten_value, f"Rutas con mayor valor", "Valor total", "Rutas",
                           "ruta_valor", "green")
        plot.h_bar_summary(top_ten_frecuency_pct, f"Rutas con mayor demanda", "Apariciones (%)",
                           "Rutas", "ruta_frec_pct", "purple")
        plot.h_bar_summary(top_ten_value_pct, f"Rutas con mayor valor", "Valor total (%)", "Rutas",
                           "ruta_valor_pct", "purple")
        # Resumen del periodo
        year_list.append(year_str)
        value_pct_list.append(sum(top_ten_value_pct.values()))
        frecuency_pct_list.append(sum(top_ten_frecuency_pct.values()))
    # Resumen multianual
    data = {'year': year_list, 'frecunecy_pct':frecuency_pct_list, 'total_value_pct':value_pct_list}
    pd.DataFrame(data).to_csv(output_folder+"/summary.csv", index=False)

# Opcion 2: Medios de transporte mas importantes


# Opcion 3: Paises que generen mayor valor

