from app import *
from flask_graphql import GraphQLView
import graphene
from flask_cors import CORS  # 🔹 Importer CORS

# Mutation pour récupérer les champs sans authentification
class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, email, password):
        print("Données reçues par Flask :")
        print(f"Email: {email}")
        print(f"Password: {password}")
        return LoginMutation(message="Données reçues avec succès")

class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()

schema = graphene.Schema(mutation=Mutation)