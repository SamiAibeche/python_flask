import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

load_dotenv()  # Load environment variables from .env file


class MongoDb:
    def __init__(self):

        self.DB_HOST = os.getenv("DB_HOST") or 'localhost'
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_URI = f"mongodb://{self.DB_HOST}/"

    def connect_db(self):
        """ Connect to MongoDB and return the database handle. """
        try:
            # Create a MongoClient to the running mongod instance
            client = MongoClient(self.DB_URI, serverSelectionTimeoutMS=5000)
            # Test connection by calling the server_info() method
            client.server_info()  # Will throw an exception if connection fails
            db = client[self.DB_NAME]
            print("MongoDB connection successful.")
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            db = None  # Ensure db is None if connection failed
        return db

    def fetch_all(self):
        """ Fetch all documents from the 'users' collection. """
        db = self.connect_db()
        if db is not None:
            # Querying the collection
            users_collection = db.users
            # Projecting specific fields
            projection = {'_id': 1, 'lastname': 1, 'firstname': 1, 'gender': 1, 'email': 1, 'message': 1, 'subjects': 1}
            try:
                result = list(users_collection.find({}, projection))
                print("Data retrieval successful.")
                return result
            except Exception as e:
                print(f"Error retrieving data: {e}")
        else:
            print("Database connection is not established.")
            return None



    def fetch_one_by(self, id):
        """ Fetches a single document from the 'users' collection by ID. """
        db = self.connect_db()
        if db is not None:
            # Access the collection
            users_collection = db.users
            try:
                # Find a single document by its ObjectId
                result = users_collection.find_one({"_id": ObjectId(id)},
                                                   {"gender": 1, "firstname": 1, "lastname": 1, "email": 1,
                                                    "message": 1, "subjects": 1, "country": 1})
                print("Document retrieval successful.")
                return result
            except Exception as e:
                print(f"Error retrieving document: {e}")
                return None
        else:
            print("Database connection is not established.")
            return None

    def delete_one_by(self, id):
        """ Deletes a single document from the 'users' collection by ID. """
        db = self.connect_db()
        if db is not None:
            # Access the collection
            users_collection = db.users
            try:
                # Convert the string ID to an ObjectId
                result = users_collection.delete_one({"_id": ObjectId(id)})
                if result.deleted_count > 0:
                    print("Document deleted successfully.")
                else:
                    print("No document found with the given ID.")
            except Exception as e:
                print(f"Error deleting document: {e}")
        else:
            print("Database connection is not established.")

    def insert_datas(self, gender, firstname, lastname, email, message, subjects, country='Be'):
        """ Inserts data into the 'users' collection. """
        db = self.connect_db()
        if db is not None:
            # Access the collection
            users_collection = db.users
            # Create a document to insert
            document = {
                'gender': gender,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'message': message,
                'subjects': subjects,
                'country': country
            }
            try:
                # Insert the document into the collection
                result = users_collection.insert_one(document)
                print(f"Document inserted successfully with id: {result.inserted_id}")
            except Exception as e:
                print(f"Error inserting document: {e}")
        else:
            print("Database connection is not established.")

