from flask import Flask, request
from os.path import exists
import os
from csv import DictReader, DictWriter
from http import HTTPStatus


FILENAME = 'users.csv'
FIELDNAMES = ["id","name", "email", "password", "age"]

def get_last_id():
    id_list = []

    with open(FILENAME, 'r') as f:
        reader = DictReader(f)
        for data in reader:
            id_list.append(int(data['id']))

    return sorted(id_list)[-1]+1 if id_list != [] else 1


app = Flask(__name__)

@app.route("/signup", methods=["POST"])
def signup():
    if not exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        with open(FILENAME, 'w') as f:
            writer = DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

    data = dict(request.get_json())
    data['id'] = get_last_id()

    with open(FILENAME, 'a') as f:
        writer = DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(data)

    return {"id": data["id"], "name": data["name"], "email": data["email"], "age": data["age"]}, HTTPStatus.CREATED


@app.route("/login", methods=["POST"])
def login():
    if not exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        return []
    
    datas = []
    
    with open(FILENAME, 'r') as f:
        reader = DictReader(f)
        for data in reader:
            datas.append(data)
    for data in datas:
        if data["email"] == request.json["email"] and data["password"] == request.json["password"]:
            return {"id": data["id"], "name": data["name"], "email": data["email"], "age": data["age"]}, HTTPStatus.OK
        return {
            "Message": "404 not found"
        }, HTTPStatus.BAD_REQUEST


@app.route("/signup/<int:login_id>", methods= ['DELETE'])
def delete_id(login_id):
    
    datas_again = []
    
    with open(FILENAME, 'r') as f:
            reader = DictReader(f)
            for data in reader:
                datas_again.append(data)
    
    data_1 = []
    
    for data in datas_again:
        if int(data['id']) != login_id:
            data_1.append(data)
    if len(data_1) == len(datas_again):
        return {
            "Message": "404 not found"
        }, HTTPStatus.BAD_REQUEST   
    with open(FILENAME, 'w') as f:
            writer = DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    with open(FILENAME, 'a') as f:
        for data in data_1:  
            writer = DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(data)
    return {"data": "Product removed!", "status": "Ok"}, HTTPStatus.NO_CONTENT

@app.route('/signup/<int:user_id>', methods=['PATCH'])
def update_info(user_id):
    
    get_data = []
    
    with open(FILENAME, 'r') as f:
            reader = DictReader(f)
            for data in reader:
                get_data.append(data)
    
    update_informations = dict(request.get_json())

    for data in get_data:
            if data['id'] == str(user_id):
                data.update(update_informations)

                with open(FILENAME, 'w') as f:
                    writer = DictWriter(f, fieldnames=FIELDNAMES)
                    writer.writeheader()
                    writer.writerows(get_data)

                return {"id": data["id"], "name": data["name"], "email": data["email"], "age": data["age"]}, HTTPStatus.OK

    return {"data": "Product doesn't exists"}

@app.route('/users', methods=['GET'])
def users():
    
    users = []

    with open(FILENAME, 'r') as f:
        reader = DictReader(f)
        for data in reader:
            users.append(data)

    return {"data": users, "status": "Ok"}, HTTPStatus.OK