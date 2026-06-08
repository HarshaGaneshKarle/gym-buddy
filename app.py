from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)
def init_db():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS buddies
          (id INTEGER PRIMARY KEY,
          name TEXT,
          city TEXT,
          goal TEXT,
          level TEXT)''')
    conn.commit()
    conn.close()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/add', methods=['POST'])
def add_buddy():
    data=request.json
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("INSERT INTO buddies (name, city, goal, level) VALUES (?, ?, ?, ?)", (data['name'], data['city'], data['goal'], data['level']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Added Successfully'})

@app.route('/buddies', methods=['GET'])
def get_buddies():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM buddies")
    rows=c.fetchall()
    conn.close()
    buddies=[{'id':row[0], 'name':row[1], 'city':row[2], 'goal':row[3], 'level':row[4]} for row in rows]
    return jsonify(buddies)
if __name__ == '__main__':
    init_db()
    app.run(debug=True)