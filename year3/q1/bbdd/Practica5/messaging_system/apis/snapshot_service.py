from apis.mongodb_api import MongoAPI
from apis.redis_api import RedisAPI
from apis.neo4j_api import Neo4jAPI

class SnapshotService:
    """
    Servicio de snapshots para el sistema de mensajería:
    - create_snapshot: exporta Neo4j + Redis + Mongo y lo guarda en MongoDB.snapshots
    - restore_snapshot: borra todo y reconstruye desde snapshot
    """

    def __init__(self, mongo_api: MongoAPI, neo4j_api: Neo4jAPI, redis_api: RedisAPI):
        self.mongo = mongo_api
        self.neo4j = neo4j_api
        self.redis = redis_api

    def create_snapshot(self, name: str) -> str:
        # Exportar neo4j
        nodes = self.neo4j.export_nodes()
        rels = self.neo4j.export_relationships()

        # Exportar redis
        queues = self.redis.export_queues_state()

        # Exportar Mongo mensajes
        messages = list(self.mongo.messages.find({}, {"_id": 0}))

        # Guardar snapshot en Mongo
        snapshot_id = self.mongo.create_snapshot_document(
            name=name,
            neo4j_nodes=nodes,
            neo4j_relationships=rels,
            redis_queues=queues,
            mongo_messages=messages
        )
        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> None:
        snap = self.mongo.get_snapshot(snapshot_id)
        if snap is None:
            raise ValueError("Snapshot no existe")

        # Borrar estado actual (sobrescribir lo que haya)
        self.neo4j.clear_graph()
        self.redis.clear_all_queues()
        self.mongo.clear_messages()

        # Restaurar neo4j
        neo = snap.get("neo4j")
        self.neo4j.import_nodes(neo.get("nodes", []))
        self.neo4j.import_relationships(neo.get("relationships", []))

        # Restaurar Redis
        red = snap.get("redis")
        self.redis.import_queues_state(red.get("queues", []))

        # Restaurar Mongo histórico
        msgs = snap.get("mongo", {}).get("messages", [])
        if msgs:
            self.mongo.messages.insert_many(msgs)