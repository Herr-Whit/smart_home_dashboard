import os.path
from abc import abstractmethod, ABC
from pathlib import Path

import pandas as pd
import seaborn as sns
from src.models.dashboard_input import DashboardInput
from src.models.tibber_models import TibberData
from datetime import datetime


class DashboardBuilder(ABC):
    @abstractmethod
    def build_dashboard(self, data: DashboardInput) -> None:
        pass


class SimpleDashboardBuilder(DashboardBuilder):

    def wrangle_tibber_data(self, data: dict) -> pd.DataFrame:
        next_two_days = data["today"] + data["tomorrow"]
        df = pd.DataFrame(next_two_days)
        df["startsAt"] = pd.to_datetime(df["startsAt"])
        df["hour"] = df["startsAt"].dt.hour
        df["day"] = df["startsAt"].dt.day
        df["Zeit"] = df["day"].astype(str) + ". " + df["hour"].astype(str)
        df["Preis in ct"] = df["total"] * 100
        return df

    def build_dashboard(self, data: dict) -> None:
        print("Building simple dashboard")
        print(data["tibber_data"])
        tibber_df = self.wrangle_tibber_data(data["tibber_data"])
        print(tibber_df)

        # Create a broad barplot
        # sns.set_theme(rc={'figure.figsize': (11.7, 8.27)})
        # sns.set_context("paper", font_scale=0.5)
        # We want to 'Zeit' as the x axis, but 'hour' as the label in jumps of 4 hours

        tibber_plot = sns.barplot(data=tibber_df, x="Zeit", y="Preis in ct")
        tibber_plot.set(xlabel="Time", ylabel="Price in ct")
        tibber_plot.set_xticklabels(
            [
                str(x) if i % 4 == 0 else ""
                for i, x in enumerate(list(tibber_df["hour"]))
            ],
            rotation=45,
            horizontalalignment="right",
        )
        tibber_plot.set_title(
            f'Kostenprognose am {datetime.now().strftime("%Y-%m-%d")}'
        )
        tibber_plot.set_ylim(15, 45)

        tibber_plot.axhline(
            tibber_df["tax"].mean() * 100, ls="--", color="r", label="Kostenlos"
        )
        tibber_plot.get_figure().show()

        # Save the plot as an image
        img_dir = os.path.join(os.getcwd(), "img")
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_tibber_plot.png"
        tibber_plot.get_figure().savefig(os.path.join(img_dir, img_name))
