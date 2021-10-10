import pandas as pd
import os

from processing.sl_filters import SynergyLogisticsFilters
from utils.graph_utils import Summary_Chart
from services.synergy_services import Service


# Crear objeto de la clase Services para las consultas
service = Service()

# Definir constantes relacionadas a la DB y los analisis a realizar
DIRECCIONES = [None, "Imports", "Exports"] # None se refiere a ambas dirrecciones juntas
PERIODO_TIEMPO = [None, 2015, 2016, 2017, 2018, 2019, 2020] # Con None se analizan todos los años
TRANSPORT_MODES = service.get_unique_values("transport_mode")  # Lista de medios de transporte
ORINGIN_COUNTRIES = service.get_unique_values("origin")  # Lista de paises de origen
DESTINATION_COUNTRIES = service.get_unique_values("destination")  # Lista de paises de destino
ROUTES = service.get_routes_list()  # Lista de rutas

# Definir constantes relacionadas a la administración de archivos
OUTPUT_INITIAL_PATH = "exploration"

# Opcion 1: 10 rutas más demandadas
print(f"Hay {len(ROUTES)} rutas diferentes.")
# Analizar demanda general y para direcciones especificas (import/export)
# Se analizaran el no. de apiriciones de la ruta en la tabla y el valor de esas apariciones, los 
# factores se expresaran como no. entero y como porcentaje del total para el periodo y dirección analizados.
for direction in DIRECCIONES:
    # Inicializar variables prinicipales de resumen
    year_list = []
    value_pct_list = []
    frecuency_pct_list = []
    # Manejo de casos none (crear str)
    if direction is None:
        direction_str = "All"
    else:
        direction_str = direction
    # Ruta para almacenar resultados
    output_folder = f"{OUTPUT_INITIAL_PATH}/opcion_1/{direction_str}"
    # Para cada caso, analizar el periodo completo (2015-2020) y por año
    for year in PERIODO_TIEMPO:
        # Inicializar variable del resumen de cada periodo
        route_frecuency = {}
        route_value = {}
        route_frecuency_pct = {}
        route_value_pct =  {}
        # Calcular totales para no. de apariciones y valor en direccion y año considerados
        # Este valor se utilizara para expresar frecuencia y valor tambien como porcentajes
        total_cases = service.get_total_elements(direction=direction, year=year) 
        total_value = service.get_total_value(direction=direction, year=year)
        # Dentro del periodo indicado se analiza frecuencia y valor ruta por ruta
        for route in ROUTES:
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
# Se analizaran el no. de apiriciones del transporte en la tabla y el valor de esas apariciones, los 
# factores se expresaran como no. entero y como porcentaje del total para el periodo y dirección analizados.
print("OPCION 2:\n")
for direction in DIRECCIONES:
    # Manejo de casos none (crear str)
    if direction is None:
        direction_str = "All"
    else:
        direction_str = direction
    # Ruta para almacenar resultados
    output_folder = f"{OUTPUT_INITIAL_PATH}/opcion_2/{direction_str}"
    # Para cada caso, analizar el periodo completo (2015-2020) y por año
    for year in PERIODO_TIEMPO:
        # Inicializar variable del resumen de cada periodo
        transport_frecuency = {}
        transport_value = {}
        transport_frecuency_pct = {}
        transport_value_pct =  {}
        # Calcular totales para no. de apariciones y valor en direccion y año considerados
        # Este valor se utilizara para expresar frecuencia y valor tambien como porcentajes
        total_cases = service.get_total_elements(direction=direction, year=year) 
        total_value = service.get_total_value(direction=direction, year=year)
        # Dentro del periodo indicado se analiza frecuencia y valor ruta por ruta
        for transport in TRANSPORT_MODES:
            # Para cada ruta consultar frencuencia y valor total
            transport_frecuency[transport] = service.get_transport_frecuency(transport, direction=direction, year=year)
            transport_value[transport] = service.get_transport_value(transport, direction=direction, year=year)
            # Calcular porcentaje de resultados de ruta respecto a totales para el caso
            transport_frecuency_pct[transport] = round((transport_frecuency[transport]/total_cases)*100, 2)
            transport_value_pct[transport] = round((transport_value[transport]/total_value)*100, 2)
        # Manejo de casos none (volver str)           
        if year is None:
            year_str = "All"
        else:
            year_str = str(year)
        # Imprimir rutas con mejor valor y más uso
        print(f"Opción 2 - Direccion: {direction_str}, Año: {year_str} ")
        print("Transportes más utilizadas:")
        i=1
        for transport in transport_frecuency.keys():
            print(f"{i}.- {transport}. {transport_frecuency[transport]}. Valor: {transport_value[transport]}")
            i+=1
        print("")
         # Definir folder para almacenar resultados y crear si no existe
        output_folder_year = f"{output_folder}/{year_str}"
        if not os.path.exists(f"{output_folder_year}"):
            os.makedirs(f"{output_folder_year}")
        # Almacenar resultados como CSV
        # Todas las rutas
        data = {'transport': list(transport_frecuency.keys()), 'frecuency':list(transport_frecuency.values()),
                'frecuency_pct':list(transport_frecuency_pct.values()), 'total_value':list(transport_value.values()),
                'total_value_pct':list(transport_value_pct.values())}
        pd.DataFrame(data).to_csv(output_folder_year+"/results.csv", index=False)
        # Graficar resultados
        plot = Summary_Chart(output_folder_year)
        plot.pie_summary(transport_frecuency, "Transporte con mayor demanda", "transporte_frec")
        plot.pie_summary(transport_value, "Transporte con mayor valor", "transporte_valor")

# Opcion 3: Paises que generen mayor valor

