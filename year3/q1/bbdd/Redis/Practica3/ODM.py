__author__ = 'Juan Felipe Rodríguez, Alejandro Castellanos'
__students__ = 'Juan Felipe Rodríguez, Alejandro Castellanos'


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
import pymongo
from bson.objectid import ObjectId
import yaml
import redis
from bson import json_util

def getLocationPoint(address: str) -> Point:
    """ 
    Obtiene las coordenadas de una dirección en formato geojson.Point
    Utilizar la API de geopy para obtener las coordenadas de la direccion
    Cuidado, la API es publica tiene limite de peticiones, utilizar sleeps.

    Parameters
    ----------
        address : str
            direccion completa de la que obtener las coordenadas
    Returns
    -------
        geojson.Point
            coordenadas del punto de la direccion
    """
    location = None
    attempt = 0
    max_attempts = 3
    while attempt < max_attempts:
        try:
            time.sleep(1)
            location = Nominatim(user_agent="Mi-Nombre-Aleatorio").geocode(address)
            if location:
                return Point((location.longitude, location.latitude))
        except GeocoderTimedOut:
            # Puede lanzar una excepcion si se supera el tiempo de espera
            # Volver a intentarlo
            pass
        attempt += 1
          
    raise ValueError("No se pudieron obtener coordenadas")

