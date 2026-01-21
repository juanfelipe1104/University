from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from apis.userData import UserData
from apis.relationData import RelationData
from apis.relationData import make_rel_id

class Neo4jAPI:
    """
    Neo4j:
        API para gestionar usuarios y relaciones de mensajería.
        - Nodos :User { user_id, ... }
        - Relación dirigida :CAN_MESSAGE { rel_id, msg_count, ... }
    """
    
    # Configuración Neo4j

    def __init__(self, uri: str, user: str, password: str) -> None:
        """
        Inicializa el driver de Neo4j.
        """

        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.__create_constraints()

    def close(self) -> None:
        """
        Cierra la conexión al driver.
        """

        self._driver.close()

    def run(self, query: str, **params) -> list:
        """
        Ejecuta una query y devuelve lista de diccionarios (record.data()).
        """

        with self._driver.session() as session:
            result = session.run(query, **params)
            return [record.data() for record in result]
    
    def run_one(self, query: str, **params) -> dict | None:
        """
        Devuelve el primer resultado o None.
        """

        results = self.run(query, **params)
        return results[0] if results else None
    
    def clear_graph(self) -> None:
        """
        Elimina todos los nodos y relaciones de la base de datos.
        """
        self.run("MATCH (n) DETACH DELETE n")

    def __create_constraints(self) -> None:
        """
        Crea constraints/índices básicos.
        """

        queries = [
            "CREATE CONSTRAINT user_id_unique IF NOT EXISTS "
            "FOR (u:User) REQUIRE u.user_id IS UNIQUE",
            "CREATE CONSTRAINT rel_id_unique IF NOT EXISTS "
            "FOR ()-[r:CAN_MESSAGE]-() REQUIRE r.rel_id IS UNIQUE"
        ]
        for q in queries:
            self.run(q)

    # Usuario User

    def __row_to_user(self, row: dict) -> UserData:
        """
        Convierte fila de resultado a UserData.
        """

        u: dict = row.get("u") or {}
        return UserData(user_id=u.get("user_id"), name=u.get("name"), props=dict(u))
    
    def __fetch_user(self, query: str, **params) -> UserData | None:
        """
        Ejecuta query para obtener un usuario.
        """

        row = self.run_one(query, **params)
        return None if row is None else self.__row_to_user(row)

    def create_user(self, user_id: str, name: str = None, **props: dict) -> UserData:
        """
        Crea usuario. Si ya existe o no se pudo crear, lanza ValueError.
        """

        all_props = {"name": name, **props}
        all_props = {k: v for k, v in all_props.items() if v is not None}
        q = """
        CREATE (u:User {user_id:$user_id})
        SET u += $props
        RETURN u
        """
        try:
            user = self.__fetch_user(q, user_id=user_id, props=all_props)
            if user is None:
                raise ValueError(f"User '{user_id}' no se pudo crear.")
            return user
        except Neo4jError as e:
            raise ValueError(f"User '{user_id}' no se pudo crear o ya existe: {e}") from e

    def update_user(self, user_id: str, **props: dict) -> UserData | None:
        """
        Actualiza usuario. Si no existe o no se pudo actualizar, devuelve None.
        """

        props = {k: v for k, v in props.items() if v is not None}
        q = """
        MATCH (u:User {user_id:$user_id})
        SET u += $props
        RETURN u
        """
        return self.__fetch_user(q, user_id=user_id, props=props)

    def get_user(self, user_id: str) -> UserData | None:
        """
        Obtiene usuario por user_id. Si no existe, devuelve None.
        """

        q = "MATCH (u:User {user_id:$user_id}) RETURN u"
        return self.__fetch_user(q, user_id=user_id)

    def delete_user(self, user_id: str) -> bool:
        """
        Elimina usuario por user_id. Devuelve True si se eliminó, False si no.
        """

        q = """
        MATCH (u:User {user_id:$user_id})
        DETACH DELETE u
        RETURN count(u) AS deleted_count
        """
        row: dict = self.run_one(q, user_id=user_id)
        return bool(row and row.get("deleted_count", 0) > 0)
    
    def list_users(self, limit: int = 100) -> list[UserData]:
        """
        Lista usuarios hasta un límite.
        """

        q = "MATCH (u:User) RETURN u ORDER BY u.user_id LIMIT $limit"
        rows = self.run(q, limit=limit)
        return [self.__row_to_user(row) for row in rows]

    # Relación CAN_MESSAGE

    def __row_to_relation(self, row: dict) -> RelationData:
        """
        Convierte fila de resultado a RelationData.
        """

        r: dict = row.get("r") or {}
        return RelationData(rel_id=r.get("rel_id"), from_user_id=row.get("from_id"), to_user_id=row.get("to_id"), msg_count=int(r.get("msg_count", 0)), props=dict(r))

    def __fetch_relation(self, query: str, **params) -> RelationData | None:
        """
        Ejecuta query para obtener una relación.
        """

        row = self.run_one(query, **params)
        return None if row is None else self.__row_to_relation(row)

    def create_relation(self, sender_id: str, receiver_id: str, rel_id: str = None, msg_count: int = 0, **props: dict) -> RelationData:
        """
        Crea relación CAN_MESSAGE entre sender y receiver.
        Si ya existe o no se pudo crear, lanza ValueError.
        """

        if rel_id is None:
            rel_id = make_rel_id(sender_id, receiver_id)
        props = {k: v for k, v in props.items() if v is not None}
        q = """
        MATCH (a:User {user_id:$sender_id}), (b:User {user_id:$receiver_id})
        CREATE (a)-[r:CAN_MESSAGE {rel_id:$rel_id}]->(b)
        SET r.msg_count = $msg_count
        SET r += $props
        RETURN properties(r) AS r, a.user_id AS from_id, b.user_id AS to_id
        """
        try:
            rel = self.__fetch_relation(q, sender_id=sender_id, receiver_id=receiver_id, rel_id=rel_id, msg_count=msg_count, props=props)
            if rel is None:
                raise ValueError("sender o receiver no existen")
            return rel
        except Neo4jError as e:
            raise ValueError(f"No se pudo crear relación {sender_id}->{receiver_id} o ya existe: {e}") from e
    
    def update_relation(self, rel_id: str, **props: dict) -> RelationData | None:
        """
        Actualiza relación CAN_MESSAGE por rel_id.
        Si no existe, devuelve None.
        """

        props = {k: v for k, v in props.items() if v is not None}
        q = """
        MATCH (a:User)-[r:CAN_MESSAGE {rel_id:$rel_id}]->(b:User)
        SET r += $props
        RETURN properties(r) AS r, a.user_id AS from_id, b.user_id AS to_id
        """
        return self.__fetch_relation(q, rel_id=rel_id, props=props)
    
    def get_relation(self, rel_id: str) -> RelationData | None:
        """
        Obtiene relación CAN_MESSAGE por rel_id. Si no existe, devuelve None.
        """

        q = """
        MATCH (a:User)-[r:CAN_MESSAGE {rel_id:$rel_id}]->(b:User)
        RETURN properties(r) AS r, a.user_id AS from_id, b.user_id AS to_id
        """
        return self.__fetch_relation(q, rel_id=rel_id)

    def delete_relation(self, rel_id: str) -> bool:
        """
        Elimina relación CAN_MESSAGE por rel_id. Devuelve True si se eliminó, False si no.
        """

        q = "MATCH ()-[r:CAN_MESSAGE {rel_id:$rel_id}]->() DELETE r RETURN count(r) AS deleted_count"
        row = self.run_one(q, rel_id=rel_id)
        return bool(row and row.get("deleted_count", 0) > 0)
    
    def increment_message_count(self, rel_id: str) -> int:
        """
        Incrementa msg_count de la relación CAN_MESSAGE por rel_id.
        Devuelve el nuevo msg_count. Si no existe la relación, lanza ValueError.
        """
        
        q = """
        MATCH ()-[r:CAN_MESSAGE {rel_id:$rel_id}]->()
        SET r.msg_count =r.msg_count + 1
        RETURN r.msg_count AS mc
        """
        row = self.run_one(q, rel_id=rel_id)
        if row is None:
            raise ValueError(f"No existe relación con rel_id={rel_id}")
        return int(row.get("mc", 0))

    def increment_by_users(self, sender_id: str, receiver_id: str) -> int:
        """
        Incrementa msg_count de la relación CAN_MESSAGE entre sender y receiver.
        Devuelve el nuevo msg_count. Si no existe la relación, lanza ValueError.
        """

        return self.increment_message_count(make_rel_id(sender_id, receiver_id))
    
    # Exportación / Importación (backup/restore)

    def export_nodes(self) -> list[dict]:
        """
        Exporta todos los nodos User.
        """

        q = """
        MATCH (u:User)
        RETURN u.user_id AS user_id, properties(u) AS props
        ORDER BY user_id
        """
        return self.run(q)

    def export_relationships(self) -> list[dict]:
        """
        Exporta todas las relaciones CAN_MESSAGE.
        """

        q = """
        MATCH (a:User)-[r:CAN_MESSAGE]->(b:User)
        RETURN a.user_id AS from_id,
            b.user_id AS to_id,
            r.rel_id AS rel_id,
            properties(r) AS props
        ORDER BY rel_id
        """
        return self.run(q)

    def import_nodes(self, nodes: list[dict]) -> None:
        """
        Importa nodos User desde una lista de diccionarios.
        """

        q = """
        MERGE (u:User {user_id:$user_id})
        SET u += $props
        """
        for n in nodes:
            props = dict(n.get("props", {}))
            self.run(q, user_id=n.get("user_id"), props=props)

    def import_relationships(self, rels: list[dict]) -> None:
        """
        Importa relaciones CAN_MESSAGE desde una lista de diccionarios.
        """

        q = """
        MATCH (a:User {user_id:$from_id}), (b:User {user_id:$to_id})
        MERGE (a)-[r:CAN_MESSAGE {rel_id:$rel_id}]->(b)
        SET r += $props
        """
        for r in rels:
            props = dict(r.get("props", {}))
            self.run(q, from_id=r.get("from_id"), to_id=r.get("to_id"), rel_id=r.get("rel_id"), props=props)

    # Consultas

    def neighbors(self, user_id: str, limit: int = 100) -> list[str]:
        """
        Devuelve lista de user_id vecinos conectados por CAN_MESSAGE.
        """

        q = """
        MATCH (u:User {user_id:$uid})-[:CAN_MESSAGE]-(v:User)
        RETURN DISTINCT v.user_id AS vid
        ORDER BY vid ASC
        LIMIT $limit
        """
        rows = self.run(q, uid=user_id, limit=limit)
        return [r.get("vid") for r in rows]
    
    def neighbors_ordered_by_messages(self, user_id: str, limit: int = 100) -> list[tuple[str, int]]:
        """
        Devuelve lista de tuplas (user_id, total_msg_count) de vecinos conectados por CAN_MESSAGE,
        ordenados por total_msg_count descendente y user_id ascendente.
        """
        
        q = """
        MATCH (u:User {user_id:$uid})-[r:CAN_MESSAGE]-(v:User)
        WITH v, sum(r.msg_count) AS total
        RETURN v.user_id AS vid, total
        ORDER BY total DESC, vid ASC
        LIMIT $limit
        """
        rows = self.run(q, uid=user_id, limit=limit)
        return [(r.get("vid"), int(r.get("total", 0))) for r in rows]
    
    def best_path_by_messages(self, src_user_id: str, dst_user_id: str) -> dict | None:
        """
        Devuelve el camino entre src y dst que maximiza el número de mensajes,
        modelando el coste de cada relación como 1 / msg_count y minimizando
        el coste total del camino.
        """

        q = """
        MATCH (s:User {user_id:$src}), (t:User {user_id:$dst})
        MATCH p = shortestPath((s)-[:CAN_MESSAGE*]->(t))
        WITH p,
            [n IN nodes(p) | n.user_id] AS nodes,
            length(p) AS hops,
            reduce(cost = 0.0, r IN relationships(p) |
                cost + (1.0 / toFloat(coalesce(r.msg_count, 0)+1))
            ) AS total_cost
        RETURN nodes, hops, total_cost
        ORDER BY total_cost ASC
        LIMIT 1
        """

        row = self.run_one(q, src=src_user_id, dst=dst_user_id)
        if row is None:
            return None

        return {
            "nodes": row["nodes"],
            "hops": int(row["hops"]),
            "cost": float(row["total_cost"])
        }
