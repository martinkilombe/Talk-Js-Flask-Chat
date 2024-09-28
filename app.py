import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

load_dotenv() 
def setup_database():
    conn = sqlite3.connect('test.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS USERS
             (ID INT PRIMARY KEY NOT NULL,
             DP CHAR(100) NOT NULL,
             EMAIL CHAR(100) NOT NULL,
             NAME CHAR(50) NOT NULL,
             ROLE CHAR(20) NOT NULL);''')
    print("Table created successfully")
    conn.close()

def create_default_users(): 
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM USERS")
    count = cursor.fetchone()[0]
    
    if count == 0:#default users frm tutorial shared
        users = [
            (1, "https://randomuser.me/api/portraits/men/1.jpg", "tom.hardy@operator.com", "Tom Hardy", "AGENT"),
            (2, "https://randomuser.me/api/portraits/men/62.jpg", "john.morrison@operator.com", "John Morrison", "USER")
        ]
        cursor.executemany("INSERT INTO USERS (ID, DP, EMAIL, NAME, ROLE) VALUES (?, ?, ?, ?, ?)", users)
        conn.commit()
        print("Default users created")
    
    conn.close()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    talkjs_app_id = os.getenv('TALKJS_APP_ID')
    return render_template('index.html', talkjs_app_id=talkjs_app_id)

@app.route('/createUser/', methods=['POST'])
def createUser():
    conn = sqlite3.connect('test.db')
    requestData = request.json
    id = requestData['id']
    name = requestData['name']
    dp = requestData['dp']
    email = requestData['email']
    role = requestData['role']
    conn.execute("INSERT INTO USERS (ID,DP,EMAIL,NAME,ROLE) VALUES (?,?,?,?,?)", (id, dp, email, name, role))
    conn.commit()
    conn.close()
    return "User Created", 200

@app.route('/getUser/', methods=['GET'])
def getUser():
    requestData = request.args
    id = requestData['id']
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT * from USERS WHERE ID = ?", (id,))
    user = {
      'id': "",
      'name': "",
      'dp': "",
      'email': "",
      'role': ""
    }
    for row in cursor:
      user['id'] = row[0]
      user['dp'] = row[1]
      user['email'] = row[2]
      user['name'] = row[3]
      user['role'] = row[4]
    conn.close()
    response = jsonify(user)
    return response, 200

if __name__ == '__main__':
    setup_database()
    create_default_users()
    app.run(port=8080, debug=True)