import graphene
from graphene import ObjectType, String, Field, Boolean
from database import events_collection  # Import de la connexion MongoDB
from graphql_folder.schema import EventType  # Import du modèle GraphQL

# Mutation pour ajouter une soirée
class CreateEvent(graphene.Mutation):
    class Arguments:
        nom = graphene.String(required=True)
        date = graphene.String(required=True)
        lieu = graphene.String(required=True)
        guests_list = graphene.List(graphene.String) # Liste des invités (optionnel ?)
        invites_number = graphene.Int(required=True)

    success = graphene.Boolean()
    event = graphene.Field(EventType)

    def mutate(self, info, nom, date, lieu, guests_list, invites_number):
        nouvelle_soiree = {
            "nom": nom,
            "date": date,
            "lieu": lieu,
            "guests_list": guests_list,
            "invites_number": invites_number
        }
        events_collection.insert_one(nouvelle_soiree)  # Ajout dans MongoDB
        return CreateSoiree(success=True, event=nouvelle_soiree)

# Ajouter la mutation au schéma
class Mutation(ObjectType):
    create_event = CreateEvent.Field()
