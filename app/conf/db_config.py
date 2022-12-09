import os

import pymongo
from dotenv import load_dotenv

load_dotenv()
# configuraciones del cliente de mongo para hacer inserciones
BD=os.getenv('ACCESS_TO_DB')
client = pymongo.MongoClient(BD)
mydb = client["crud"]
mycol = mydb["empresas"]
