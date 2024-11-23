from pymongo import MongoClient    
from keycloak import KeycloakOpenID
import os

class KeycloakConfig:
    keycloak_openid = None
    UNPROTECTED_ENDPOINTS = None

    keycloakurl = os.getenv("KEYCLOAK_URL", None)
    realmName = os.getenv("KEYCLOAK_REALM", None)
    clientId = os.getenv("KEYCLOAK_CLIENT_ID", None)
    clientSecretKey = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY", None)

    @classmethod
    def initialize(cls, keycloakurl=None, realmName=None, clientId=None, clientSecretKey=None, unProtectedEndpoints=None):
        
        cls.keycloakurl = keycloakurl or cls.keycloakurl 
        cls.realmName = realmName or cls.realmName 
        cls.clientId = clientId or cls.clientId 
        cls.clientSecretKey = clientSecretKey or cls.clientSecretKey 
        
        if not all([cls.keycloakurl, cls.realmName, cls.clientId, cls.clientSecretKey]):
            raise ValueError("All required values (keycloakurl, realmName, clientId, clientSecretKey) must be provided.")
        
        
        cls.UNPROTECTED_ENDPOINTS = unProtectedEndpoints or [
            "/docs", "/redoc", "/openapi.json", 
            "/register", "/login", "/health", 
            "/status", "/verifyToken"
        ]
        
        cls.keycloak_openid = KeycloakOpenID(
            server_url=cls.keycloakurl,
            client_id=cls.clientId,
            realm_name=cls.realmName,
            client_secret_key=cls.clientSecretKey,
            verify=True
        )

class MongoConfig:
    
    mongoDbUrl = os.getenv("MONGO_DB_URL", None)
    databaseName = os.getenv("MONGO_DATABASE_NAME", None)
    collectionName = os.getenv("MONGO_COLLECTION_NAME", None)

    client = None
    db = None
    collection = None

    @classmethod
    def initialize(cls, mongoDbUrl=None, dataBaseName=None, loginCollectionName=None):
        
        cls.mongoDbUrl = mongoDbUrl or cls.mongoDbUrl or os.getenv("MONGO_DB_URL")
        cls.databaseName = dataBaseName or cls.databaseName or os.getenv("MONGO_DATABASE_NAME")
        cls.collectionName = loginCollectionName or cls.collectionName or os.getenv("MONGO_COLLECTION_NAME")
        
        if not all([cls.mongoDbUrl, cls.databaseName, cls.collectionName]):
            raise ValueError("All required values (mongoDbUrl, dataBaseName, loginCollectionName) must be provided.")
        
        cls.client = MongoClient(cls.mongoDbUrl)
        cls.db = cls.client[cls.databaseName]
        cls.collection = cls.db[cls.collectionName]



