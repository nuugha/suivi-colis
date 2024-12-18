# globals.py
import json

# Nom du fichier pour stocker la variable
STATE_FILE = "state.json"

# Charger la valeur de user_globale à partir du fichier
def load_user():
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("user_globale", None)  # Retourne None si la clé n'existe pas
    except FileNotFoundError:
        return None  # Si le fichier n'existe pas encore

# Sauvegarder la valeur de user_globale dans le fichier
def save_user(value):
    with open(STATE_FILE, "w") as f:
        json.dump({"user_idg": value}, f)

# Initialisation de la variable globale
user_idg = load_user()

# Session variable
_usrcon = False

def get_usrcon():
    global _usrcon
    return _usrcon

def set_usrcon(value):
    global _usrcon
    _usrcon = value
from dotenv import load_dotenv, set_key, find_dotenv
import os

class SessionConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionConfig, cls).__new__(cls)
            cls._instance.env_file = '.env'
            load_dotenv(cls._instance.env_file)
        return cls._instance
    
    def set(self, key, value):
        set_key(self.env_file, key, str(value))
        os.environ[key] = str(value)
    
    def get(self, key, default=None):
        return os.getenv(key, default)
    
    def clear(self):
        with open(self.env_file, 'w') as f:
            f.write('')
        os.environ.clear()
