from typing import Protocol
from entities import Fault

class AlertRepository(Protocol):
    def save(self, fault: Fault) -> None: ...
    def remove(self, fault: Fault) -> None: ...

class handle(Protocol):
    @classmethod
    def process_alert(cls, fault: Fault)-> tuple[str, str]: ...

# REPOSITÓRIO EM MEMÓRIA (TESTE)
class InMemoryAlertRepository:
    def __init__(self, handles: handle):
        self.storage: list[Fault] = []
        self.handles = handles

    def save(self, fault: Fault) -> None:
        print(self.handles.process_alert(fault))
        self.storage.append(fault)

    def remove(self, fault: Fault) -> None:
        print(fault)
        self.storage = [f for f in self.storage if f != fault]
