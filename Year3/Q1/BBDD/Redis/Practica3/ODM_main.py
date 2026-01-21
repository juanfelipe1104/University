import ODM as ODM
import redis
# Redis para cache (db=0)
redis_sh = redis.from_url(
    "redis://localhost:6379/0",
    decode_responses=True
)

def show_cache_person(pid: str):
    key = f"Persona:{pid}"
    cache = redis_sh.get(key)

    if cache is None:
        print(f"[CACHE] No existe la clave {key}")
        return
    print(f"[CACHE] {key} --> {cache}")


# Inicializa con Redis
ODM.initApp(db_name="Practica3")

# Borrar datos previos
ODM.Persona._db.delete_many({})
ODM.Empresa._db.delete_many({})
ODM.Centro_Educativo._db.delete_many({})

# Insertar datos de prueba 
p1 = ODM.Persona(nombre="Pablo",  dni="DNI-P1", edad=30)
p2 = ODM.Persona(nombre="Lucía",  dni="DNI-P2", edad=25)
p3 = ODM.Persona(nombre="Carlos", dni="DNI-P3", edad=40)

p1.save()
p2.save()
p3.save()

e1 = ODM.Empresa(nombre="Empresa Uno",   nif="NIF-E1")
e2 = ODM.Empresa(nombre="Empresa Dos",   nif="NIF-E2")
e3 = ODM.Empresa(nombre="Empresa Tres",  nif="NIF-E3")

e1.save()
e2.save()
e3.save()

c1 = ODM.Centro_Educativo(nombre="Colegio San Juan",    codigo="CE-1")
c2 = ODM.Centro_Educativo(nombre="Instituto Central",   codigo="CE-2")
c3 = ODM.Centro_Educativo(nombre="Centro Formación X",  codigo="CE-3")

c1.save()
c2.save()
c3.save()

pid = str(p1._data["_id"])
print(f"_id de p1: {pid}")

print()

print("Primer find_by_id (MISS --> lee de Mongo y guarda en Redis)")
show_cache_person(pid)
obj1 = ODM.Persona.find_by_id(pid)
print("Resultado:", obj1.nombre, obj1.dni, obj1.edad)
show_cache_person(pid)

print()

print("Actualizar el nombre de p1 (actualiza Mongo y borra de la caché)")
p1.nombre = "Pablo Cacheado"
p1.save()
show_cache_person(pid)
print("find_by_id de nuevo (debe mostrar el nombre actualizado)")
obj2 = ODM.Persona.find_by_id(pid)
print("Resultado:", obj2.nombre, obj2.dni, obj2.edad)
show_cache_person(pid)

print()

print("Borrar la persona y luego find_by_id (debe devolver None)")
p1.delete()
show_cache_person(pid)
obj4 = ODM.Persona.find_by_id(pid)
print("Resultado:", obj4)
