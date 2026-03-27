from apis.messageData import MessageData
from apis.neo4j_api import Neo4jAPI
from apis.redis_api import RedisAPI
from apis.mongodb_api import MongoAPI
from apis.relationData import make_rel_id


class MessagingService:
    """
    Servicio de mensajería que integra Neo4j, Redis y MongoDB:
    - send_message: Redis enqueue + Neo4j increment
    - consume_message: Redis BLPOP + Mongo insert (histórico)
    """

    def __init__(self, neo4j_api: Neo4jAPI, redis_api: RedisAPI, mongo_api: MongoAPI):
        self.neo4j = neo4j_api
        self.redis = redis_api
        self.mongo = mongo_api

    def send_message(self, sender_id: str, receiver_id: str, content: str, metadata: dict | None = None) -> MessageData:
        """
        Envia (encola) un mensaje en Redis para la relación sender->receiver y
        actualiza la cuenta en Neo4j (msg_count) asociada a esa relación.

        Nota: MongoDB se actualiza en consume_message (histórico al consumir),
        siguiendo el flujo recomendado.
        """
        rel_id = make_rel_id(sender_id, receiver_id)
        msg = MessageData(sender_id=sender_id, receiver_id=receiver_id, content=content, rel_id=rel_id, metadata=metadata)

        # Mensaje en Redis
        self.redis.enqueue_message(rel_id, msg.to_redis_dict())

        # Incrementar contador en Neo4j
        try:
            self.neo4j.increment_message_count(rel_id)
            return msg
        except Exception as e:
            raise RuntimeError(f"Redis encoló mensaje pero Neo4j no pudo incrementar: {e}")

    def consume_message(self, rel_id: str, timeout: int = 5) -> MessageData | None:
        """
        Consume (bloqueante) un mensaje desde Redis y lo guarda en MongoDB (histórico).
        Devuelve el mensaje o None si timeout.
        """
        # Consumir mensaje de Redis
        msg = self.redis.consume_blocking(rel_id, timeout)
        if msg is None:
            return None
        # Guardar en MongoDB
        self.mongo.insert_message(msg.to_dict())
        return msg

    def consume_by_users(self, sender_id: str, receiver_id: str, timeout: int = 5) -> MessageData | None:
        rel_id = make_rel_id(sender_id, receiver_id)
        return self.consume_message(rel_id, timeout)