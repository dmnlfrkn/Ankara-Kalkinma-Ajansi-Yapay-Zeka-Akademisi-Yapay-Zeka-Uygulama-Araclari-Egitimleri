from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    with sqlite3.connect("finance.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, category TEXT,
        description TEXT, is_income INTEGER, date TEXT)""")
        conn.commit()

def authenticate(username,password):
    if not username or not password:
        return None, jsonify({'error':'Kullanıcı adı ve şifre gerekli'}), 401
    with sqlite3.connect("finance.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? and password=?",(username,password))
        user = c.fetchone()
        if not user:
            return None, jsonify({'error':'Geçersiz kimlik bilgileri'}),401
        return user[0], None
def register_db(username,password):
    with sqlite3.connect('finance.db') as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
            conn.commit()
            return jsonify({'message':'Kullanıcı oluşturuldu'}),201
        except sqlite3.IntegrityError:
            return jsonify({'error':'Kullanıcı adı zaten mevcut'}),400

def transaction_db(user_id,amount,category,description, is_income,date):
    with sqlite3.connect('finance.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO transactions (user_id, amount, category, description,is_income,date) VALUES (?,?,?,?,?,?)',
                  (user_id,amount,category,description,is_income,date))
        conn.commit()
        return jsonify({'message':'İşlem eklendi'}),201

def get_transaction_db(user_id,category):
    with sqlite3.connect('finance.db') as conn:
        c = conn.cursor()
        if category:
            c.execute('SELECT * FROM transactions WHERE user_id = ? and category = ?',(user_id,category))
        else:
            c.execute('SELECT * FROM transactions WHERE user_id = ?',(user_id,))
        transactions = [{'id':row[0],'amount':row[2],'category':row[3],'description':row[4],'is_income':bool(row[5]),'date':row[6]} for row in c.fetchall()]
        return jsonify(transactions)

def delete_transaction_db(id,user_id):
    with sqlite3.connect('finance.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?',(id,user_id))

        if c.rowcount == 0:
            return jsonify({'error':'İşlem bulunamadı veya yetkiniz yok'}),404
        conn.commit()
        return jsonify({'message':'İşlem silindi'}),200

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error":"JSON verisi eksik"}),400
    username = data.get("username")
    password = data.get("password")
    if not username:
        return jsonify({'error':'Kullanıcı adı eksik'}),400
    if not password:
        return jsonify({'error':'Şifre eksik'}),400
    return register_db(username,password)

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON verisi eksik"}), 400
    username = data.get("username")
    password = data.get("password")
    user_id, error = authenticate(username,password)
    if error:
        return error
    return jsonify({'message':'Giriş başarılı'}),200


@app.route('/transactions',methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON verisi eksik"}), 400

    username = data.get("username")
    password = data.get("password")
    amount = data.get("amount")
    category = data.get("category")
    description = data.get('description','')
    is_income = data.get('is_income',0)
    user_id, error = authenticate(username, password)
    if error:
        return error
    if not amount or not category:
        return jsonify({'error':'Tutar veya kategori gerekli'}),400
    date = datetime.now().strftime('%Y-%m-%d')
    return transaction_db(user_id,amount,category,description,is_income,date)

@app.route('/transactions',methods=['GET'])
def get_transactions():
    username = request.args.get('username')
    password = request.args.get('password')
    category = request.args.get('category')
    user_id, error = authenticate(username, password)
    if error:
        return error
    return get_transaction_db(user_id,category)

@app.route('/transactions/<int:id>',methods=['DELETE'])
def delete_transaction(id):
    username = request.args.get('username')
    password = request.args.get('password')
    user_id, error = authenticate(username, password)
    if error:
        return error
    return delete_transaction_db(id,user_id)

if __name__=='__main__':
    init_db()
    app.run(debug=True,port=5005)
