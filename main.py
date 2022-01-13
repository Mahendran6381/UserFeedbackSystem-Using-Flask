from tokenize import String
from flask import Flask, render_template, request
from flask.typing import StatusCode
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kalisee",
    database="feedback",
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()

app = Flask(__name__)


class User():
    userArr = []

    def __init__(self, name, staff_name, rating, detail) -> None:
        self.__name = name
        self.__staff_name = staff_name
        self.__rating = rating
        self.__detail = detail
        User.userArr.append(self)

    def insertion(self) -> String:
        query = f"insert into user_feedback (name,staff_name,rating,detail) values ( '{self.__name}' ,'{self.__staff_name}' ,{self.__rating} ,'{self.__detail}')"
        cursor.execute(query)
        mydb.commit()
        return str(cursor.rowcount) + "record Inserted"

    @classmethod
    def deletion(cls, name) -> String:
        query = f"delete from user_feedback where name = {name}"
        cursor.execute(query)
        mydb.commit()
        return "deleted"


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
        newObj = User(name, staff_name, rating, detail)
        print(newObj.insertion())
        return render_template('success.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
