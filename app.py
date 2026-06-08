from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS buddies
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  city TEXT,
                  zipcode TEXT,
                  goal TEXT,
                  level TEXT,
                  gender TEXT,
                  contact TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_buddy():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO buddies (name, city, zipcode, goal, level, gender, contact, date) VALUES (?,?,?,?,?,?,?,?)",
            (data['name'], data['city'], data['zipcode'], data['goal'], data['level'],
            data['gender'], data['contact'], data['date']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Added successfully'})

@app.route('/buddies', methods=['GET'])
def get_buddies():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM buddies")
    rows = c.fetchall()
    conn.close()
    buddies = [{'id':r[0],'name':r[1],'city':r[2],'zipcode':r[3],'goal':r[4],
                'level':r[5],'gender':r[6],'contact':r[7],'date':r[8]}
            for r in rows]
    return jsonify(buddies)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_buddy(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM buddies WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)