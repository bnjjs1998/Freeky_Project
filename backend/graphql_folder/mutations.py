import graphene
from graphene import ObjectType, String, Field, Boolean
from database import events_collection  # Import de la connexion MongoDB
from graphql_folder.schema import EventType  # Import du modèle GraphQL
from graphql_folder.schema import UserType  # Import du modèle GraphQL
from graphql_folder.schema import Query

# Mutation pour ajouter une soirée
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
        new_event = {
            "name": name,
            "date": date,
            "location": location,
            "guests_list": guests_list,
            "invites_number": invites_number
        }
        events_collection.insert_one(new_event)  # Ajout dans MongoDB
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

    def mutate(self, info, FirstName, LastName, birthdate, email, password):
        # Vérifier si l'email existe déjà
        existing_user = db["users"].find_one({"email": email})
        if existing_user:
            raise Exception("Cet email est déjà utilisé.")

        # Hash du mot de passe pour la sécurité
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Créer le nouvel utilisateur
        new_user = {
            "lirstName": firstName,
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

    message = graphene.String()

    def mutate(self, info, email, password):
        # Simuler la vérification de l'existence de l'utilisateur
        print(f"Vérification de l'utilisateur avec l'email : {email}")
        print(password)
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



# Fusion des mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = LoginMutation.Field()

# Définition du schéma GraphQL (Query + Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)
