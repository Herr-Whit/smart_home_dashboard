from pydantic import BaseModel

from src.server.models.tibber_models import TibberData


class DashboardInput(BaseModel):
    tibber_data: TibberData
