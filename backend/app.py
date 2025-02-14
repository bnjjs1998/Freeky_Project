from flask import Flask, request, jsonify
from flask_cors import CORS
import graphene
from graphene import Schema
from graphql_folder.schema import Query
from graphql_folder.mutations import Mutation


app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Définition du schéma GraphQL
schema = Schema(query=Query, mutation=Mutation)

@app.route("/graphql", methods=["POST", "OPTIONS"])
def graphql_server():
    print("Request received")
    if request.method == "OPTIONS":
        print("Options request received")
        return _build_cors_preflight_response()
    
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Requête invalide"}), 400
    result = schema.execute(data["query"])
    if result.errors:
        return jsonify({"errors": [str(error) for error in result.errors]})
    
    return _corsify_actual_response(jsonify(result.data))

# Réponse CORS pour les requêtes pré-vol
@app.before_request
def before_request():
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight CORS OK"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

# Appliquer CORS aux réponses réelles
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    return response

# Route GraphQL
@app.route('/')
def hello_world():  # put application's code here
    return {"message": "API Flask + GraphQL + MongoDB is running !",
        # "events": events
    }


if __name__ == '__main__':
    app.run(debug=True, port=5001)
