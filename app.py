from flask import Flask, render_template,request
import mysql.connector

app = Flask(__name__)


def get_states():
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773046",
        password="x4HBUbFzQu",
        database="sql12773046",
        port=3306  # use the port they gave you
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT State FROM places")
    rows = cursor.fetchall()
    states = [row[0] for row in rows]  # Convert tuples to plain list
    conn.close()
    return states


# Connect to MySQL
def get_data():
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773046",
        password="x4HBUbFzQu",
        database="sql12773046",
        port=3306  # use the port they gave you
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM places")
    result = cursor.fetchall()
    conn.close()
    return result

@app.route('/search.html')
def call():
    states = get_states()
    return render_template('search.html', result=None, query=None, states=states)

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    states = get_states()
    if request.method == 'POST':
        query = request.form['query']
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12773046",
            password="x4HBUbFzQu",
            database="sql12773046",
            port=3306  # use the port they gave you
        )
        cursor = conn.cursor(dictionary=True)   
        cursor.execute("SELECT * FROM places WHERE LOWER(State) = LOWER(%s)", (query,))
        result = cursor.fetchall()
        conn.close()
        return render_template('search.html', result=result, query=query, states=states)
    return render_template('search.html', result=None, query=None, states=states)

@app.route('/budget', methods=['POST'])
def by_budget():
    states = get_states()
    budget = request.form['budget']
    query = request.form['query']  
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773046",
        password="x4HBUbFzQu",
        database="sql12773046",
        port=3306  # use the port they gave you
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM places WHERE LOWER(State) = LOWER(%s) AND `Entrance Fee in INR` <= %s", (query, budget))
    result = cursor.fetchall()
    conn.close()
    return render_template('search.html', result=result, query=query, states=states,budget=budget)

@app.route('/time', methods=['POST'])
def by_time():
    states = get_states()
    budget = request.form['budget']
    query = request.form['query']  
    time = request.form['time']
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773046",
        password="x4HBUbFzQu",
        database="sql12773046",
        port=3306  # use the port they gave you
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM places WHERE LOWER(State) = LOWER(%s) AND `Entrance Fee in INR` <= %s AND (`Best Time to visit` =%s or `Best Time to visit` ='All')", (query, budget,time))
    result = cursor.fetchall()
    conn.close()
    return render_template('search.html', result=result, query=query, states=states)

@app.route('/timewithoutbudget', methods=['POST'])
def by_timenotbudget():
    states = get_states()
    query = request.form['query']  
    time = request.form['time']
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773046",
        password="x4HBUbFzQu",
        database="sql12773046",
        port=3306  # use the port they gave you
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM places WHERE LOWER(State) = LOWER(%s) AND (`Best Time to visit` =%s or `Best Time to visit` ='All')", (query,time))
    result = cursor.fetchall()
    conn.close()
    return render_template('search.html', result=result, query=query, states=states)



if __name__ == '__main__':
    app.run(debug=True)
