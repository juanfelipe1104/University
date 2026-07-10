from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "Jfrc2004"

class Neo4jDB:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run(self, query: str, **params) -> list:
        with self.driver.session() as session:
            result = session.run(query, **params)
            return [record.data() for record in result]

def reset_db(db: Neo4jDB):
    db.run("MATCH (n) DETACH DELETE n")