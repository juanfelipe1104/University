from dataclasses import dataclass, field

@dataclass
class RelationData:
    rel_id: str
    from_user_id: str
    to_user_id: str
    msg_count: int = 0
    props: dict = field(default_factory=dict)

def make_rel_id(sender_id: str, receiver_id: str) -> str:
    """
    Genera rel_id a partir de sender_id y receiver_id.
    """

    return f"{sender_id}-{receiver_id}"
