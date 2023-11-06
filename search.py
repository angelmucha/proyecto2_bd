import json
from tf_idf import calculate_document_length, calculate_tfidf
import csv
import time

#realizar una consulta y retornar segun su scorecosine
def search(query, inverted_index, document_lengths, total_docs, tfidf_data):

    query_tokens = query.split()

    query_tfidf = {}
    for term in query_tokens:
        tfidf = calculate_tfidf(term, query_tokens, inverted_index, total_docs)
        query_tfidf[term] = tfidf

    query_length = calculate_document_length(query_tokens, inverted_index, total_docs)

    cosine_scores = {}
    for doc_id, doc_length in document_lengths.items():
        score = 0.0
        for term, tfidf in query_tfidf.items():
            if term in inverted_index:
                if doc_id in inverted_index[term]:
                    score += tfidf * tfidf_data[doc_id][term]
        score /= doc_length * query_length
        cosine_scores[doc_id] = score

    # Ordenar los documentos por puntaje coseno y retornar los 10 mejores
    results = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    results = [x for x in results if x[1] > 0]

    return results

# Cargar el índice invertido
with open('indice_invertido.json', 'r') as index_file:
    inverted_index = json.load(index_file)

# Cargar las longitudes de los documentos
with open('document_lengths.json', 'r') as lengths_file:
    document_lengths = json.load(lengths_file)

#cargar tfidf
with open('tfidf_data.json', 'r') as tfidf_file:
    tfidf_data = json.load(tfidf_file)

#print(tfidf_data['15970']['casual'])

# Ejemplo de consulta
# query = 'casual'
# results = search(query, inverted_index, document_lengths, 44424, tfidf_data)

#retornar el nombre del articulo
def get_name(id):
    with open('styleslimpio.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['id'] == id:
                return row['productDisplayName']

# Recibe y muestra a frontend
results = None
def for_user(query):
    s_time = time.time()
    results = search(query, inverted_index, document_lengths, 44424, tfidf_data)
    e_time = time.time()
    exe_time = e_time - s_time

    product_names = [get_name(doc_id) for doc_id, _ in results]
    return product_names, round(exe_time, 3)

#imprimir los resultados
# for doc_id, score in results:
    # print(f'{get_name(doc_id)} - {score}')

