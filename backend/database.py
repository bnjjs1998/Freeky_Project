from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["freeky_db"]
events_collection = db["events"]

# Insert de données dans la base de données MongoDB
db.events.insert_many([
  { "name": "Soirée Étudiante", "date": "2025-03-10", "location": "Paris", "guests_list": ["Alice", "Bob", "Charlie"], "invites_number": 50 },
  { "name": "Anniversaire Alex", "date": "2025-04-05", "location": "Lyon", "guests_list": ["Alex", "Billy", "Charles"], "invites_number": 30 },
  { "name": "Réunion Startup", "date": "2025-05-15", "location": "Bordeaux", "guests_list": ["Alexandre", "Charlotte", "Franck"], "invites_number": 20 },
])