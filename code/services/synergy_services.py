from typing import List

from processing.sl_filters import SynergyLogisticsFilters

class Service(SynergyLogisticsFilters):
    """
    Clase que contine servicios para el analisis de la tabla de Synergy Logistics.
    """
    def get_routes_list(self) -> List:
        """Genera una lista con todas las rutas diferentes de la tabla.

        Returns:
            List: Lista con rutas con formato origen-destino.
        """
        routes_list = []
        # Check row by row table
        for index, row in self.SYNERGY_DB.iterrows():
            # route=origin-destination
            route = (row['origin']+ "-" + row['destination'])
            if not route in routes_list:
                routes_list.append(route)
        return routes_list

    def get_route_frecuency(self, route:str, direction:str or None = None, year:int or None = None)-> int:
        """
        Cuenta las veces que una ruta aparece en una tabla filtrada. La tabla puede filtrarse por
        dirección o por año.

        Args:
            route (str): Rutas con formato origen-destino.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: Numero de apariciones de ruta en la tabla filtrada.
        """
        # Obtener origen y destino para filtros
        origin, destination = route.split("-")
        # Tabla filtrada
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction, start_year=year, end_year=year)
        # Contar filas en la tabla
        route_frecuency = len(filtered_table)
        return route_frecuency

    def get_route_value(self, route:str, direction:str or None = None, year:int or None = None) -> int:
        """
        Suma el valor total para una ruta especifica dentro de una tabla filtrada.
        Se pueden filtrar resultados por dirección o año.

        Args:
            route (str): Rutas con formato origen-destino.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: suma de valor de elementos en tabla filtrada
        """
        origin, destination = route.split("-")
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction, start_year=year, end_year=year)
        route_value = filtered_table["total_value"].sum()
        return route_value

    def get_top_ten(self, all_cases: dict) -> List:
        """De un diccionario de elementos se obtienen los 10 casos con mejores resultados.

        Args:
            all_cases (dict): Diccionario con todos los casos

        Returns:
            List: Lista con los 10 casos con mejores resultados.  
        """
        top_ten_cases = sorted(all_cases, key=all_cases.get, reverse=True)[:10]
        return top_ten_cases
