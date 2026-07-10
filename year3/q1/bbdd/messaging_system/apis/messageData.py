from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid


@dataclass
class MessageData:
    """
    Estructura de un mensaje del sistema.

    - msg_id: identificador único (UUID por defecto)
    - timestamp: timestamp UTC del mensaje
    - sender_id / receiver_id: usuarios implicados
    - rel_id: relación (sender-receiver)
    - content: contenido del mensaje
    - metadata: metadatos opcionales
    """

    sender_id: str
    receiver_id: str
    content: str

    rel_id: str
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """
        Convierte clase a dict.
        """
        d = asdict(self)
        return d

    def to_redis_dict(self) -> dict:
        """
        Redis guarda timestamp como ISO string.
        """
        d = self.to_dict()
        d["timestamp"] = self.timestamp.isoformat()
        return d

    @staticmethod
    def from_dict(d: dict) -> "MessageData":
        """
        Reconstruye MessageData desde dict.
        Acepta 'timestamp' como datetime (Mongo) o como ISO string (Redis).
        """
        timestamp = d.get("timestamp", None)
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        metadata = d.get("metadata", {})
        if metadata is None:
            metadata = {}

        return MessageData(
            sender_id=d.get("sender_id"),
            receiver_id=d.get("receiver_id"),
            content=d.get("content"),
            rel_id=d.get("rel_id"),
            msg_id=d.get("msg_id", str(uuid.uuid4())),
            timestamp=timestamp,
            metadata=metadata
        )
