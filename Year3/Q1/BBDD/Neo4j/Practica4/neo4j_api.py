import neo4j_db 

def create_user(db: neo4j_db.Neo4jDB, user_id: str, nombre: str):
    q = """
    CREATE (u:User {id:$id, nombre:$nombre})
    RETURN u.id AS id, u.nombre AS nombre
    """
    db.run(q, id=user_id, nombre=nombre)

def create_empresa(db: neo4j_db.Neo4jDB, emp_id: str, nombre: str):
    q = """
    CREATE (e:Empresa {id:$id, nombre:$nombre})
    """
    db.run(q, id=emp_id, nombre=nombre)

def create_centro(db: neo4j_db.Neo4jDB, centro_id: str, nombre: str):
    q = """
    CREATE (c:CentroEducativo {id:$id, nombre:$nombre})
    """
    db.run(q, id=centro_id, nombre=nombre)

def add_friend(db: neo4j_db.Neo4jDB, a: str, b: str):
    q = """
    MATCH (u1:User {id:$a}), (u2:User {id:$b})
    CREATE (u1)-[:AMIGO]->(u2), (u2)-[:AMIGO]->(u1)
    """
    db.run(q, a=a, b=b)

def add_family(db: neo4j_db.Neo4jDB, a: str, b: str):
    q = """
    MATCH (u1:User {id:$a}), (u2:User {id:$b})
    CREATE (u1)-[:FAMILIAR]->(u2), (u2)-[:FAMILIAR]->(u1)
    """
    db.run(q, a=a, b=b)

def add_work(db: neo4j_db.Neo4jDB, user_id: str, emp_id: str):
    q = """
    MATCH (u:User {id:$u}), (e:Empresa {id:$e})
    CREATE (u)-[:LABORAL]->(e)
    """
    db.run(q, u=user_id, e=emp_id)

def add_study(db: neo4j_db.Neo4jDB, user_id: str, centro_id: str):
    q = """
    MATCH (u:User {id:$u}), (c:CentroEducativo {id:$c})
    CREATE (u)-[:ACADEMICO]->(c)
    """
    db.run(q, u=user_id, c=centro_id)

def send_message(db: neo4j_db.Neo4jDB, from_id: str, to_id: str,
                 msg_id: str, conversacion: str, secuencia: int,
                 fecha: str, texto: str):
    q = """
    MATCH (a:User {id:$from}), (b:User {id:$to})
    CREATE (a)-[:ENVIA]->(m:Mensaje {
        id:$msg_id, conversacion:$conv, secuencia:$seq,
        fecha: date($fecha), texto:$texto
    })-[:A]->(b)
    """
    db.run(q, **{
        "from": from_id, "to": to_id, "msg_id": msg_id,
        "conv": conversacion, "seq": secuencia,
        "fecha": fecha, "texto": texto
    })

def create_post(db: neo4j_db.Neo4jDB, user_id: str, post_id: str, titulo: str, fecha_iso: str) -> None:
    q = """
    MATCH (u:User {id:$uid})
    CREATE (p:Publicacion {id:$pid, titulo:$titulo, fecha:date($fecha)}), (u)-[:PUBLICA]->(p)
    """
    db.run(q, uid=user_id, pid=post_id, titulo=titulo, fecha=fecha_iso)

def mention_user_in_post(db: neo4j_db.Neo4jDB, post_id: str, mentioned_user_id: str) -> None:
    q = """
    MATCH (p:Publicacion {id:$pid}), (m:User {id:$mid})
    CREATE (p)-[:MENCIONA]->(m)
    """
    db.run(q,pid=post_id, mid=mentioned_user_id)

def friends_and_family(db: neo4j_db.Neo4jDB, uid: str):
    q = """
    MATCH (u:User {id:$uid})-[:AMIGO|FAMILIAR]-(v:User)
    RETURN DISTINCT v.id AS id, v.nombre AS nombre
    ORDER BY id
    """
    return db.run(q, uid=uid)

def family_of_family(db: neo4j_db.Neo4jDB, uid: str):
    q ="""
    MATCH (u:User {id:$uid})-[:FAMILIAR]-(f:User)-[:FAMILIAR]-(ff:User)
    WHERE ff <> u
    RETURN DISTINCT ff.id AS id, ff.nombre AS nombre
    ORDER BY id
    """
    return db.run(q, uid=uid)

