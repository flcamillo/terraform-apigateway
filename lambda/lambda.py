import os
import pymongo
import json
from bson.objectid import ObjectId
from datetime import datetime

# inicializa o cliente do mongo
mongo = pymongo.MongoClient(os.environ["DB_CONNECTION_STRING"])

# seleciona o banco de dados
db = mongo[os.environ["DB_NAME"]]

# seleciona a collection
col = db["users"]

# cria o indice da collection
# se já existir o MongoDB ignora e não gera erro
col.create_index([("userName", pymongo.ASCENDING)], unique=True)


# função recursiva para converter o ObjectId e ISODate para string
def mongo_format_to_string(records):
    for k in records:
        value = records[k]
        if type(value) is ObjectId:
            records[k] = str(value)
            continue
        if type(value) is dict:
            records[k] = mongo_format_to_string(value)
            continue
        if type(value) is datetime:
            records[k] = str(value)
    return records


# cria um usuário
def create_user(event):
    body = json.loads(event["body"])
    if body.get("_id") is not None:
        del body["_id"]
    body["created"] = datetime.now()
    col_result = col.insert_one(body)
    body["_id"] = col_result.inserted_id
    return {
        "statusCode": 201,
        "body": json.dumps(mongo_format_to_string(body))
    }


# procura um usuário pelo seu id
def get_user(event):
    parms = event["pathParameters"]
    query = {"_id": ObjectId(parms["id"])}
    for r in col.find(query):
        return {
            "statusCode": 200,
            "body": json.dumps(mongo_format_to_string(r))
        }
    return {
        "statusCode": 400,
        "body": "not found"
    }


# apaga um usuário pelo seu id
def delete_user(event):
    parms = event["pathParameters"]
    query = {"_id": ObjectId(parms["id"])}
    col_result = col.delete_one(query)
    if col_result.deleted_count > 0:
        return {
            "statusCode": 200,
            "body": "records deleted: {0}".format(col_result.deleted_count)
        }
    return {
        "statusCode": 400,
        "body": "not found"
    }


# atualiza um usuário pelo seu id
def update_user(event):
    parms = event["pathParameters"]
    body = json.loads(event["body"])
    query = {"_id": ObjectId(parms["id"])}
    for r in col.find(query):
        for k in body:
            if k == "_id":
                continue
            r[k] = body[k]
        col.replace_one(query, r)
        return {
            "statusCode": 200,
            "body": json.dumps(mongo_format_to_string(r))
        }
    return {
        "statusCode": 400,
        "body": "not found"
    }


# procura um usuário pelo seu userName
def get_user_by_userName(event):
    parms = event["pathParameters"]
    query = {"userName": parms["userName"]}
    for r in col.find(query):
        return {
            "statusCode": 200,
            "body": json.dumps(mongo_format_to_string(r))
        }
    return {
        "statusCode": 400,
        "body": "not found"
    }


# procura usuários pelo seu nome
def find_user(event,):
    parms = event["queryStringParameters"]
    page = parms.get("page")
    if page is None:
        page = 0
    pagesize = parms.get("pageSize")
    if pagesize is None:
        pagesize = 10
    firstName = parms.get("firstName")
    lastName = parms.get("lastName")
    email = parms.get("email")
    userStatus = parms.get("userStatus")
    createdStart = parms.get("createdStart")
    createdEnd = parms.get("createdEnd")
    query = {}
    if firstName is not None and firstName.strip() != "":
        query["firstName"] = {"$regex": ".*{0}.*".format(firstName)}
    if lastName is not None and lastName.strip() != "":
        query["lastName"] = {"$regex": ".*{0}.*".format(lastName)}
    if email is not None and email.strip() != "":
        query["email"] = {"$regex": ".*{0}.*".format(email)}
    if userStatus is not None and userStatus.strip() != "":
        query["userStatus"] = int(userStatus)
    created = {}
    if createdStart is not None and createdStart.strip() != "":
        start = datetime.fromisoformat(createdStart)
        created["$gte"] = start
    if createdEnd is not None and createdEnd.strip() != "":
        end = datetime.fromisoformat(createdEnd)
        created["$lte"] = end
    if len(created) > 0:
        query["created"] = created
    records = []
    for r in col.find(query).limit(pagesize).skip(pagesize*page):
        records.insert(len(records), mongo_format_to_string(r))
    return {
        "statusCode": 200,
        "body": json.dumps(records)
    }


# função principal da lambda
def lambda_handler(event, context):
    print(event)
    # define as rotas da api
    routes = {
        "/user": {
            "POST": create_user
        },
        "/user/{id}": {
            "PUT": update_user,
            "DELETE": delete_user,
            "GET": get_user
        },
        "/user/username/{userName}": {
            "GET": get_user_by_userName
        },
        "/user/find": {
            "GET": find_user,
        }
    }
    # executa a rota solicitada
    route = routes.get(event["resource"])
    if route is None:
        return {
            "statusCode": 400
        }
    method = route.get(event["httpMethod"])
    if method is None:
        return {
            "statusCode": 400
        }
    return method(event)
