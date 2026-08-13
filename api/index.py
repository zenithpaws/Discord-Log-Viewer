import os
from flask import Flask, render_template

# Point static_folder to the root static directory
app = Flask(
    __name__, 
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/static"
)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)