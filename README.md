En este trabajo buscamos la eficiencia en cuanto a los recursos se refiere, será nuestra premisa para abordar los requerimientos necesarios y asi cumplir con las demandas de nuestro cliente.

Nuestro cliente necesita desplegar una API en un servicio web gratuito, los requerimientos incluyen 5 funciones y un sistema de recomendación, los que podemos desglosar de la siguinte manera:

ENDPOINTS:

-PlayTimeGenre: Se ingresa el el genero y retorna el año con mas horas juagadas para dicho juego.

-UserForGenre: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

-UsersRecommend: Debe retornar los 3 juegos mas recomendados por el usuario.

-UsersRecommend: Ingresado el año, debe retornar los 3 desarolladores menos recomendados para dicho año.

-UsersWorstDeveloper: Debido ingreso de la empresa desarrolladora, debe devolver diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de eseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor. 

El sistema de recomendación Item-Item mediante la aplicación de la similitud del coseno, debe recomnedar (dado el item) una lista de 5 juegos similares al item ingresado.

Para cumplir este proposito declinamods por el uso de FastAPI, debido a su simplicidad y entorno ligero.

La materia prima entregada por el cliente son 3 dataset em formato JSON, los cuales buscaremos reducir de manera justificada para su implementación en el servicio gratuito.

El proceso de desanidación de estos datasets la pueden entontrar en los archivos ETL_steam_games.ipynb, ETL_user_items.ipynb y ETL_users_reviews.ipynb, todo fue realizado en unnambiente de jupyter y python.

en el archivo adjunto union.ipynb encontraremos de manera detallada como fue posible juntar estos datasets mediante sus campos en común, por otra parte en el archivo EDA.ipynb se encuentra el EDA de nuestro proyecto.

En el siguiente enlace pueden encotrar los archivos sin procesar usados en este proyecto:

Fuente de datos

+ [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con el archivo que requieren ser procesados.
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>

En el siguiente enlace pueden encotrar un video explicativo de como usar la API
https://youtu.be/6oOD64tBFkQ

En este enlace pueden acceder a la API  en la web.
proyecto-games-production.up.railway.app

Es importante aclarar que para obtener un retorno de la api debemos usar datos validos, por ejemplo 

Géneros Validos: 'item_name', 'Action', 'Adventure', 'Indie', 'RPG', 'Strategy'

Años Validos: 2010, 2011, 2012, 2013, 2014, 2015

Items Validos: 10, 386710, 352760, entre muchos otros

Si se quiere ejecutar la API en un entorno local, primero se debe tener el repo descargado, se puede usar el siguiente comando en la consola: git clone https://github.com/tonygrill/proyecto-games.git   una vez con los archivos necesarios se debe disponer de un editor de codigo como vscode, la terminal debe estar en el directorio donde se encuentran los archivos, una vez en la terminal del editor de texto se ejecuta el siguiente comando para instalar todas las librerias necesarias: pip install -r requirements.txt, ya con los requerimientos instalados procedemos a ejecutar el servidor uvicorn con el siguiente comando: uvicorn main:app --reload --port 5000 --host 0.0.0.0, este comando ejecutara el servidor y recargara la API cuando detecte cambios en el archivo main.py y permira el acceso a cualquier dispositivo en la red loca, despues de actiar el servidor http://localhost:5000/docs, desde ahi ya puede ser consumida la API.

Los procesos de extracción, ETL y EDA se explican mas a detalle en los archivos respectivos.

El orden en que deben ejecutar los notebooks es el siguiente:


-ARCHIVO: ETL_steam_games.ipynb   -ARCHIVO RESULTANTE: steam.csv
-ARCHIVO: ETL_user_items.ipynb    -ARCHIVO RESULTANTE: user_items.parquet
-ARCHIVO: ETL_user_reviews        -ARCHIVO RESULTANTE: user_reviews.parquet
-ARCHIVO: union.ipynb:            -ARCHIVO RESULTANTE: games.parquet
-ARCHIVO: EDA.ipynb               -ARCHIVO RESULTANTE: steam_games.parquet   

El dataset que consumira el archivo main.py de la API es steam_games.parquet.

Luego de ejecutado todo ese proceso se puede ejecutar la api como se explico anteriormente

El archivo steam.csv de mantuvo en ese formato y no en parquet, debido a que generaba errores al desanidar la columna gener.



Proyecto desarrollado por ING Antonio Moreno
antomore353@hotmail.com
https://github.com/tonygrill