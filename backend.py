import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import json
nltk.download('stopwords')
nltk.download('wordnet')

class TokenStream:
    def __init__(self, documents):
        self.documents = documents
        self.current_docID = 0  # Inicializa el docID en 0
        self.token_index = 0  # Inicializa el índice del token

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_docID < len(self.documents):
            doc = self.documents[self.current_docID]
            if self.token_index < len(doc):
                token = doc[self.token_index]
                self.token_index += 1
                return token
            else:
                # Pasar al siguiente documento
                self.current_docID += 1
                self.token_index = 0
                return next(self)
        else:
            raise StopIteration

    def reset(self):
        self.current_docID = 0  # Restablece el docID al valor inicial
        self.token_index = 0  # Restablece el índice del token al valor inicial


# Abrir el archivo CSV en modo lectura
with open('styleslimpio.csv', 'r') as file:
    # Leer las líneas del archivo
    lines = file.readlines()

# Crear una lista de listas para almacenar los datos procesados
processed_data = []

# Dividir la primera línea (encabezados)
headers = lines[0].strip().split(',')

# Encontrar los índices de las columnas que deseas concatenar
id_index = headers.index('id')
year_index = headers.index('year')

# Recorrer las líneas del archivo, excluir 'id' y 'year' y concatenar los atributos
for line in lines[1:]:
    values = line.strip().split(',')
    concatenated_attributes = [values[i] for i in range(len(values)) if i != id_index and i != year_index]
    processed_data.append(concatenated_attributes)

# Ahora, processed_data es una lista de listas que contiene los datos procesados



def pre_procesar(lista_de_textos):
    resultados = []
    lemmatizer = WordNetLemmatizer()
    puntuacion = string.punctuation
    customSW = open('stopwords.txt','r')
    palabras_stoplist = customSW.read() #.splitlines()
    customSW.close()

    for texto in lista_de_textos:
        # 1- extraer los tokens
        tokens = nltk.word_tokenize(texto)
        tokens = [token.lower() for token in tokens]
        # 2- eliminar signos innecesarios
        tokens = [token for token in tokens if all(char not in puntuacion for char in token)]
        # 3- eliminar stopwords
        tokens = [token for token in tokens if token.lower() not in palabras_stoplist]
        # 4- sacar la raíz de cada palabra (lexema)
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        resultados.append(tokens)

    
    return resultados
lista_de_cadenas = [' '.join(lista) for lista in processed_data]
a = pre_procesar(lista_de_cadenas)

# Algoritmo SPIMI para construir el índice invertido
def SPIMI_INVERT(token_stream, block_size):
    output_files = []
    block_dictionary = {}
    block_memory_limit = block_size  # Establece el límite de memoria por bloque

    while True:
        try:
            token = next(token_stream)
        except StopIteration:
            break

        term = token  # Obtén el término del token

        if term not in block_dictionary:
            block_dictionary[term] = []  # Inicializa la lista de postings

        postings_list = block_dictionary[term]

        # Verifica si la lista de postings está llena
        if len(postings_list) >= block_memory_limit:
            # Ordena los términos y escribe el bloque en disco
            sorted_terms = sorted(block_dictionary.keys())
            block_file = 'block_{}.json'.format(len(output_files) + 1)
            with open(block_file, 'w') as f:
                block_data = {term: postings_list for term, postings_list in block_dictionary.items()}
                json.dump(block_data, f)
                output_files.append(block_file)
            block_dictionary.clear()

        # Agrega el docID al postings list
        docID = token_stream.current_docID  # Asegúrate de tener esta información en tu token_stream
        if docID not in postings_list:
            postings_list.append(docID)

    # Procesa el último bloque si es necesario
    if block_dictionary:
        sorted_terms = sorted(block_dictionary.keys())
        block_file = 'block_{}.json'.format(len(output_files) + 1)
        with open(block_file, 'w') as f:
            block_data = {term: postings_list for term, postings_list in block_dictionary.items()}
            json.dump(block_data, f)
            output_files.append(block_file)
        block_dictionary.clear()

    return output_files

# Uso del algoritmo SPIMI para construir el índice invertido en bloques
block_size = 1000  # Tamaño de bloque en términos de cantidad de términos
token_stream = TokenStream(a)  # Asegúrate de tener una clase TokenStream que pueda seguir los docIDs
block_files = SPIMI_INVERT(token_stream, block_size)

# Combinación de los bloques en un solo índice invertido final
final_index = {}
for block_file in block_files:
    with open(block_file, 'r') as f:
        block_data = json.load(f)
        for term, postings_list in block_data.items():
            if term not in final_index:
                final_index[term] = []
            final_index[term].extend(postings_list)

# Guardar el índice invertido en un archivo JSON
with open('indice_invertido.json', 'w') as f:
    json.dump(final_index, f)