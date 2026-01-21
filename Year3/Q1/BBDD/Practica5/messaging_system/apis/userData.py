from dataclasses import dataclass, field

@dataclass
class UserData:
    user_id: str
    name: str | None = None
    props: dict = field(default_factory=dict)
