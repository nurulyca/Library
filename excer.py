import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

app = Flask(__name__)

conn_str = 'postgresql://postgres:postgres@localhost:5432/excer'
engine = create_engine(conn_str, echo=False)

@app.route('/users/')
def get_users():
    all = []
    with engine.connect() as connection:
        qry = text("SELECT * FROM public.user")
        result = connection.execute(qry)
        for item in result:
            all.append({
                'user_id': item[0], 'name': item[1], 'email': item[3], 'password': item[2]
            })
    return jsonify(all)

@app.route('/users/<id>')
def get_user(id):
    all = []
    with engine.connect() as connection:
        qry = text("SELECT * FROM public.user where user_id=:id")
        result = connection.execute(qry, id=id)
        for item in result:
            all.append({
                'user_id': item[0], 
                'name': item[1], 
                'password': item[2],
                'email': item[3]  
            })
    return jsonify(all)

@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    result_total = {}
    with engine.connect() as connection:
        qry = text("INSERT INTO excer.public.user (name, password, email) \
                  VALUES (\'{}\',  \'{}\',  \'{}\')".format(data["name"], data["password"], data["email"]))
        qry2 = text("SELECT * FROM excer.public.user")
        result = connection.execute(qry)
        result2 = list(connection.execute(qry2))
        print(result2)
        result_total["id"] = result2[-1].user_id
        result_total["name"] = result2[-1].name
        result_total["email"] = result2[-1].email
        result_total["password"] = result2[-1].password
    return result_total, 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    all = []
    data = request.get_json()
    
    with engine.connect() as connection:
        email = data.get("email")
        name = data.get("name")
        password = data.get("password")

        if email == None and password == None:
            qry = text("UPDATE public.user SET name = \'{}\' WHERE user_id = {}".format(name, id))
        elif email == None and name == None:
            qry = text("UPDATE public.user SET password = \'{}\' WHERE user_id = {}".format(password, id))
        elif name == None and password == None:
            qry = text("UPDATE public.user SET email = \'{}\' WHERE user_id = {}".format(email, id))
        elif email == None:
            qry = text("UPDATE public.user SET name = \'{}\', password = \'{}\' WHERE user_id = {}".format(name, password, id))
        elif password == None:
            qry = text("UPDATE public.user SET name = \'{}\', email = \'{}\' WHERE user_id = {}".format(name, email, id))
        elif name == None:
            qry = text("UPDATE public.user SET email = \'{}\', password = \'{}\' WHERE user_id={}".format(email, password, id))
        else:
            qry = text("UPDATE public.user SET name = \'{}\', email = \'{}\', password = \'{}\' WHERE user_id = {}".format(name, email, password, id))
        
        qry2 = text("SELECT * FROM public.user where user_id={}".format(id))
        result = connection.execute(qry)
        result2 = connection.execute(qry2)
        for item in result2:
            all.append({
                'user_id': item[0], 
                'name': item[1], 
                'password': item[2],
                'email': item[3]
                    })
        return jsonify(all)
        
@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    with engine.connect() as connection:
        qry = text("DELETE FROM public.user where user_id = {}".format(id))
        result = connection.execute(qry)
    return {
        'success': 'Data deleted successfully'
    }