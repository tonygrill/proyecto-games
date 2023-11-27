from fastapi import FastAPI, HTTPException, Query
from typing import Dict, List, Union
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



app = FastAPI()

# Cargamos el archivo a un Dataframe
df = pd.read_parquet('steam_games.parquet')

@app.get('/playtime_genre', tags=['PlayTimeGenre'])
def PlayTimeGenre(genre: str = Query(..., title="Género del juego")) -> Dict[str, int]:
    """
    Obtiene el año con la mayor cantidad de horas jugadas para un género de juegos específico.

    Parameters:
    - genre (str): El género del juego para el cual se desea obtener la información.

    Returns:
    Dict[str, int]: Un diccionario que contiene el año con la mayor cantidad de horas jugadas
                   para el género proporcionado.
    
    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no se encuentren datos para el género proporcionado
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Obtener todas las columnas que comienzan con el nombre del género
        genre_columns = [col for col in df.columns if col.lower().startswith(genre.lower())]

        # Verificar si se encontraron columnas para el género proporcionado
        if not genre_columns:
            raise HTTPException(status_code=400, detail=f"No se encontraron datos para el género {genre}")

        # Filtrar el DataFrame por las columnas del género proporcionado
        genre_df = df[['year'] + genre_columns]

        # Agrupar por año y sumar las horas jugadas
        genre_year_playtime = genre_df.groupby('year')[genre_columns].sum()

        # Encontrar el año con más horas jugadas
        max_playtime_year = genre_year_playtime.idxmax().values[0]

        print("Género Columns:", genre_columns)
        print("DataFrame Filtrado:")
        print(genre_df)
        print("Agrupación por Año:")
        print(genre_year_playtime)

        # Devolver un diccionario como respuesta
        return {"most_played_year": max_playtime_year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get('/user_for_genre', tags=['UserForGenre'])
def UserForGenre(genre: str = Query(..., title="Género del juego")):
    """
    Obtiene información sobre el usuario con más horas jugadas para un género de juegos específico.

    Parameters:
    - genre (str): El género del juego para el cual se desea obtener la información.

    Returns:
    Dict: Un diccionario que contiene el usuario con más horas jugadas y una lista de acumulación
          de horas jugadas por año para el género proporcionado.
          Estructura del diccionario:
          {
              "Usuario con más horas jugadas para [genre]": [user_id],
              "Horas jugadas": [{"Año": [year], "Horas": [hours]}, ...]
          }
    
    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no se encuentren datos para el género proporcionado
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Filtrar el DataFrame por el género proporcionado
        genre_df = df[df[genre] == 1]

        if genre_df.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos para el género: {genre}")

        # Encontrar el usuario con más horas jugadas
        max_played_user = genre_df.loc[genre_df['playtime_forever'].idxmax()]['user_id']

        # Agrupar por año y sumar las horas jugadas
        genre_year_playtime = genre_df.groupby('year')['playtime_forever'].sum()

        # Crear la lista de acumulación de horas jugadas por año
        playtime_list = [{"Año": year, "Horas": hours} for year, hours in genre_year_playtime.items()]

        return {
            "Usuario con más horas jugadas para {}".format(genre): max_played_user,
            "Horas jugadas": playtime_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/users_recommend', tags=['UsersRecommend'])
def UsersRecommend(year: int) -> List[Dict[str, str]]:
    """
    Obtiene la lista de los juegos más recomendados para un año específico.

    Parameters:
    - year (int): El año para el cual se desean obtener las recomendaciones.

    Returns:
    List[Dict[str, str]]: Una lista de diccionarios que contiene la posición y el nombre de los juegos
                         más recomendados para el año proporcionado.
                         Estructura de cada diccionario:
                         {"Puesto [posición]": [nombre del juego]}
    
    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no haya juegos recomendados para el año proporcionado
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Filtrar el DataFrame por el año y juegos recomendados
        recommend_df = df[(df['year'] == year) & (df['recommend'] == True)]

        if recommend_df.empty:
            raise HTTPException(status_code=404, detail=f"No hay juegos recomendados para el año {year}")

        # Ordenar los juegos por algún criterio (por ejemplo, nombre del juego)
        recommend_df = recommend_df.sort_values(by='item_name', ascending=True)

        # Tomar los top 3 juegos recomendados
        top3_recommendations = recommend_df.head(3)['item_name'].tolist()

        # Crear el formato de retorno
        result = [{"Puesto {}".format(i + 1): game} for i, game in enumerate(top3_recommendations)]

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/worst_developer', tags=['UsersWorstDeveloper'])
def UsersWorstDeveloper(year: int = Query(..., title="Año del juego")) -> List[Dict[str, Union[str, int]]]:
    """
    Obtiene la lista de las desarrolladoras con los juegos menos recomendados y comentarios negativos
    para un año específico.

    Parameters:
    - year (int): El año para el cual se desean obtener las desarrolladoras con los peores juegos.

    Returns:
    List[Dict[str, Union[str, int]]]: Una lista de diccionarios que contiene la posición y el nombre de las desarrolladoras
                                      con los juegos menos recomendados y comentarios negativos para el año proporcionado.
                                      Estructura de cada diccionario:
                                      {"Puesto [posición]": [nombre de la desarrolladora]}
    
    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no haya datos para el año proporcionado
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Filtrar el DataFrame por el año proporcionado, juegos no recomendados y comentarios negativos
        filtered_df = df[(df['year'] == year) & (df['recommend'] == False) & (df['sentiment_analysis'] == 0)]

        if filtered_df.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos para el año {year}")

        # Obtener el top 3 de desarrolladoras con juegos menos recomendados y comentarios negativos
        top_worst_developers = (
            filtered_df.groupby('developer')['recommend']
            .count().sort_values().head(3).index.tolist()
        )

        # Crear la lista de resultados
        result_list = [{"Puesto {}".format(i + 1): developer} for i, developer in enumerate(top_worst_developers)]

        return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/sentiment_analysis', tags=['SentimentAnalysis'])
def sentiment_analysis(developer: str = Query(..., title="Empresa desarrolladora")) -> List[Dict[str, Union[str, int]]]:
    """
    Realiza un análisis de sentimiento para los juegos de una empresa desarrolladora específica.

    Parameters:
    - developer (str): El nombre de la empresa desarrolladora para la cual se realizará el análisis.

    Returns:
    List[Dict[str, Union[str, int]]]: Una lista de diccionarios que contiene la información del análisis de sentimiento
                                      para los juegos de la empresa desarrolladora proporcionada. Cada diccionario tiene
                                      las siguientes claves:
                                      - "Developer": Nombre de la empresa desarrolladora.
                                      - "Sentiment": Categoría de sentimiento (positivo, negativo o neutro).
                                      - "Count": Número de registros en la categoría de sentimiento.

    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no haya datos para la empresa desarrolladora proporcionada
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Filtrar el DataFrame por la empresa desarrolladora proporcionada
        filtered_df = df[df['developer'] == developer]

        if filtered_df.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos para la empresa desarrolladora: {developer}")

        # Realizar el análisis de sentimiento y contar los registros por categoría
        sentiment_counts = filtered_df['sentiment_analysis'].value_counts().to_dict()

        # Crear la lista de resultados
        result_list = [{"Developer": developer, "Sentiment": sentiment, "Count": count} for sentiment, count in sentiment_counts.items()]

        return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


