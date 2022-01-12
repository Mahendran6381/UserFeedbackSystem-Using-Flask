from flask import Flask, render_template, request
from flask.typing import StatusCode

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form['customer']
        staff_name = request.form['staff_name']
        rating = request.form['rating']
        detail = request.form['textarea']
        if name == "" or staff_name == "":
            return render_template("index.html", message="Please enter The required Fields")
        print(name, staff_name, rating, detail)
        return render_template('success.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
