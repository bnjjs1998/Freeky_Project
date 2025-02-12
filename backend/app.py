import graphene
from flask_graphql import GraphQLView

from flask import Flask
from flask_cors import CORS
import graphene
from graphene import ObjectType, String, List, Schema
from flask_graphql import GraphQLView
from pymongo import MongoClient


app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app, origins=["http://localhost:5173"])


client = MongoClient("mongodb://localhost:27017/")
db = client["freeky_db"]  # Nom de la base de données

# # Création de la collection
# users = db["users"]  # Nom de la collection

# users.insert_one({"name": "John", "lastname": "Doe", "email": "jd@mail.com" })"
# # Création de la collection
# event = db["event"]  # Nom de la collection

# Définition du type GraphQL pour les soirées
class SoireeType(graphene.ObjectType):
    id = graphene.String()
    nom = graphene.String()
    date = graphene.String()
    lieu = graphene.String()

# Définition de la Query pour récupérer les soirées
class Query(graphene.ObjectType):
    soirees = graphene.List(SoireeType)

    def resolve_soirees(self, info):
        return list(db["soirees"].find({}, {"_id": 0}))  # Récupère toutes les soirées

# Définition du schéma GraphQL
schema = graphene.Schema(query=Query)

# Ajout de la route GraphQL
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@app.route('/')
def hello_world():  # put application's code here
    return {"message": "API Flask + GraphQL + MongoDB is ok !"}


if __name__ == '__main__':
    app.run(debug=True)
