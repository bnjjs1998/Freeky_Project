from datetime import datetime, date

import bcrypt
import graphene
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from graphene import ObjectType, String, Field, Boolean
 # Import de la connexion MongoDB
from .schema import EventType
from .schema import UserType
from .schema import Query
from backend import database
from backend.database import events_collection, db


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        date = graphene.String(required=True)
        location = graphene.String(required=True)
        guests_list = graphene.List(graphene.String) # Liste des invités (optionnel ?)
        invites_number = graphene.Int(required=True)

    success = graphene.Boolean()
    event = graphene.Field(EventType)

    def mutate(self, info, name, date, location, guests_list, invites_number):
        nouvelle_soiree = {
            "name": name,
            "date": date,
            "location": location,
            "guests_list": guests_list,
            "invites_number": invites_number
        }


        events_collection.insert_one(nouvelle_soiree)  # Ajout dans MongoDB
        return CreateEvent(success=True, event=nouvelle_soiree)

# Ajouter la mutation au schéma
class Mutation(ObjectType):
    create_event = CreateEvent.Field()

# Mutation pour l'enregistrement d'un utilisateur
class Register(graphene.Mutation):
    class Arguments:
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        birthdate = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, firstName, lastName, birthdate, email, password):
        print(firstName, lastName, birthdate, email, password)
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
            "firstName": firstName,
            "lastName": lastName,
            "birthdate": birthdate,
            "email": email,
            "password": hashed_password.decode('utf-8')
        }

        db["users"].insert_one(new_user)

        return Register(user=UserType(
            firstName=firstName,
            lastName=lastName,
            birthdate=birthdate,
            email=email
        ))

class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)
    message = graphene.String()

    def mutate(self, info, email, password):
        # 🔍 Recherche de l'utilisateur dans la base de données
        user_data = db['users'].find_one({"email": email})
        if not user_data:
            raise Exception("Utilisateur non trouvé.")

        # 🔑 Vérification du mot de passe
        if not check_password_hash(user_data["password"], password):
            raise Exception("Mot de passe incorrect.")

        # 🔥 Génération du token JWT
        token = create_access_token(identity=str(user_data["_id"]))

        # 📌 Construction de la réponse utilisateur
        user = UserType(
            email=user_data["email"],
            firstName=user_data.get("firstName", "Inconnu")  # Utilise "Inconnu" si firstName n'existe pas
        )

        return LoginMutation(
            token=token,
            user=user,
            message="Connexion réussie."
        )
# Fusion des mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = LoginMutation.Field()

# Définition du schéma GraphQL (Query + Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)
