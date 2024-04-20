"""
A fastapi server that serves dashboard as an image
"""
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.server.dashboard_builder import SimpleDashboardBuilder
from src.server.tibber_client import TibberClient

app = FastAPI()
tibber_client = TibberClient()
builder = SimpleDashboardBuilder()

@app.get("/dashboard/")
def create_dashboard():
    tibber_data = tibber_client.get_price()
    data = {'tibber_data': tibber_data}
    file = builder.build_dashboard(data)
    return FileResponse(file, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app)