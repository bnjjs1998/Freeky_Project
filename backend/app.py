from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene import Schema
from graphql.schema import Query as QuerySchema
from graphql.mutations import Mutation


app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app)

# Définition du schéma GraphQL
schema = Schema(query=QuerySchema, mutation=Mutation)

# Route GraphQL
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@app.route('/')
def hello_world():  # put application's code here
    return {"message": "API Flask + GraphQL + MongoDB is ok !"}


if __name__ == '__main__':
    app.run(debug=True)
