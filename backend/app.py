from datetime import datetime
from datetime import date
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


## Travail baptiste

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



    def mutate(self, info, FirstName, LastName, birthdate, email, password):
        # Vérifier si l'email existe déjà
        existing_email = db["users"].find_one(
            {"email": email,},
        )
        if existing_email:
            raise Exception("Cet email est déjà utilisé.")

        # Convertir la date reçue en un objet datetime
        date_naissance = datetime.strptime(birthdate, "%Y-%m-%d").date()

        # Calculer l'âge
        aujourd_hui = date.today()
        age = aujourd_hui.year - date_naissance.year - (
                (aujourd_hui.month, aujourd_hui.day) < (date_naissance.month, date_naissance.day)
                )

        # Vérifier si l'utilisateur est majeur
        if age < 18:
            raise Exception("L'utilisateur doit être majeur pour s'inscrire.")

        # Hash du mot de passe pour la sécurité
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Créer le nouvel utilisateur
        new_user = {
            "FirstName": FirstName,
            "LastName": LastName,
            "birthdate": birthdate,
            "email": email,
            "password": hashed_password.decode('utf-8')
        }
        db["users"].insert_one(new_user)
        return Register(user=UserType(
            FirstName=FirstName,
            LastName=LastName,
            birthdate=birthdate,
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
        print(password)


        user = db["users"].find_one({"email": email})

        if not user:
            raise Exception("l'utilsateur n'existe pas")



        print("Connexion réussie.")
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
