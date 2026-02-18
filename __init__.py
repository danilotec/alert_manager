from .pipeline import AlertPipeline

__ALL__ = [
    'AlertPipeline'
]

""" example:
from alert_manager import AlertPipeline
pipe = AlertPipeline()


pipe.check_hospital(payload)
print(pipe.repo.storage)
"""