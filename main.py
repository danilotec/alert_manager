from entities import Hospital
from repository import InMemoryAlertRepository
from alert import AlertManager, AlertService
from process import Handles, Telegram
teste =[
    {
    "Hospital":"Joao Machado - Natal/RN",
    "Data":{
        "C1":"Stand-by",
        "C2":None,
        "BE":"Ligado",
        "RST":"Ligado",
        "auto":None,
        "rede":None,
        "pressure":6,
        "dew_point":None,
        "vacuo":None,
        }
    },
    {
    "Hospital":"Hospital das Clinicas",
    "Data":{
        "C1":"Stand-by",
        "C2":"Stand-by",
        "BE":None,
        "RST":None,
        "auto":None,
        "rede":None,
        "pressure":4.3,
        "dew_point":"-76.5",
        "vacuo":"-530"
        }
    }
    
    ]

tel = Telegram()
han = Handles()
repo = InMemoryAlertRepository(han, tel)
manager = AlertManager(repo)
service = AlertService(manager)


for item in teste:

    hos = Hospital(item)
    data = hos.central
    service.process_hospital(data)
    manager.cleanup_expired()
    
        

