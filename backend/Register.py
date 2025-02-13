from app import *

class UserType(graphene.ObjectType):
    FirstName = graphene.String()
    LastName = graphene.String()
    birthdate = graphene.String()
    email = graphene.String()

class Register(graphene.Mutation):
    class Arguments:
        FirstName = graphene.String(required=True)
        LastName = graphene.String(required=True)
        birthdate = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, FirstName, LastName, birthdate, email, password):
        print("Nouvel utilisateur enregistré :")
        print(f"Prénom: {FirstName}")
        print(f"Nom: {LastName}")
        print(f"Date de naissance: {birthdate}")
        print(f"Email: {email}")
        print(f"Mot de passe: (non affiché pour la sécurité) {password} ")

        return Register(user=UserType(
            FirstName=FirstName,
            LastName=LastName,
            birthdate=birthdate,
            email=email
        ))

# Définition du schéma GraphQL
class Mutation(graphene.ObjectType):
    register = Register.Field()

# Définition du schéma GraphQL
schema = graphene.Schema(mutation=Mutation)