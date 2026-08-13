from flask import Flask, render_template

app = Flask(__name__, template_folder="../templates")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)