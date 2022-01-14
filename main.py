from email import message
from tokenize import String
from flask import Flask, render_template, request
from flask.typing import StatusCode
import mysql.connector
from email.mime.text import MIMEText
import smtplib


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kalisee",
    database="feedback",
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()

app = Flask(__name__)


class SendEmail():
    def __init__(self, name, staff_name, rating, detail) -> None:
        self.name = name
        self.staff_name = staff_name
        self.rating = rating
        self.detail = detail
        self.port = 2525
        self.username = "7a3de55faaa936"
        self.password = "d4b110ef5db0a7"
        self.host = "smtp.mailtrap.io"

    def send_email(self):
        sender_mail = "email1@example.com"
        receiver_email = "email2@example.com"
        message = f"<h3>User Feedback system</h3><ul><li>Customer : {self.name}</li><li>Staff Name : {self.staff_name}</li><li>Rating : {self.rating}</li><li>Detail : {self.detail}</li></ul>"
        msg = MIMEText(message, 'html')
        msg["Subject"] = "User FeedBack Details"
        msg["From"] = sender_mail
        msg['To'] = receiver_email

        with smtplib.SMTP(self.host, self.port) as server:
            server.login(self.username, self.password)
            server.sendmail(sender_mail, receiver_email, msg.as_string())
        return "Success"


class User(SendEmail):
    userArr = []

    def __init__(self, name, staff_name, rating, detail) -> None:
        super().__init__(name, staff_name, rating, detail)
        self.__name = name
        self.__staff_name = staff_name
        self.__rating = rating
        self.__detail = detail
        User.userArr.append(self)

    def insertion(self) -> String:
        query = f"insert into user_feedback (name,staff_name,rating,detail) values ( '{self.__name}' ,'{self.__staff_name}' ,{self.__rating} ,'{self.__detail}')"
        cursor.execute(query)
        mydb.commit()
        print(self.send_email())
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
