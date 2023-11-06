import csv
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import os

import spacy



"""
# Cargar las palabras de detención desde el archivo stopwords.txt
with open('stopwords.txt', 'r') as stopwords_file:
    stopwords = stopwords_file.read().splitlines()
"""
# Crear un objeto stemmer
stemmer = PorterStemmer()

# Función para limpiar y tokenizar el texto
def clean_and_tokenize(text):
    # Eliminar caracteres no alfanuméricos y convertir a minúsculas
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text).lower()
    tokens = word_tokenize(text)
    return tokens

# Crear un diccionario para almacenar los datos procesados
data = {}

# Abrir el archivo CSV
with open('new_spotify.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Obtener el ID de la fila
        row_id = row['track_id']
        idioma_track=row['language']
        print("------------------------------------------------------")
        print(idioma_track)
        #stopwords=set(stopwords.words(idioma_track))
        #stopwords = get_stop_words('Italian')
        nlp = spacy.load(f"{idioma_track}_core_news_sm")
        stopwords = nlp.Defaults.stop_words
        
        # Concatenar los atributos textuales en una cadena
        atributos_textuales = [row[key] for key in row if key not in ['track_id','track_popularity', 'track_album_release_date','danceability','energy','key','loudness','mode','speechiness'
                                                                    ,'acousticness','instrumentalness','liveness','valence','tempo','duration_ms','track_album_id','playlist_id']]
        texto_completo = ' '.join(atributos_textuales)
        
        # Limpieza y tokenización del texto
        tokens = clean_and_tokenize(texto_completo)
        
        # Eliminar las stopwords
        tokens = [token for token in tokens if token.lower() not in stopwords]
        
        # Aplicar stemming a los tokens
        tokens = [stemmer.stem(token) for token in tokens]

        #ordenar los tokens
        tokens.sort()
        
        # Almacenar el ID de la fila y sus tokens en el diccionario
        data[row_id] = tokens

# Guardar los datos en un archivo JSON
with open('archivo_procesado_english.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)


"""


### ESPAÑOL PRUEBA

# Cargar las palabras de detención desde el archivo stopwords.txt
with open('stopwords.txt', 'r') as stopwords_file:
    stopwords = stopwords_file.read().splitlines()

# Crear un objeto stemmer
stemmer = PorterStemmer()

# Función para limpiar y tokenizar el texto
def clean_and_tokenize(text):
    # Eliminar caracteres no alfanuméricos y convertir a minúsculas
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text).lower()
    tokens = word_tokenize(text)
    return tokens

# Crear un diccionario para almacenar los datos procesados
data = {}

# Abrir el archivo CSV
with open('new_spotify.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Obtener el ID de la fila
        row_id = row['track_id']
        idioma_track=row['language']
        if(idioma_track=="es"):

            # Concatenar los atributos textuales en una cadena
            atributos_textuales = [row[key] for key in row if key not in ['track_popularity', 'track_album_release_date','danceability','energy','key','loudness','mode','speechiness'
                                                                        ,'acousticness','instrumentalness','liveness','valence','tempo','duration_ms']] 
            texto_completo = ' '.join(atributos_textuales)
            
            # Limpieza y tokenización del texto
            tokens = clean_and_tokenize(texto_completo)
            
            # Eliminar las stopwords
            tokens = [token for token in tokens if token.lower() not in stopwords]
            
            # Aplicar stemming a los tokens
            tokens = [stemmer.stem(token) for token in tokens]

            #ordenar los tokens
            tokens.sort()
            
            # Almacenar el ID de la fila y sus tokens en el diccionario
            data[row_id] = tokens

# Guardar los datos en un archivo JSON
with open('archivo_procesado_español.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
"""