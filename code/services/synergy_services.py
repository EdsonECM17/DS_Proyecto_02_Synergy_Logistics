from typing import List

from processing.sl_filters import SynergyLogisticsFilters

class Service(SynergyLogisticsFilters):
    """
    Clase que contine servicios para el analisis de la tabla de Synergy Logistics.
    """
    def get_routes_list(self,  direction:str or None = None) -> List:
        """Genera una lista con todas las rutas diferentes de la tabla.
        
        Args:
            direction (str or None, optional): Dirección de transacción. Defaults to None.

        Returns:
            List: Lista con rutas con formato origen-destino.
        """
        routes_list = []
        # Filter tables by direction
        filtered_table = self.filter_routes_df(direction=direction)
        # Check row by row table
        for index, row in filtered_table.iterrows():
            # route=origin-destination
            route = (row['origin']+ "-" + row['destination'])
            if not route in routes_list:
                routes_list.append(route)
        return routes_list
    
    def get_total_elements(self, direction:str or None = None, year:int or None = None, transport_mode:str or None = None) -> int:
        """ 
        Cuenta el número de transacciones en una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.
            transport_mode (str or None, optional): Tipo de medio de transporte. Defaults to None.

        Returns:
            int: Total de casos en tabla filtrada. 
        """
        # Tabla filtrada
        filtered_table = self.filter_routes_df(direction=direction, start_year=year,
                                               end_year=year, transport_mode=transport_mode)
        # Contar filas en la tabla
        elements_count= len(filtered_table)
        return elements_count

    def get_route_frecuency(self, route:str, direction:str or None = None, year:int or None = None)-> int:
        """
        Cuenta las veces que una ruta aparece en una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

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
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction,
                                               start_year=year, end_year=year)
        # Contar filas en la tabla
        route_frecuency = len(filtered_table)
        return route_frecuency
        
    def get_total_value(self, direction:str or None = None, year:int or None = None, transport_mode: str or None = None) -> int:
        """
        Suma el valor total dentro de una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            route (str): Rutas con formato origen-destino.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.
            transport_mode (str or None, optional): Tipo de medio de transporte. Defaults to None.

        Returns:
            int: suma de valor de elementos en tabla filtrada.
        """
        filtered_table = self.filter_routes_df(direction=direction, start_year=year, end_year=year, transport_mode=transport_mode)
        total_value = filtered_table["total_value"].sum()
        return total_value

    def get_route_value(self, route:str, direction:str or None = None, year:int or None = None) -> int:
        """
        Suma el valor total para una ruta especifica dentro de una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            route (str): Rutas con formato origen-destino.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.
            transport_mode (str or None, optional): Tipo de medio de transporte. Defaults to None.

        Returns:
            int: suma de valor de elementos en tabla filtrada.
        """
        origin, destination = route.split("-")
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction,
                                               start_year=year, end_year=year)
        route_value = filtered_table["total_value"].sum()
        return route_value

    def get_top_ten(self, all_cases: dict) -> dict:
        """De un diccionario de elementos se obtienen los 10 casos con mejores resultados.

        Args:
            all_cases (dict): Diccionario con todos los casos

        Returns:
            List: Lista con los 10 casos con mejores resultados.  
        """
        top_ten_cases = sorted(all_cases, key=all_cases.get, reverse=True)[:10]
        top_ten_dict = {}
        for case in top_ten_cases:
            top_ten_dict[case] = all_cases[case]

        return top_ten_dict

    def get_transport_frecuency(self, transport:str, direction:str or None = None, year:int or None = None)-> int:
        """
        Cuenta las veces que un transporte aparece en una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            transport (str): Tipo de medio de transporte.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: Numero de apariciones de transporte en la tabla filtrada.
        """
        # Tabla filtrada
        filtered_table = self.filter_routes_df(transport_mode=transport, direction=direction,
                                               start_year=year, end_year=year)
        # Contar filas en la tabla
        transport_frecuency = len(filtered_table)
        return transport_frecuency
        

    def get_transport_value(self, transport:str, direction:str or None = None, year:int or None = None) -> int:
        """
        Suma el valor total para un transporte especifico dentro de una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            transport (str): Tipo de medio de transporte.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: suma de valor de elementos en tabla filtrada.
        """
        filtered_table = self.filter_routes_df(transport_mode=transport, direction=direction,
                                               start_year=year, end_year=year)
        transport_value = filtered_table["total_value"].sum()
        return transport_value


    def get_country_frecuency(self, origin:str or None = None, destination:str or None = None, direction:str or None = None, year:int or None = None)-> int:
        """
        Cuenta las veces que un pais aparece en una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            origin (str or None, optional): Pais de origen. Defaults to None.
            destination (str or None, optional): Pais de destino. Defaults to None.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: Numero de apariciones de transporte en la tabla filtrada.
        """
        # Tabla filtrada
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction,
                                               start_year=year, end_year=year)
        # Contar filas en la tabla
        transport_frecuency = len(filtered_table)
        return transport_frecuency
        

    def get_country_value(self, origin:str or None = None, destination:str or None = None, direction:str or None = None, year:int or None = None) -> int:
        """
        Suma el valor total para un pais especifico dentro de una tabla filtrada.
        Se pueden filtrar resultados por dirección, año y/o medio de transporte.

        Args:
            origin (str or None, optional): Pais de origen. Defaults to None.
            destination (str or None, optional): Pais de destino. Defaults to None.
            direction (str or None, optional): Dirección de transacción. Defaults to None.
            year (int or None, optional): Año de transacciones. Defaults to None.

        Returns:
            int: suma de valor de elementos en tabla filtrada.
        """
        filtered_table = self.filter_routes_df(origin=origin, destination=destination, direction=direction,
                                               start_year=year, end_year=year)
        transport_value = filtered_table["total_value"].sum()
        return transport_value

    def reorder_dict_max(self, data_dict: dict) -> dict:
        """
        Ordena diccionario a partir de valores de mayor a menor.
        Elimita los elementos del diccionario que tengan un valor de 0.

        Args:
            data_dict (dict): Diccionario de datos desordenados.

        Returns:
            dict: Diccionario de datos filtrados.
        """
        # Crear nuevo diccionario para almacenar datos ordenados
        ordered_data_dict = {}
        ordered_keys = sorted(data_dict, key=data_dict.get, reverse=True)
        for key in ordered_keys:
            # if value is 0, skip
            if data_dict[key] == 0:
                continue
            # if value > 0
            else:
                ordered_data_dict[key]=data_dict[key]
        return ordered_data_dict
