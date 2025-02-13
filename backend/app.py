from flask import Flask, request, jsonify
from flask_cors import CORS
import graphene
from graphene import Schema
from graphql_folder.schema import Query
from graphql_folder.mutations import Mutation


app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app)

# Définition du schéma GraphQL
schema = Schema(query=Query, mutation=Mutation)

# app.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
# )

# Route GraphQL
@app.route('/')
def hello_world():  # put application's code here
    return {"message": "API Flask + GraphQL + MongoDB is ok !"}


if __name__ == '__main__':
    app.run(debug=True)
