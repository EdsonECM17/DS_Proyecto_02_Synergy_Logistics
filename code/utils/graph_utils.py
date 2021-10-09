import os 

import plotly.graph_objects as go

# Comando necesario para usar librerias de imagenes fijas
os.environ["PATH"] = os.environ["PATH"] + f";{os.path.abspath('venv/lib/site-packages/kaleido/executable/')}"

class Chart:
    """
    Funciones generales para la generación de gráficas.
    """
    def save_as_image(self, fig, file_name: str):
        """ Esta función guarda una gráfica como imagen.
        Args:
            fig (plotly.graph_objects.Figure): Objeto de la gráfica creada.
            file_name (str): Ruta donde almacenar el archivo.
        """ 
        fig.write_image(file_name, width=1350, height=730)


class Summary_Chart(Chart):
    """
    Funciones para gráfica resultados de las consultas realizadas de las tablas de Lifestore.
    """
    def __init__(self, file_path: str) -> None:
        """Establece parametros default para objetos de la clase.

        Args:
            file_path (str): Ruta donde guardar gráficas.
        """
        super().__init__()
        # Definir folder donde se ubicaran las gráficas
        self.file_path = file_path
        # Agregar atributos de formato de gráfica (visualización)
        self.layout = go.Layout(
            title=dict(y=0.99, x=0.5, xanchor='center', yanchor='top'),
            xaxis=dict(showgrid=True, showline=True, linewidth=1,
                       linecolor='black', mirror=True, gridwidth=0.4,
                       gridcolor='rgb(204,209,208)', tickfont=dict(size=20),
                       type='category'),
            yaxis=dict(zeroline=False, showline=True, linewidth=1,
                       linecolor='black', mirror=True, gridwidth=0.4,
                       gridcolor='rgb(204, 209, 208)', tickfont=dict(size=20)),
            margin=dict(r=20, t=35),
            plot_bgcolor='rgba(0,0,0,0)', width=1080, height=566,
            font=dict(family='Arial, monospace', size=18))


    def bar_summary(self, data: dict, plot_title: str, x_axis_name: str, y_axis_name: str,
                    file_name: str, color:str = "blue") -> None:
        """Gráfica de barras a partir de un diccionario.

        Args:
            data (dict): Datos a graficar.
            plot_title (str): Titulo de la gráfica.
            x_axis_name (str): Nombre de eje x.
            y_axis_name (str): Nombre de eje y.
            file_name (str): Nombre del archivo.
            color (str, optional): Color del gráfico. Defaults to "blue".
        """          
        # Se da de alta diccionario con colores disponibles
        color_dict = {"blue": "rgb(15, 78, 171)", "green": "rgb(15, 171, 72)",
                      "red": "rgb(232, 4, 0)", "purple": "rgb(109, 15, 171)",
                      "yellow": "rgb(199, 199, 18)", "orange": "rgb(232, 155, 0)"}
        # Seleccionar color del gráfico
        plot_color = color_dict[color] 

        # Separar diccionarios en dos listas, una para cada eje
        x_data = list(data.keys())
        y_data = list(data.values())

        # Generar objeto de gráfica
        plot_bar = go.Bar(x=x_data, y=y_data)
        mydata = [plot_bar]

        # Formato de la grafica de barras
        fig = go.Figure(data=mydata, layout=self.layout)
        
        # Actualizar color del grafico
        fig.update_traces(marker_color=plot_color, marker_line_color=plot_color)
        # Actualizar gráfico con datos de entrada
        fig.update_layout(
            title_text=plot_title,
            xaxis_title=x_axis_name,
            yaxis_title=y_axis_name)

        # Validar si folder existe, o si es necesario crearlo
        if not os.path.exists(f"{self.file_path}"):
            os.makedirs(f"{self.file_path}")
        # Guardar grafico interactivo como html
        fig.write_html(f"{self.file_path}/{file_name}.html")
        # Guardar imagen statica en
        self.save_as_image(fig, f"{self.file_path}/{file_name}.png")
        # Indicar a usuario en consola
        print(f"Resultado gráficado en {self.file_path}/{file_name}.png")