class Model:
    """ 
    Clase de modelo abstracta
    Crear tantas clases que hereden de esta clase como  
    colecciones/modelos se deseen tener en la base de datos.

    Attributes
    ----------
        required_vars : set[str]
            conjunto de atributos requeridos por el modelo
        admissible_vars : set[str]
            conjunto de atributos admitidos por el modelo
        db : pymongo.collection.Collection
            conexion a la coleccion de la base de datos
    
    Methods
    -------
        __setattr__(name: str, value: str | dict) -> None
            Sobreescribe el metodo de asignacion de valores a los 
            atributos del objeto con el fin de controlar qué atributos 
            son modificados y cuando son modificados.
        __getattr__(name: str) -> Any
            Sobreescribe el metodo de acceso a atributos del objeto 
        save()  -> None
            Guarda el modelo en la base de datos
        delete() -> None
            Elimina el modelo de la base de datos
        find(filter: dict[str, str | dict]) -> ModelCursor
            Realiza una consulta de lectura en la BBDD.
            Devuelve un cursor de modelos ModelCursor
        aggregate(pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor
            Devuelve el resultado de una consulta aggregate.
        find_by_id(id: str) -> dict | None
            Busca un documento por su id utilizando la cache y lo devuelve.
            Si no se encuentra el documento, devuelve None.
        init_class(db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None
            Inicializa las variables de clase en la inicializacion del sistema.

    """
    _required_vars: set[str]
    _admissible_vars: set[str]
    _location_var: None
    _db: pymongo.collection.Collection
    _cache: redis.Redis
    _cache_ttl_secs: int = 86400  # 24 h

    def __init__(self, **kwargs: dict[str, str | int | dict]):
        super().__setattr__('_data', {})
        super().__setattr__('_modified_vars', set())
        super().__setattr__('_unset_vars', set())
        """
        Inicializa el modelo con los valores proporcionados en kwargs
        Comprueba que los valores proporcionados en kwargs son admitidos
        por el modelo y que los atributos requeridos son proporcionados.

        Parameters
        ----------
            kwargs : dict[str, str | dict]
                diccionario con los valores de las atributos del modelo
        """
        # Comprobar que se proporcionan todos los atributos requeridos
        missing_required_vars = set(self._required_vars) - set(kwargs.keys())
        if missing_required_vars:
            raise AttributeError(f"Faltan atributos: {missing_required_vars}")
        # Asigna todos los valores en kwargs a las atributos con nombre de las claves en kwargs.
        # Comprueba que sean correctos
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, name: str, value: str | int | dict) -> None:
        """
        Sobreescribe el metodo de asignacion de valores a los 
        atributos del objeto con el fin de controlar que atributos 
        son modificados y cuando son modificados.
        """
        # Comprobar que el atributo es admitido por el modelo
        allowed = {'_id'} | self._required_vars | self._admissible_vars
        if self._location_var:
            allowed.add(f"{self._location_var}_loc")
        if name not in allowed:
            raise AttributeError(f"Atributo no existente o no admitido: {name}")
        
        # Si la variable es de tipo localizacion, obtener las coordenadas geojson
        if self._location_var and name == self._location_var and isinstance(value, str):
            try:
                valueGeo = getLocationPoint(value)
            except Exception as e:
                raise ValueError(f"No se han podido obtener las coordenadas de la direccion {value}: {e}")
            # Guardar las coordenadas en la variable con sufijo _loc
            nameGeo = f"{name}_loc"
            self._data[nameGeo] = valueGeo
            self._modified_vars.add(nameGeo)

        # Asigna el valor value a la variable name
        self._data[name] = value
        if isinstance(value, str) and value == "":
            self._unset_vars.add(name)
            self._modified_vars.discard(name)
            self._data.pop(name, None)
            if self._location_var and name == self._location_var:
                self._unset_vars.add(f"{name}_loc")
        else:
            self._modified_vars.add(name)
            self._unset_vars.discard(name)

    def __getattr__(self, name: str) -> Any:
        """
        Sobreescribe el metodo de acceso a atributos del objeto
        __getattr__ solo es llamado cuando no encuentra el atributo
        en el objeto 
        """
        if name in {'_required_vars', '_admissible_vars', '_db', '_data', '_location_var', '_modiefied_vars', '_unset_vars'}:
            return super().__getattribute__(name)
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError
        
    def save(self) -> None:
        """
        Guarda el modelo en la base de datos
        Si el modelo no existe en la base de datos, se crea un nuevo
        documento con los valores del modelo. En caso contrario, se
        actualiza el documento existente con los nuevos valores del
        modelo.
        """
        _id = self._data.get('_id')

        # Insertar documento
        if _id is None:
            result = self._db.insert_one(self._data)
            self._data['_id'] = result.inserted_id
        # Actualizar documento
        else:
            update = {}
            if self._modified_vars:
                update['$set'] = {k: self._data[k] for k in self._modified_vars}
            if self._unset_vars:
                update['$unset'] = {k: "" for k in self._unset_vars}
            if update:
                self._db.update_one({'_id': _id}, update)
        # Limpiar modified y unset
        self._modified_vars.clear()
        self._unset_vars.clear()
        # Actualizar cache
        if self._cache and _id:
            try:
                key = self._cache_key(str(self._data['_id']))
                self._cache.delete(key)
            except Exception:
                pass


    def delete(self) -> None:
        """
        Elimina el modelo de la base de datos
        """
        if '_id' not in self._data or self._data['_id'] is None:
            raise ValueError("El modelo no existe en la BD (no tiene _id).")
        self._db.delete_one({'_id': self._data['_id']})
        # Eliminar de cache
        if self._cache is not None:
            try:
                key = self._cache_key(str(self._data['_id']))
                self._cache.delete(key)
            except Exception:
                pass
    
    @classmethod
    def _cache_key(cls, id_str: str) -> str:
        # Combinación de nombre de colección e ID (Coleccion:ID)
        collection = cls._db.name
        return f"{collection}:{id_str}"

    @classmethod
    def find(cls, filter: dict[str, str | dict]) -> Any:
        """ 
        Utiliza el metodo find de pymongo para realizar una consulta
        de lectura en la BBDD.
        find debe devolver un cursor de modelos ModelCursor

        Parameters
        ----------
            filter : dict[str, str | dict]
                diccionario con el criterio de busqueda de la consulta
        Returns
        -------
            ModelCursor
                cursor de modelos
        """ 
        cursor = cls._db.find(filter)
        return ModelCursor(cls, cursor)

    @classmethod
    def aggregate(cls, pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor:
        """ 
        Devuelve el resultado de una consulta aggregate. 
        No hay nada que hacer en esta funcion.
        Se utilizara para las consultas solicitadas
        en el segundo proyecto de la practica.

        Parameters
        ----------
            pipeline : list[dict]
                lista de etapas de la consulta aggregate 
        Returns
        -------
            pymongo.command_cursor.CommandCursor
                cursor de pymongo con el resultado de la consulta
        """ 
        return cls._db.aggregate(pipeline)
    
    @classmethod
    def find_by_id(cls, id: str) -> Self | None:
        """ 
        NO IMPLEMENTAR HASTA EL TERCER PROYECTO
        Busca un documento por su id utilizando la cache y lo devuelve.
        Si no se encuentra el documento, devuelve None.

        Parameters
        ----------
            id : str
                id del documento a buscar
        Returns
        -------
            Self | None
                Modelo del documento encontrado o None si no se encuentra
        """
        # Revisar en cache
        if cls._cache is not None:
            key = cls._cache_key(id)
            data = cls._cache.get(key)
            if data is not None:
                doc = json_util.loads(data)
                try:
                    cls._cache.expire(key, cls._cache_ttl_secs)
                except Exception:
                    print(f"[CACHE] Error actualizando TTL de la clave {key}")
                    pass
                return cls(**doc)
        # Usamos ObjectId porque está guardado así en mongo
        doc = cls._db.find_one({"_id": ObjectId(id)})
        if doc is None:
            return None
        if cls._cache is not None:
            try:
                key = cls._cache_key(str(doc["_id"]))
                cls._cache.setex(key, cls._cache_ttl_secs, json_util.dumps(doc))
            except Exception as e:
                print(f"[CACHE] Error guardando en caché: {e}")
                pass
        return cls(**doc)


    @classmethod
    def init_class(cls, db_collection: pymongo.collection.Collection, indexes:dict[str,str], required_vars: set[str], admissible_vars: set[str], cache: redis.Redis) -> None:
        """ 
        Inicializa los atributos de clase en la inicializacion del sistema.
        Aqui se deben inicializar o asegurar los indices. Tambien se puede
        alguna otra inicialización/comprobaciones o cambios adicionales
        que estime el alumno.

        Parameters
        ----------
            db_collection : pymongo.collection.Collection
                Conexion a la collecion de la base de datos.
            indexes: Dict[str,str]
                Set de indices y tipo de indices para la coleccion
            required_vars : set[str]
                Set de atributos requeridos por el modelo
            admissible_vars : set[str] 
                Set de atributos admitidos por el modelo
        """
        cls._db = db_collection
        cls._required_vars = required_vars
        cls._admissible_vars = admissible_vars
        cls._location_var = None
        cls._cache = cache

        if indexes:
            # Índices únicos
            for field in indexes.get('unique', []):
                cls._db.create_index([(field, pymongo.ASCENDING)], unique=True)

            # Índices regulares
            text_fields = indexes.get('regular', [])
            if text_fields:
                keys = [(field, pymongo.TEXT) for field in text_fields]
                cls._db.create_index(keys, default_language="spanish")

            # Índice geoespacial (2dsphere)
            loc = indexes.get('location')
            if loc:
                cls._location_var = loc
                loc = f"{loc}_loc"
                cls._db.create_index([(loc, pymongo.GEOSPHERE)])
                


class ModelCursor:
    """ 
    Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.

    Attributes
    ----------
        model_class : Model
            Clase para crear los modelos de los documentos que se iteran.
        cursor : pymongo.cursor.Cursor
            Cursor de pymongo a iterar

    Methods
    -------
        __iter__() -> Generator
            Devuelve un iterador que recorre los elementos del cursor
            y devuelve los documentos en forma de objetos modelo.
    """

    def __init__(self, model_class: Model, cursor: pymongo.cursor.Cursor):
        """
        Inicializa el cursor con la clase de modelo y el cursor de pymongo

        Parameters
        ----------
            model_class : Model
                Clase para crear los modelos de los documentos que se iteran.
            cursor: pymongo.cursor.Cursor
                Cursor de pymongo a iterar
        """
        self.model = model_class
        self.cursor = cursor
    
    def __iter__(self) -> Generator:
        """
        Devuelve un iterador que recorre los elementos del cursor
        y devuelve los documentos en forma de objetos modelo.
        Utilizar yield para generar el iterador
        Utilizar la funcion next para obtener el siguiente documento del cursor
        Utilizar alive para comprobar si existen mas documentos.
        """
        while self.cursor.alive:
            try:
                doc = next(self.cursor)
                yield self.model(**doc)
            except StopIteration:
                break


def initApp(definitions_path: str = "./models.yml", mongodb_uri="mongodb://localhost:27017/", db_name="abc", cache_redis_url: str = "redis://localhost:6379/0", scope=globals()) -> None:
    """ 
    Declara las clases que heredan de Model para cada uno de los 
    modelos de las colecciones definidas en definitions_path.
    Inicializa las clases de los modelos proporcionando los indices y 
    atributos admitidos y requeridos para cada una de ellas y la conexión a la
    collecion de la base de datos.
    
    Parameters
    ----------
        definitions_path : str
            ruta al fichero de definiciones de modelos
        mongodb_uri : str
            uri de conexion a la base de datos
        db_name : str
            nombre de la base de datos
    """
    # Conectar a base de datos
    client = pymongo.MongoClient(mongodb_uri)
    db = client[db_name]

    # Conectar a Redis
    cache = redis.from_url(cache_redis_url, decode_responses=True)
    try:
        cache.config_set("maxmemory", "150mb")
        cache.config_set("maxmemory-policy", "volatile-ttl")  # Elimina los registros con menor ttl
    except Exception:
        # Si no hay permisos para CONFIG SET, seguimos
        pass


    # Leer definiciones de modelos
    with open(definitions_path, 'r') as f:
        definitions = yaml.safe_load(f)
    
    for collection_name, configuration in definitions.items():
        required = set(configuration.get('required_vars', []))
        admissible = set(configuration.get('admissible_vars', []))
        unique_idx = list(configuration.get('unique_indexes', []))
        regular_idx = list(configuration.get('regular_indexes', []))
        location_idx = configuration.get('location_index', None)
        # Crear clase
        model_cls = type(collection_name, (Model,), {})
        scope[collection_name] = model_cls  # expone la clase en el scope

        # Inicializar clase con su colección e índices
        indexes = {
            'unique': unique_idx,
            'regular': regular_idx,
            'location': location_idx
        }
        model_cls.init_class(
            db_collection=db[collection_name],
            indexes=indexes,
            required_vars=required,
            admissible_vars=admissible,
            cache=cache
        )