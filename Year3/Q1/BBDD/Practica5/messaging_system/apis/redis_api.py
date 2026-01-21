import json
from redis import Redis
from redis.exceptions import ResponseError

from apis.messageData import MessageData

class RedisAPI:
    """
    Redis como sistema de colas (LIST) por relación Neo4j.

    Key pattern:
        queue:{rel_id} -> Redis LIST

    - enqueue: RPUSH
    - blocking consume: BLPOP timeout=5 (borra el mensaje al consumir)
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Inicializa conexión Redis.
        """

        self._r = Redis(host=host, port=port, db=db, decode_responses=True)

    @staticmethod
    def queue_key(rel_id: str) -> str:
        """
        Key de la cola para una relación.
        """

        return f"queue:{rel_id}"

    def delete_queue(self, rel_id: str) -> int:
        """
        Borra la cola. Devuelve número de keys borradas (0 o 1).
        """

        return int(self._r.delete(self.queue_key(rel_id)))

    def queue_length(self, rel_id: str) -> int:
        """
        Devuelve longitud de la cola.
        """

        return int(self._r.llen(self.queue_key(rel_id)))

    def list_queues(self, pattern: str = "queue:*") -> list[str]:
        """
        Lista keys de colas.
        """

        return [k for k in self._r.scan_iter(match=pattern)]
    
    def enqueue_message(self, rel_id: str, message: dict) -> int:
        """
        Encola un mensaje (JSON) al final.
        Devuelve longitud de la cola tras insertar.
        """

        key = self.queue_key(rel_id)
        message_parsed = json.dumps(message)
        return int(self._r.rpush(key, message_parsed))

    def peek_messages(self, rel_id: str, start: int = 0, end: int = -1) -> list[dict]:
        """
        Lee mensajes sin consumir.
        """

        key = self.queue_key(rel_id)
        items = self._r.lrange(key, start, end)
        out: list[dict] = []
        for s in items:
            try:
                out.append(json.loads(s))
            except json.JSONDecodeError:
                # Si no se puede parsear, lo devolvemos como raw
                out.append({"raw": s})
        return out

    def update_message_at(self, rel_id: str, index: int, new_message: dict) -> bool:
        """
        Actualiza dentro de una cola: Redis LIST permite LSET por índice.
        Devuelve True si ok; si index inválido, ResponseError y devuelve False.
        """

        key = self.queue_key(rel_id)
        message_parsed = json.dumps(new_message)
        try:
            self._r.lset(key, index, message_parsed)
            return True
        except ResponseError:
            return False

    def delete_message_at(self, rel_id: str, index: int) -> bool:
        """
        Borrar por índice en lista no es directo:
            - LSET index a un marcador único
            - LREM 1 marcador
        """
        
        key = self.queue_key(rel_id)
        marker = "DELETED"
        try:
            self._r.lset(key, index, marker)
            removed = self._r.lrem(key, 1, marker)
            return int(removed) == 1
        except ResponseError:
            return False

    def consume_blocking(self, rel_id: str, timeout: int = 5) -> MessageData | None:
        """
        BLPOP con timeout=5s.
        Devuelve el mensaje (MessageData) o None si timeout, quitandolo de la cola.
        """

        key = self.queue_key(rel_id)
        result: tuple[str, str] | None = self._r.blpop(key, timeout=timeout)  # (key, value) o None
        if result is None:
            return None
        _, value = result
        try:
            message = json.loads(value)
            return MessageData.from_dict(message)
        except Exception as e:
            raise ValueError(f"Mensaje inválido en Redis ({rel_id}): {e}")

    def export_queues_state(self) -> list[dict]:
        """
        Exporta estado de todas las colas:
          [{ "key": "...", "rel_id": "...", "items": [<dict>, ...] }, ...]
        """

        queues = self.list_queues()
        out: list[dict] = []
        for key in queues:
            rel_id = key.split("queue:", 1)[1] if key.startswith("queue:") else key
            out.append({
                "key": key,
                "rel_id": rel_id,
                "items": self.peek_messages(rel_id)
            })
        return out

    def clear_all_queues(self) -> int:
        """
        Borra todas las colas queue:*.
        Devuelve cuántas keys borró.
        """

        keys = self.list_queues()
        if not keys:
            return 0
        return int(self._r.delete(*keys))

    def import_queues_state(self, queues_state: list[dict]) -> None:
        """
        Reconstruye colas desde snapshot. Se asume que antes se han borrado.
        Mantiene orden original insertando con RPUSH en el mismo orden.
        """

        for q in queues_state:
            rel_id = q.get("rel_id")
            items = q.get("items", [])
            for msg in items:
                self.enqueue_message(rel_id, msg)
