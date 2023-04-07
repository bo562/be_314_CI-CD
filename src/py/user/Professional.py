"""
py class for professional data structure
"""
from dataclasses import dataclass
from service.Service import Service
from user.Billing import Billing


@dataclass
class Professional:
    professional_id: int
    subscription_id: int = None
    services: [Service] = None
    CCin: Billing = None
    user_id: int = None

    @staticmethod
    def ToAPI(obj):
        if isinstance(obj, Professional):
            remap = {
                "services": obj.services,
                "CCin": obj.CCin
            }
            return remap

        raise TypeError

    @staticmethod
    def FromAPI(obj):
        return Professional(professional_id=-1, subscription_id=-1, services=obj.get('services'), CCin=obj.get('CCin'),
                            user_id=-1)
