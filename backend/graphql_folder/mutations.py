import graphene
from graphene import ObjectType, String, Field, Boolean, List, Int
from database import events_collection  # Import de la connexion MongoDB
from graphql_folder.schema import EventType, UserType  # Import des modèles GraphQL

# Mutation pour ajouter un événement
class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        date = graphene.String(required=True)
        location = graphene.String(required=True)
        invitesNumber = graphene.Int(required=True)

    success = graphene.Boolean()
    event = graphene.Field(EventType)

    def mutate(self, info, name, description, date, location, invitesNumber):
        new_event = {
            "name": name,
            "description": description if description else "",
            "date": date,
            "location": location,
            "invitesNumber": invitesNumber
        }
        inserted_event = events_collection.insert_one(new_event)
        new_event["id"] = str(inserted_event.inserted_id)
        return CreateEvent(success=True, event=EventType(
            name=new_event["name"],
            description=new_event["description"],
            date=new_event["date"],
            location=new_event["location"],
            guestsList=[],  # Ajout de guestsList vide par défaut
            invitesNumber=new_event["invitesNumber"]
        ))

# Mutation pour l'enregistrement d'un utilisateur
class Register(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        birthdate = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, first_name, last_name, birthdate, email, password):
        from database import db  # Import de la connexion MongoDB
        import bcrypt

        # Vérifier si l'email existe déjà
        existing_user = db["users"].find_one({"email": email})
        if existing_user:
            raise Exception("Cet email est déjà utilisé.")

        # Hash du mot de passe pour la sécurité
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Créer le nouvel utilisateur
        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "email": email,
            "password": hashed_password.decode('utf-8')
        }
        db["users"].insert_one(new_user)

        return Register(user=UserType(
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            email=email
        ))

# Mutation pour la connexion d'un utilisateur
class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, email, password):
        from database import db
        import bcrypt

        user = db["users"].find_one({"email": email})
        if not user:
            raise Exception("Utilisateur non trouvé.")

        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            raise Exception("Mot de passe incorrect.")

        return LoginMutation(message="Connexion réussie.")

# Fusion des mutations
class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    register = Register.Field()
    login = LoginMutation.Field()
