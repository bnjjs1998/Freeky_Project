from datetime import datetime
import bcrypt
import graphene
from flask_graphql import GraphQLView
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# Autoriser le CORS uniquement sur l'URL local de React
CORS(app, origins=["http://localhost:5173"])

# Connexion à la base MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["freeky_db"]  # Nom de la base de données




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
        soirees = db["soirees"].find({}, {"_id": 0})  # Exclut l'ID MongoDB
        return list(soirees)  # Conversion en liste pour GraphQL




# Définition du type GraphQL pour les utilisateurs
class UserType(graphene.ObjectType):
    FirstName = graphene.String()
    LastName = graphene.String()
    birthday = graphene.String()
    email = graphene.String()



# Mutation pour l'enregistrement d'un utilisateur
class Register(graphene.Mutation):
    class Arguments:
        FirstName = graphene.String(required=True)
        LastName = graphene.String(required=True)
        birthday = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, FirstName, LastName, birthday, email, password):
        # Vérifier si l'email existe déjà
        existing_user = db["users"].find_one({"email": email})
        if existing_user:
            raise Exception("Cet email est déjà utilisé.")

        # Hash du mot de passe pour la sécurité
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Sauvegarde dans MongoDB
        db["users"].insert_one({
            "FirstName": FirstName,
            "LastName": LastName,
            "birthday": birthday,
            "email": email,
            "password": hashed_password.decode('utf-8')  # Stocker en texte lisible
        })

        return Register(user=UserType(
            FirstName=FirstName,
            LastName=LastName,
            birthday=birthday,
            email=email
        ))




class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, email, password):
        # Simuler la vérification de l'existence de l'utilisateur
        print(f"Vérification de l'utilisateur avec l'email : {email}")
        user_exists = True  # Supposons que l'utilisateur existe pour cette démonstration

        if not user_exists:
            raise Exception("Utilisateur non trouvé.")

        # Simuler la vérification du mot de passe
        print(f"Vérification du mot de passe pour l'utilisateur : {email}")
        password_correct = True  # Supposons que le mot de passe est correct pour cette démonstration

        if not password_correct:
            raise Exception("Mot de passe incorrect.")

        print("Connexion réussie.")
        return LoginMutation(message="Connexion réussie.")


        return LoginMutation(message="Connexion réussie.")




# Fusion des mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = LoginMutation.Field()



# Définition du schéma GraphQL (Query + Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)



# Ajout de la route GraphQL
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

@app.route('/')
def hello_world():
    return {"message": "API Flask + GraphQL + MongoDB is ok !"}

if __name__ == '__main__':
    app.run(debug=True)
