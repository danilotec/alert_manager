from typing import Set
from .entities import Fault
from .interfaces import AlertRepository, Sender
from .process import ProcessData

class AlertManager:

    def __init__(self, 
                 repository: AlertRepository, 
                
                 sender: Sender,
                 timeout_seconds: int = 120):
        
        self.repository = repository
        self.timeout_seconds = timeout_seconds
        self.active_alerts: Set[Fault] = set()
        
        self.sender = sender

    def trigger(self, fault: Fault) -> bool:
        """
        Dispara alerta se ainda não estiver ativo.
        Retorna True se for novo alerta.
        """
        if fault in self.active_alerts:
            return False

        self.active_alerts.add(fault)
        self.repository.save(fault)
        self.sender.send_fault(fault)
        return True

    def recover(self, fault: Fault) -> bool:
        """
        Remove alerta se voltou ao normal.
        """
        if fault not in self.active_alerts:
            return False

        self.active_alerts.remove(fault)
        self.repository.remove(fault)
        self.sender.send_fault(fault)
        return True

    def cleanup_expired(self) -> None:
        """
        Remove alertas que passaram do timeout.
        """
        expired = {f for f in self.active_alerts if f.is_expired(self.timeout_seconds)}
        for fault in expired:
            self.recover(fault)

    def is_active(self, fault: Fault) -> bool:
        return fault in self.active_alerts
    
    

class AlertService:

    def __init__(self, manager):
        self.manager = manager

    def process_usina(self, data):
        psa = data["Data"]

        faults = ProcessData.generate_fault_objects(
            name="Oxygen Plant",
            hospital=data["Hospital"],
            values=psa,
            rules=ProcessData.USINA_RULES + ProcessData.FLAG_RULES,
            safe_get=ProcessData._safe_get
        )

        self._handle_faults(faults, data.name, "Oxygen Plant")


    def process_hospital(self, data):
        hospital_data = data.data

        faults = ProcessData.generate_fault_objects(
            name="Hospital",
            hospital=data.name,
            values=hospital_data,
            rules=ProcessData.HOSPITAL_RULES + ProcessData.FLAG_RULES,
            safe_get=ProcessData._safe_get
        )

        self._handle_faults(faults, data.name, "Hospital")


    def _handle_faults(self, faults: list[Fault], hospital: str, source: str):

        active_now = set(faults)

        active_before = {
            f for f in self.manager.active_alerts
            if f.hospital == hospital and f.source == source
        }

        # Novos alertas
        for fault in active_now - active_before:
            self.manager.trigger(fault)

        # Recuperados
        for old_fault in active_before - active_now:
            self.manager.recover(old_fault)
