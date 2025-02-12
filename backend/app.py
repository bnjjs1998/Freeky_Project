from datetime import datetime

import bcrypt
import graphene
from flask_graphql import GraphQLView

from flask import Flask
from flask_cors import CORS
import graphene
from graphene import ObjectType, String, List, Schema
from flask_graphql import GraphQLView
from pymongo import MongoClient
from Register import *

app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app, origins=["http://localhost:5173"])


client = MongoClient("mongodb://localhost:27017/")
db = client["freeky_db"]  # Nom de la base de données

# # Création de la collection
# users = db["users"]  # Nom de la collection

# users.insert_one({"name": "John", "lastname": "Doe", "email": "jd@mail.com" })"
# # Création de la collection
# event


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


class UserType(graphene.ObjectType):
    FirstName = graphene.String()
    LastName = graphene.String()
    birthday = graphene.String()
    email = graphene.String()

class Register(graphene.Mutation):
    class Arguments:
        FirstName = graphene.String(required=True)
        LastName = graphene.String(required=True)
        birthday = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, FirstName, LastName, birthday, email, password):
        print("Nouvel utilisateur enregistré :")
        print(f"Prénom: {FirstName}")
        print(f"Nom: {LastName}")
        print(f"Date de naissance: {birthday}")
        print(f"Email: {email}")
        print(f"Mot de passe: (non affiché pour la sécurité) {password} ")

        return Register(user=UserType(
            FirstName=FirstName,
            LastName=LastName,
            birthday=birthday,
            email=email
        ))

# Définition du schéma GraphQL
class Mutation(graphene.ObjectType):
    register = Register.Field()

# Définition du schéma GraphQL
schema = graphene.Schema(mutation=Mutation)


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