from pydantic import BaseModel

from src.models.tibber_models import TibberData


class DashboardInput(BaseModel):
    tibber_data: TibberData
