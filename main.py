from flask import Flask, render_template, request
from flask.typing import StatusCode
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user = "root",
    password ="kalisee",
    database="feedback"
)
cursor = mydb.cursor()

app = Flask(__name__)

class User():
    userArr = []
    def __init__(self,name,staff_name,rating,detail) -> None:
        self.name = name
        self.staff_name = staff_name
        self.rating = rating
        self.detail = detail
        

    def insertion(self):
        query = f"insert into user_feedback (name,staff_name,rating,detail) values ( {self.name} ,{self.staff_name} ,{self.rating} ,{self.detail})"

    @classmethod
    def deletion(cls)    

        


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
