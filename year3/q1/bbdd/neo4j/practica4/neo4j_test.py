import neo4j_db, neo4j_api

db = neo4j_db.Neo4jDB(neo4j_db.URI, neo4j_db.USER, neo4j_db.PASSWORD)
neo4j_db.reset_db(db)

# Datos base
for uid, nombre in [("u1","Pablo"),("u2","Lucía"),("u3","Carlos"),("u4","Ana"),("u5","Javier"),("u6","María")]:
    neo4j_api.create_user(db, uid, nombre)

for eid, nombre in [("e1","Google"),("e2","Amazon")]:
    neo4j_api.create_empresa(db, eid, nombre)

for cid, nombre in [("c1","UPM"),("c2","UAM")]:
    neo4j_api.create_centro(db, cid, nombre)

# Conexiones
neo4j_api.add_friend(db, "u1","u2")
neo4j_api.add_friend(db, "u2","u3")
neo4j_api.add_friend(db, "u3","u4")

neo4j_api.add_family(db, "u1","u5")
neo4j_api.add_family(db, "u5","u6")
neo4j_api.add_family(db, "u2","u4")

# Empresa / Centro Educativo
neo4j_api.add_work(db, "u1","e1")
neo4j_api.add_work(db, "u2","e1")
neo4j_api.add_work(db, "u4","e1")
neo4j_api.add_work(db, "u3","e2")

neo4j_api.add_study(db, "u1","c1")
neo4j_api.add_study(db, "u2","c1")
neo4j_api.add_study(db, "u3","c2")

# Mensajes
neo4j_api.send_message(db, "u1","u2","m1","c1",1,"2024-01-01","Hola Lucía")
neo4j_api.send_message(db, "u2","u1","m2","c1",2,"2024-01-02","Hola Pablo")
neo4j_api.send_message(db, "u1","u3","m3","c2",1,"2024-02-01","Hola Carlos")
neo4j_api.send_message(db, "u2", "u3", "m4", "c3", 1, "2024-02-10", "Hola Carlos, qué tal?")

# Publicaciones + menciones
neo4j_api.create_post(db, "u1", "p1", "Proyecto IA", "2024-03-01")
neo4j_api.mention_user_in_post(db, "p1", "u2")
neo4j_api.mention_user_in_post(db, "p1", "u4")

# Consultas
print("\n[A1] Amigos y familiares de u1")
print(neo4j_api.friends_and_family(db, "u1"))

print("\n[A2] Familiares de familiares de u1")
print(neo4j_api.family_of_family(db, "u1"))

print("\n[B1] Mensajes u2 -> u1 después de 2024-01-01")
print(neo4j_api.messages_after_date(db, "u2", "u1", "2024-01-01"))

print("\n[B2] Conversación completa u1 <-> u2")
print(neo4j_api.conversation_full(db, "u1", "u2"))

print("\n[C1] Mencionados por u1 que trabajan con u1")
print(neo4j_api.mentions_with_work_relation(db, "u1"))

print("\n[D1] Nuevas conexiones por saltos (max_hops=2) desde u1")
print(neo4j_api.new_connections_by_hops(db, "u1", 2))

print("\n[D2] Nuevas conexiones por mensajes (min_msgs=0) desde u1")
print(neo4j_api.new_connections_by_messages(db, "u1", 0))

db.close()