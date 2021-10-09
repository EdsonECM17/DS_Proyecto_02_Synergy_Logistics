from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from datetime import datetime

# Definir ubicación de archivo CSV
DATA_FILE_PATH = "data\synergy_logistics_database.csv"

class SynergyLogisticsFilters():
    def __init__(self) -> None:
        """Lectura de la BD de Synergy Logistics.
        """
        self.SYNERGY_DB = pd.read_csv(DATA_FILE_PATH, index_col="register_id")
        # Convert date column to datetime objects
        self.SYNERGY_DB["date"] = pd.to_datetime(self.SYNERGY_DB["date"])

    def filter_routes_df(self, direction: str or None = None,
                         origin: str or None = None, destination: str or None = None,
                         start_year: int or None = None, end_year: int or None = None,
                         start_date: str or None = None, end_date: str or None = None,
                         product: str or None = None, transport_mode: str or None = None,
                         company_name: str or None = None, min_value: int or None = None,
                         max_value: int or None = None) -> DataFrame:
        """
        Filtra el dataframe de Synergy Logistics de acuerdo a valores en las columnas que tiene
        la tabla generada. Si no hay filtro, se regresa un dataframe completo.

        Args:
            direction (str or None, optional): Tipo de dirección (Import o Export). Defaults to None.
            origin (str or None, optional): Pais de origen. Defaults to None.
            destination (str or None, optional): Pais de destino. Defaults to None.
            start_year (int or None, optional): Año inicial de periodo. Defaults to None.
            end_year (int or None, optional): Año final de periodo. Defaults to None.
            start_date (str or None, optional): Fecha inicial de periodo. Defaults to None.
            end_date (str or None, optional): Fecha final de periodo. Defaults to None.
            product (str or None, optional): Tipo de producto. Defaults to None.
            transport_mode (str or None, optional): Tipo de medio de transporte. Defaults to None.
            company_name (str or None, optional): Nombre de compañia. Defaults to None.
            min_value (int or None, optional): Valor minimo. Defaults to None.
            max_value (int or None, optional): Valor maximo. Defaults to None.

        Returns:
            DataFrame:  Dataframe con columnas de la tabla que cumplen con los filtros indicados.
        """
        routes_table = self.SYNERGY_DB
        # Get valid cases for string filters from unique values of each str column
        direction_cases = list(routes_table["direction"].unique())
        origin_countries = list(routes_table["origin"].unique())
        destination_countries = list(routes_table["destination"].unique())
        years = list(range(routes_table["year"].min(), datetime.now().year))
        product_types = list(routes_table["product"].unique())
        transport_modes = list(routes_table["transport_mode"].unique())
        companies = list(routes_table["company_name"].unique())
        date_format = '%d/%m/%Y'
        # Add filter to column if valid input is given
        # Dirección
        if direction is not None:
            if direction in direction_cases:
                routes_table=routes_table[routes_table["direction"] == direction]
            else:
                print(f"El valor '{direction}' no es un filtro valido para la columna direction.")
        # Origen
        if origin is not None:
            if origin in origin_countries:
                routes_table=routes_table[routes_table["origin"] == origin]
            else:
                print(f"El valor '{origin}' no es un filtro valido para la columna origin.")
        # Destino
        if destination is not None:
            if destination in destination_countries:
                routes_table=routes_table[routes_table["destination"] == destination]
            else:
                print(f"El valor '{destination}' no es un filtro valido para la columna destination.")
        # Year
        if start_year is not None:
            if start_year in years:
                routes_table=routes_table[routes_table["year"] >= start_date]
            else:
                print(f"El valor '{start_year}' no es un año valido para la columna year.")
        if end_year is not None:
            if end_year in years:
                routes_table=routes_table[routes_table["year"] <= end_date]
            else:
                print(f"El valor '{end_year}' no es un año valido para la columna year.")
        # Date
        if start_date is not None:
            try:
                datetime.strptime(start_date, date_format)
                routes_table=routes_table[routes_table["date"] >= start_date]
            except ValueError:
                print("Fecha invalida. Debe usarse el formato DD/MM/YYYY")
        if end_date is not None:
            try:
                datetime.strptime(end_date, date_format)
                routes_table=routes_table[routes_table["date"] <= end_date]
            except ValueError:
                print("Fecha invalida. Debe usarse el formato DD/MM/YYYY")
        # Producto
        if product is not None:
            if product in product_types:
                routes_table=routes_table[routes_table["product"] == product]
            else:
                print(f"El valor '{product}' no es un filtro valido para la columna product.")
        # Modo de transporte
        if transport_mode is not None:
            if transport_mode in transport_modes:
                routes_table=routes_table[routes_table["transport_mode"] == transport_mode]
            else:
                print(f"El valor '{transport_mode}' no es un filtro valido para la columna product.")
        # Nombre de Compañia
        if company_name is not None:
            if company_name in companies:
                routes_table=routes_table[routes_table["company_name"] == company_name]
            else:
                print(f"El valor '{company_name}' no es un filtro valido para la columna company_name.")
        # Valor total
        if min_value is not None:
            routes_table=routes_table[routes_table["total_value"] >= min_value]
        if max_value is not None:
            routes_table=routes_table[routes_table["total_value"] <= max_value]

        return routes_table
        

    def get_unique_values(self, category:str) -> List:
        """Genera lista con valores unicos de columna de la base de datos.

        Args:
            category (str): Nombre de la columna.

        Returns:
            List: Valores unicos en columna de la tabla.
        """
        # Si elemento es columna de la tabla, obtiene valores distintos. 
        if category in self.SYNERGY_DB.columns.values.tolist():
            unique_column_values = list(self.SYNERGY_DB[category].unique())
        else:
            print("La categoría indicada no existe dentro de la Base de Datos")
            unique_column_values = []
        return unique_column_values
