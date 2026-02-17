from protocols import handle, Sender, Fault, get_chat_id

# REPOSITÓRIO EM MEMÓRIA (TESTE)
class InMemoryAlertRepository:
    def __init__(self, handles: handle, sender: Sender):
        self.storage: list[Fault] = []
        self.handles = handles
        self.sender = sender

    def save(self, fault: Fault) -> None:
        body = self.handles.process_alert(fault)

        try: 
            chat_id = get_chat_id(fault.hospital)
            self.sender.send_message(chat_id, body)
        except:
            self.sender.send_message(1538185358, body)
        
        self.storage.append(fault)

    def remove(self, fault: Fault) -> None:
        print(fault)
        self.storage = [f for f in self.storage if f != fault]
