from flask import Flask, jsonify, request, render_template
from search import for_user_index
from search_db import for_user_sql
import csv

app = Flask(__name__)

def get_links(file):
    links = {}
    file = "Data/" + file
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            id = row['filename']
            id = id.replace('.jpg', '')
            link_ = row['link']
            links[id] = link_
    return links

@app.route("/", methods=['GET', 'POST'])
def main_query():
    product_names = []
    product_ids = []
    
    time = None
    gallery_links = None
    gallery_data = None

    search_option = ""
    active_section = ""
    # is_clothes = True

    if request.method == 'POST':
        active_section = request.form['active_section']
        print(active_section)
        """
        if (active_section == 'songSearch'):
           is_clothes = False
        """

    if request.method == 'POST' and active_section == 'clothSearch':
        user_input = request.form['input_text']
        search_option = request.form['search_option']

        if search_option == "Our_index":
            product_names, product_ids, time = for_user_index(user_input)
            print(f"User search - {user_input}, Search option - {search_option}")
        else:
            product_names, product_ids, time = for_user_sql(user_input)
            print(f"User search - {user_input}, Search option - {search_option}")

        # Obtener links de csv y hacer match según resultado de busqueda
        query_links = get_links("images.csv")
        gallery_links = [query_links.get(id, '') for id in product_ids]

        # gallery_data = zip(gallery_links, product_names)
        if gallery_links is not None and product_names is not None:
            gallery_data = zip(gallery_links, product_names)
        else:
            gallery_data = []
        
    elif request.method == 'POST' and active_section == 'songSearch':
        return render_template('song_search.html', gallery_data=gallery_data, time=time)

    return render_template('index.html', gallery_data=gallery_data, time=time)

if __name__ == "__main__":
    app.run(debug=True)
