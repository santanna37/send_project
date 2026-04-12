from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from pathlib import Path
import os


# Isso garante que as variáveis carreguem assim que o arquivo for lido
env_path = Path(__file__).parent.parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
#print(os.environ)
# -----------------------------------

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__conection_string = os.getenv("DATABASE_URL")

        self.__engine = self.__create_database_engine()
        self.session: Session = None

    def __create_database_engine(self):
        engine = create_engine(self.__conection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self) -> Session:
        session_make = sessionmaker(bind = self.__engine)
        self.session = session_make()
        return self.session 

    def __exit__(self, exc_type, exc_val,  exc_tb):
        if self.session:
            self.session.close()
