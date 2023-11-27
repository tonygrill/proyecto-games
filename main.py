from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Dict, List, Union
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



app = FastAPI()

# Cargamos el archivo a un Dataframe
df = pd.read_parquet('steam_games.parquet')




# Obtén los datos una sola vez y utilízalos en las funciones que los necesiten
df_items_unicos = df[['item_id', 'item_name', 'Action', 'Indie']]
df_items_unicos.set_index('item_id', inplace=True)
df_similitud = cosine_similarity(df_items_unicos[['Action', 'Indie']])

@app.get('/recommend_games', tags=['RecommendGames'])
def recommend_games(item_id: int = Query(..., title="ID del juego")) -> List[str]:
    """
    Obtiene una lista de juegos recomendados para un juego específico basándose en similitud de ítems.

    Parameters:
    - item_id (int): El ID del juego para el cual se desea obtener recomendaciones.

    Returns:
    List[str]: Una lista de nombres de juegos recomendados para el juego especificado.

    Raises:
    HTTPException: Se genera una excepción HTTP en caso de que no se encuentre información para el 'item_id' proporcionado
                  o si ocurre algún otro error durante la ejecución.
    """
    try:
        # Verificar si el 'item_id' existe
        if item_id not in df_items_unicos.index:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el juego con item_id '{item_id}'")
        
        # Obtener la fila de similitud correspondiente solo para las columnas 'Action' y 'Indie'
        fila_similitud = df_similitud[df_items_unicos.index.get_loc(item_id)]

        # Obtener los 'item_id' recomendados ordenados por similitud en orden descendente y seleccionar los primeros n
        juegos_recomendados = df_items_unicos.index[fila_similitud.argsort()[::-1][:5]].tolist()

        # Obtener los 'item_name' correspondientes a los 'item_id' recomendados
        juegos_recomendados_nombres = df_items_unicos.loc[juegos_recomendados, 'item_name'].tolist()
        
        return juegos_recomendados_nombres
    except KeyError as ke:
        raise HTTPException(status_code=500, detail=f"Error de clave: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
