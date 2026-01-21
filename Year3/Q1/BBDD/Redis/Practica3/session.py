import redis
import uuid
import random

# Redis para sesiones + helpdesk (db=1)
redis_sh = redis.from_url(
    "redis://localhost:6379/1",
    decode_responses=True
)

SESSION_TTL = 30 * 24 * 3600  # 1 mes

def _user_key(username: str) -> str:
    return f"user:{username}"

def _session_key(token: str) -> str:
    return f"session:{token}"


def create_user(full_name: str, username: str, password: str,
                privileges: int | None = None) -> None:
    # Crea un usuario nuevo. Lanza ValueError si ya existe
    key = _user_key(username)
    if redis_sh.exists(key):
        raise ValueError("El usuario ya existe")

    if privileges is None:
        privileges = random.randint(1, 10_000)

    redis_sh.hset(key, mapping={
        "full_name": full_name,
        "username": username,
        "password": password,
        "privileges": str(privileges),
        "token": ""      # sin sesión activa (No hay token)
    })


def get_user(username: str) -> dict | None:
    # Devuelve los datos del usuario (dict) o None si no existe.
    key = _user_key(username)
    data = redis_sh.hgetall(key)
    if not data:
        return None
    # cast privileges a int (porque todo esta en strings dentro de redis)
    data["privileges"] = int(data.get("privileges"))
    return data


def update_user(username: str, **fields) -> None:
    # Actualiza campos del usuario (full_name, password, privileges).
    key = _user_key(username)
    if redis_sh.exists(key):
        data = {}
        if "full_name" in fields:
            data["full_name"] = fields["full_name"]
        if "password" in fields:
            data["password"] = fields["password"]
        if "privileges" in fields:
            data["privileges"] = str(fields["privileges"])

        if data:
            redis_sh.hset(key, mapping=data)


def delete_user(username: str) -> None:
    # Elimina un usuario y su sesión si existe.
    key = _user_key(username)
    if redis_sh.exists(key):
        # Si tiene token de sesión, borrar también la clave de sesión
        token = redis_sh.hget(key, "token")
        if token:
            redis_sh.delete(_session_key(token))
        redis_sh.delete(key)

def login_user_password(username: str, password: str) -> tuple[int, str | None]:
    """
    Login con usuario y contraseña.
    Devuelve (privileges, token) si OK, o (-1, None) si usuario o contraseña incorrectos.
    """
    key = _user_key(username)
    data = redis_sh.hgetall(key)
    if not data:
        return -1, None

    if data.get("password") != password:
        return -1, None

    # Generar nuevo token
    token = uuid.uuid4().hex

    # Guardar sesión con TTL = 1 mes
    redis_sh.setex(_session_key(token), SESSION_TTL, username)

    # Guardar token en el hash de usuario
    redis_sh.hset(key, "token", token)

    privileges = int(data.get("privileges"))
    return privileges, token

def login_token(token: str) -> int:
    """
    Login mediante token de sesión.
    Devuelve privileges si el token es válido, o -1 si no.
    """
    username = redis_sh.get(_session_key(token))
    if username is None:
        return -1  # No existe token
    data = redis_sh.hgetall(_user_key(username))
    return int(data.get("privileges"))