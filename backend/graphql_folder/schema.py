import graphene
from graphene import ObjectType, String, List, Int
from database import events_collection  # Import de la connexion MongoDB

# Définition du modèle GraphQL
class EventType(ObjectType):
    nom = String()
    date = String()
    lieu = String()
    guests_list = List(String)
    invites_number = Int()

# Query GraphQL
class Query(ObjectType):
    events = List(EventType)

    def resolve_soirees(self, info):
        return list(events_collection.find({}, {"_id": 0}))
