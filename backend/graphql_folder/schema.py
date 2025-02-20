import graphene
from bson import ObjectId
from graphene import ObjectType, String, List, Int, Field
from database import events_collection  # Import de la connexion MongoDB

# Définition du modèle GraphQL
class EventType(ObjectType):
    id = graphene.String()
    name = String()
    description = String()
    cover = String()
    date = String()
    location = String()
    guestsList = List(String)
    invitesNumber = Int()
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

    all_events = List(EventType)
    def resolve_all_events(self, info):
        events = events_collection.find()
        return [
            EventType(
                id=str(event["_id"]),
                name=event["name"],
                description=event.get("description", ""),
                date=event["date"],
                location=event["location"],
                invitesNumber=event["invitesNumber"],
                guestsList=event.get("guestsList", [])
            )
            for event in events
        ]

    event = Field(EventType, id=String())
    def resolve_event(self, info, id):
        return events_collection.find_one({"_id": ObjectId(id)})

    email = graphene.String()
