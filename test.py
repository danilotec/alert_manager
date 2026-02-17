teste = [
    {
    "Hospital":"Joao Machado - Natal/RN",
    "Data":{
        "C1":"Stand-by",
        "C2":None,
        "BE":"Ligado",
        "RST":"Ligado",
        "auto":None,
        "rede":2,
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


if __name__ == '__main__':
    from pipeline import AlertPipeline

    pipe = AlertPipeline()

    for item in teste:
        pipe.check_hospital(item)
        print(pipe.repo.storage)