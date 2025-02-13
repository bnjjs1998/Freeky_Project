import graphene
from bson import ObjectId
from graphene import ObjectType, String, List, Int, Field
from database import events_collection  # Import de la connexion MongoDB

# Définition du modèle GraphQL
class EventType(ObjectType):
    id = graphene.String()
    name = String()
    description = String()
    date = String()
    location = String()
    guests_list = List(String)
    invites_number = Int()

# Définition du type GraphQL pour les utilisateurs
class UserType(graphene.ObjectType):
    id = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    birthdate = graphene.String()
    email = graphene.String()


# Query GraphQL
class Query(ObjectType):
    users = List(UserType)
    def resolve_users(self, info):
        return list(users_collection.find({}, {"_id": 0}))  # Récupération des utilisateurs depuis MongoDB

    events = List(EventType)
    def resolve_events(self, info):
        return list(events_collection.find({}, {"_id": 0}))

    event = Field(EventType, id=String())
    def resolve_event(self, info, id):
        return events_collection.find_one({"_id": ObjectId(id)})

    email = graphene.String()
