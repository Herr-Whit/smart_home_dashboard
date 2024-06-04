"""
A fastapi server that serves dashboard as an image
"""

import argparse
import os
from datetime import datetime, timedelta

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.server.dashboard_builder import SimpleDashboardBuilder
from src.server.tibber import TibberClient, calculate_update_time

app = FastAPI()
tibber_client = TibberClient()
builder = SimpleDashboardBuilder()


@app.get("/dashboard/")
def create_dashboard():
    tibber_data = tibber_client.get_price()
    data = {"tibber_data": tibber_data}
    file = builder.build_dashboard(data)
    return FileResponse(file, media_type="image/png")


@app.get("/timing/")
def get_timing_info():
    """
    returns the time and duration in ms, when the dashboard is going to be available. Tibber usually publishes the
    prices for the next day at 13:00.
    :return: object with target time and sleep duration in seconds
    """
    if sleep_time:
        update_time = {
            "target_time": datetime.now() + timedelta(seconds=sleep_time),
            "time_to_sleep": sleep_time,
        }
    else:
        update_time = calculate_update_time(13, 15)
    print(f"{update_time=}")
    return update_time


if __name__ == "__main__":
    # retrieve kwarg sleep time from command line if applicable
    sleep_time = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep_time", type=int)
    args = parser.parse_args()
    if args.sleep_time:
        sleep_time = args.sleep_time
    uvicorn.run(app, host="0.0.0.0", port=8000)
