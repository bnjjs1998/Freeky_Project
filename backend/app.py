from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app, origins=["http://localhost:5173"])

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Bienvenue sur le site d'hébergement de soirées !"

schema = graphene.Schema(query=Query)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    app.run()
