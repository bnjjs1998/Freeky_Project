from app import *

class UserType(graphene.ObjectType):
    FirstName = graphene.String()
    LastName = graphene.String()
    birthday = graphene.String()
    email = graphene.String()

class Register(graphene.Mutation):
    class Arguments:
        FirstName = graphene.String(required=True)
        LastName = graphene.String(required=True)
        birthday = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, FirstName, LastName, birthday, email, password):
        print("Nouvel utilisateur enregistré :")
        print(f"Prénom: {FirstName}")
        print(f"Nom: {LastName}")
        print(f"Date de naissance: {birthday}")
        print(f"Email: {email}")
        print(f"Mot de passe: (non affiché pour la sécurité) {password} ")

        return Register(user=UserType(
            FirstName=FirstName,
            LastName=LastName,
            birthday=birthday,
            email=email
        ))

# Définition du schéma GraphQL
class Mutation(graphene.ObjectType):
    register = Register.Field()

# Définition du schéma GraphQL
schema = graphene.Schema(mutation=Mutation)