def messages_after_date(db: neo4j_db.Neo4jDB, from_id: str, to_id: str, fecha_iso: str):
    q = """
    MATCH (a:User {id:$from})-[:ENVIA]->(m:Mensaje)-[:A]->(b:User {id:$to})
    WHERE m.fecha > date($fecha)
    RETURN m.id AS id, m.conversacion AS conversacion, m.secuencia AS secuencia, m.fecha AS fecha, m.texto AS texto
    ORDER BY m.fecha, m.secuencia
    """
    return db.run(q, **{"from": from_id, "to": to_id, "fecha": fecha_iso})

def conversation_full(db: neo4j_db.Neo4jDB, u1: str, u2: str):
    q = """
    MATCH (a:User {id:$u1})-[:ENVIA]->(m:Mensaje)-[:A]->(b:User {id:$u2})
    RETURN m.conversacion AS conversacion, m.secuencia AS secuencia, m.fecha AS fecha, m.texto AS texto
    UNION
    MATCH (b:User {id:$u2})-[:ENVIA]->(m:Mensaje)-[:A]->(a:User {id:$u1})
    RETURN m.conversacion AS conversacion, m.secuencia AS secuencia, m.fecha AS fecha, m.texto AS texto
    ORDER BY fecha, secuencia
    """
    return db.run(q, u1=u1, u2=u2)

def mentions_with_work_relation(db: neo4j_db.Neo4jDB, uid: str):
    q = """
    MATCH (u:User {id:$uid})-[:PUBLICA]->(:Publicacion)-[:MENCIONA]->(m:User)
    MATCH (u)-[:LABORAL]->(e:Empresa)<-[:LABORAL]-(m)
    RETURN DISTINCT m.id AS id, m.nombre AS nombre, e.nombre AS empresa
    ORDER BY id
    """
    return db.run(q, uid=uid)


def new_connections_by_hops(db: neo4j_db.Neo4jDB, uid: str, max_hops: int):
    max_hops = int(max(1, max_hops))
    q = f"""
    MATCH (u:User {{id:$uid}})-[:AMIGO|FAMILIAR]-(s:User)
    MATCH p = (s)-[:AMIGO|FAMILIAR*1..{max_hops}]-(t:User)
    WHERE t <> u AND NOT (u)-[:AMIGO|FAMILIAR]-(t)
    RETURN DISTINCT s.id AS segundo_id, s.nombre AS segundo_nombre,
        t.id AS tercero_id, t.nombre AS tercero_nombre,
        min(length(p)) AS saltos
    ORDER BY saltos, segundo_id, tercero_id
    """
    return db.run(q, uid=uid)

def new_connections_by_messages(db, uid: str, min_msgs: int):
    q = """
    MATCH (u:User {id:$uid})-[:AMIGO|FAMILIAR]-(s:User)

    CALL (u, s) {
      MATCH (u)-[:ENVIA]->(:Mensaje)-[:A]->(s)
      RETURN count(*) AS a
      UNION ALL
      MATCH (s)-[:ENVIA]->(:Mensaje)-[:A]->(u)
      RETURN count(*) AS a
    }

    WITH u, s, sum(a) AS msgs_us
    WHERE msgs_us > $min_msgs

    MATCH (s)-[:AMIGO|FAMILIAR]-(t:User)
    WHERE t <> u AND NOT (u)-[:AMIGO|FAMILIAR]-(t)

    CALL (s, t) {
      MATCH (s)-[:ENVIA]->(:Mensaje)-[:A]->(t)
      RETURN count(*) AS b
      UNION ALL
      MATCH (t)-[:ENVIA]->(:Mensaje)-[:A]->(s)
      RETURN count(*) AS b
    }

    WITH s, t, msgs_us, sum(b) AS msgs_st
    WHERE msgs_st > $min_msgs

    RETURN
      s.id AS segundo_id, s.nombre AS segundo_nombre,
      t.id AS tercero_id, t.nombre AS tercero_nombre,
      msgs_us, msgs_st
    ORDER BY msgs_us DESC, msgs_st DESC, segundo_id, tercero_id
    """
    return db.run(q, uid=uid, min_msgs=min_msgs)