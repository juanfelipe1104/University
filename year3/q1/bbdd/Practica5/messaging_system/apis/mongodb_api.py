from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId


class MongoAPI:
    """
    MongoDB:
        - messages: histórico/log de mensajes
        - snapshots: versionado del estado completo (Neo4j + Redis + histórico Mongo)
    """

    def __init__(self, mongo_uri: str = "mongodb://localhost:27017/", db_name: str = "messaging"):
        """
        Inicializa conexión a MongoDB.
        """

        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]
        self.messages = self._db["messages"]
        self.snapshots = self._db["snapshots"]
        self.__ensure_indexes()

    def close(self) -> None:
        """
        Cierra la conexión a MongoDB.
        """

        self._client.close()
    
    def __ensure_indexes(self) -> None:
        """
        Crea los índices necesarios en las colecciones.
        """
        self.messages.drop_indexes()
        # messages
        self.messages.create_index([("timestamp", ASCENDING)])
        self.messages.create_index([("rel_id", ASCENDING), ("timestamp", ASCENDING)])
        self.messages.create_index([("sender_id", ASCENDING), ("timestamp", ASCENDING)])
        self.messages.create_index([("receiver_id", ASCENDING), ("timestamp", ASCENDING)])
        self.messages.create_index([("msg_id", ASCENDING)], unique=True)

        self.snapshots.drop_indexes()
        # snapshots
        self.snapshots.create_index([("created_at", DESCENDING)])
        self.snapshots.create_index([("name", ASCENDING)])

    def insert_message(self, message: dict) -> str:
        """
        Inserta un mensaje en el histórico.
        Si no viene timestamp, se añade.
        Devuelve id (string) del documento insertado.
        """

        doc = dict(message)
        doc.setdefault("timestamp", datetime.now(timezone.utc))
        res = self.messages.insert_one(doc)
        return str(res.inserted_id)

    def get_message_by_id(self, _id: str) -> dict | None:
        """
        Obtiene un mensaje por su ObjectId.
        Devuelve None si no existe.
        """

        doc = self.messages.find_one({"_id": ObjectId(_id)})
        return doc

    def get_message_by_msg_id(self, msg_id: str) -> dict | None:
        """
        Obtiene un mensaje por su msg_id (identificador único del mensaje).
        Devuelve None si no existe.
        """

        doc = self.messages.find_one({"msg_id": msg_id})
        return doc

    def list_messages(self, limit: int = 50, newest_first: bool = True) -> list[dict]:
        """
        Lista mensajes del histórico.
        Por defecto, los más recientes primero.
        """

        sort = DESCENDING if newest_first else ASCENDING
        docs = list(self.messages.find().sort("timestamp", sort).limit(limit))
        return docs

    def delete_message_by_msg_id(self, msg_id: str) -> int:
        """
        Elimina un mensaje por su msg_id.
        Devuelve el número de documentos eliminados (0 o 1).
        """

        res = self.messages.delete_one({"msg_id": msg_id})
        return int(res.deleted_count)

    def clear_messages(self) -> int:
        """
        Elimina todos los mensajes del histórico.
        Devuelve el número de documentos eliminados.
        """

        res = self.messages.delete_many({})
        return int(res.deleted_count)
    
    def count_messages_by_time_for_relation(self, rel_id: str, time: str = "day", start: datetime | None = None, end: datetime | None = None) -> list[dict]:
        """
        Agregación por tiempo para una relación determinada (rel_id).
        time: "hour" | "day" | "month"
        Devuelve lista [{periodo: <datetime/str>, count: <int>}]
        """

        format = {
            "hour": "%Y-%m-%d %H:00",
            "day": "%Y-%m-%d",
            "month": "%Y-%m",
        }.get(time)
        if format is None:
            raise ValueError("time debe ser 'hour', 'day' o 'month'")

        match = {"rel_id": rel_id}
        if start or end:
            match["timestamp"] = {}
            if start:
                match["timestamp"]["$gte"] = start
            if end:
                match["timestamp"]["$lte"] = end
        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": {"$dateToString": {"format": format, "date": "$timestamp"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}},
            {"$project": {"_id": 0, "periodo": "$_id", "count": 1}}
        ]
        return list(self.messages.aggregate(pipeline))

    def count_messages_by_user(self, user_id: str, role: str = "sender") -> int:
        """
        Agregación por usuario (conteo).
        role: "sender" o "receiver" o "either"
        """

        if role == "sender":
            return int(self.messages.count_documents({"sender_id": user_id}))
        if role == "receiver":
            return int(self.messages.count_documents({"receiver_id": user_id}))
        if role == "either":
            return int(self.messages.count_documents({"$or": [{"sender_id": user_id}, {"receiver_id": user_id}]}))
        
        raise ValueError("role debe ser 'sender', 'receiver' o 'either'")

    def create_snapshot_document(self, name: str, neo4j_nodes: list[dict], neo4j_relationships: list[dict], redis_queues: list[dict], mongo_messages: list[dict] | None = None) -> str:
        """
        Crea un snapshot completo (documento) en MongoDB.
        Si mongo_messages es None, se usan todos los mensajes actuales.
        Devuelve id (string) del snapshot creado.
        """

        if mongo_messages is None:
            mongo_messages = list(self.messages.find({}, {"_id": 0}))  # Excluir _id

        stats = {
            "total_messages": len(mongo_messages),
            "num_nodes": len(neo4j_nodes),
            "num_relationships": len(neo4j_relationships),
            "num_queued": sum(len(q.get("items", [])) for q in redis_queues),
        }

        doc = {
            "name": name,
            "created_at": datetime.now(timezone.utc),
            "neo4j": {"nodes": neo4j_nodes, "relationships": neo4j_relationships},
            "redis": {"queues": redis_queues},
            "mongo": {"messages": mongo_messages},
            "stats": stats
        }
        res = self.snapshots.insert_one(doc)
        return str(res.inserted_id)

    def list_snapshots(self, limit: int = 20) -> list[dict]:
        """
        Lista snapshots guardados, sin incluir los mensajes.
        Ordenados por fecha de creación (más recientes primero).
        """

        docs = list(self.snapshots.find({}, {"mongo.messages": 0}).sort("created_at", DESCENDING).limit(limit))
        return docs

    def get_snapshot(self, snapshot_id: str) -> dict | None:
        """
        Obtiene un snapshot completo por su ObjectId.
        Devuelve None si no existe.
        """

        doc = self.snapshots.find_one({"_id": ObjectId(snapshot_id)})
        return doc

    def delete_snapshot(self, snapshot_id: str) -> int:
        """
        Elimina un snapshot por su ObjectId.
        Devuelve el número de documentos eliminados (0 o 1).
        """

        res = self.snapshots.delete_one({"_id": ObjectId(snapshot_id)})
        return int(res.deleted_count)
    
    def clear_snapshots(self) -> int:
        """
        Elimina todos los snapshots.
        Devuelve el número de documentos eliminados.
        """

        res = self.snapshots.delete_many({})
        return int(res.deleted_count)

    def compare_snapshots(self, name_a: str, name_b: str) -> dict:
        """
        Compara dos snapshots por nombre.
        Devuelve estadísticas de cada uno y la diferencia (B - A).
        """

        snap_a: dict = self.snapshots.find_one({"name": name_a})
        snap_b: dict = self.snapshots.find_one({"name": name_b})

        if snap_a is None or snap_b is None:
            raise ValueError("Uno o ambos snapshots no existen")

        stats_a = snap_a.get("stats", {})
        stats_b = snap_b.get("stats", {})

        keys = [
            "total_messages",
            "num_nodes",
            "num_relationships",
            "num_queued"
        ]

        def normalize(stats: dict) -> dict:
            return {k: int(stats.get(k, 0)) for k in keys}

        a = normalize(stats_a)
        b = normalize(stats_b)

        diff = {k: b[k] - a[k] for k in keys}

        return {
            "snapshot_a": {
                "name": snap_a.get("name"),
                "created_at": snap_a.get("created_at"),
                **a
            },
            "snapshot_b": {
                "name": snap_b.get("name"),
                "created_at": snap_b.get("created_at"),
                **b
            },
            "diff": diff
        }
