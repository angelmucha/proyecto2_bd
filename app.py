from flask import Flask, jsonify, request, render_template
from search import for_user
# import psycopg2

app = Flask(__name__)

def get_db():
    # psycopg2 connection
    pass

@app.route("/", methods=['GET', 'POST'])
def main_query():
    product_names = None
    time = None
    if request.method == 'POST':
        user_input = request.form['input_text']
        product_names, time = for_user(user_input)
        print("User search")
        
    return render_template('index.html', product_names=product_names, time=time)

if __name__ == "__main__":
    app.run(debug=True)
