from dataclasses import dataclass
from typing import Optional

@dataclass
class StatusConsulta:
    descricao: str

    id: Optional[int] = None

    def __str__(self):
        return f"StatusConsulta(id={self.id}, descricao={self.descricao})"