import redis

# Redis para sesiones + helpdesk (db=1)
redis_sh = redis.from_url(
    "redis://localhost:6379/1",
    decode_responses=True
)

HELPDESK_QUEUE_KEY = "helpdesk:queue"

def request_help(username: str, priority: int) -> None:
    """
    Registra una petición de ayuda de un usuario con una prioridad.
    score = priority, valor = username
    """
    redis_sh.zadd(HELPDESK_QUEUE_KEY, {username: priority})

def attend_next_help(block: bool = True, timeout: int = 0) -> str | None:
    """
    Atiende la petición de mayor prioridad.
    - Si block=True y timeout=0, entonces se queda esperando hasta que haya algo (BZPOPMAX).
    - Si block=True y timeout>0, entonces espera como máximo 'timeout' segundos.
    - Si block=False, entonces intenta ZPOPMAX (no bloqueante) y devuelve None si no hay nada.

    Devuelve el user_id o None
    """
    if block:
        # BZPOPMAX devuelve (key, member, score) o None si timeout
        res = redis_sh.bzpopmax(HELPDESK_QUEUE_KEY, timeout=timeout)
        if res is None:
            return None
        _, user_id, _ = res
        return user_id

    # Modo no bloqueante: ZPOPMAX devuelve lista [(member, score)] o vacía
    res = redis_sh.zpopmax(HELPDESK_QUEUE_KEY)
    if not res:
        return None
    user_id, _ = res[0] # Devolvemos el primero
    return user_id