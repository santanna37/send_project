from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from datetime import datetime



logger = logging.getLogger(__name__)



# Carrega .env
env_path = Path(__file__).parent.parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)



class DBConnectionHandler:
    _engine = None

    def __init__(self) -> None:
        if DBConnectionHandler._engine is None:
            self._initialize_engine()
        self.session = None

    def _initialize_engine(self):
        ambiente = os.getenv("AMBIENTE", "LOCAL")

        if ambiente == "LOCAL":
            connection_string = os.getenv("DATABASE_URL_LOCAL")
        elif ambiente == "ONLINE":
            connection_string = os.getenv("DATABASE_URL")
        else:
            raise ValueError(f"AMBIENTE inválido: {ambiente}")

        if not connection_string:
            raise ValueError(f"String de conexão não encontrada para ambiente: {ambiente}")

        print(f"🚀 [DB] Conectando em: {ambiente} | {datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"Conectando ao banco em: {ambiente}")

        DBConnectionHandler._engine = self._create_engine(connection_string)

    def _create_engine(self, connection_string: str):
        # Configurações diferentes para MySQL e PostgreSQL
        if "postgresql" in connection_string:
            connect_args = {
                "connect_timeout": 10,
                "sslmode": "require",
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            }
        else:  # MySQL
            connect_args = {"connect_timeout": 10}

        return create_engine(
            connection_string,
            pool_size=5,
            max_overflow=3,
            pool_timeout=300,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args=connect_args,
            echo=False
        )

    def get_engine(self):
        return DBConnectionHandler._engine

    def __enter__(self) -> Session:
        session_maker = sessionmaker(bind=DBConnectionHandler._engine)
        self.session = session_maker()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()