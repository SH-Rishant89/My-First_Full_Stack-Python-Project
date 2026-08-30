import os

from flask import Flask, render_template, request
import mysql.connector

flask_app = Flask(__name__)
    
@flask_app.route('/')
def registration_page():
    return render_template('Registration_Website.html')


#registration form submission route
@flask_app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form["name"]
    dob = request.form["dob"]
    phone = request.form["phone"]

    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    mycursor = db.cursor()
    try:
        #Prepare the query to insert data into the Student table
        sql = "INSERT INTO Student (name,date_of_birth,phone_no) VALUES (%s, %s, %s)"
        values = (name, dob, phone)
        #Execute the query with the provided values
        mycursor.execute(sql, values)
        db.commit()
        #Retrieve the last inserted ID to confirm the insertion
        last_id = mycursor.lastrowid
        return f"Success! Student added with ID: {last_id}"




    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db.is_connected():
            mycursor.close()
            db.close()


if __name__ == "__main__":
    flask_app.run(debug=True)