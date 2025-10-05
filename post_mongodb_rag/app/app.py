from pymongo import MongoClient
from dotenv import load_dotenv
import logging
import os


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app/mongodb_rag.log")
    ]
)


class MongoConnection:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)

    def get_client(self):
        uri = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"

        try:
            self.logger.info("Tentando conectar ao MongoDB...")
            client = MongoClient(uri, timeoutms=10000)

            self.logger.info("Conexão com MongoDB bem-sucedida!")
            client.admin.command('ping')

            return client
        except Exception as e:
            self.logger.error(
                f"Falha ao conectar ao MongoDB: {e}", exc_info=True)

            raise ConnectionError(
                "Não foi possível conectar ao MongoDB") from e
