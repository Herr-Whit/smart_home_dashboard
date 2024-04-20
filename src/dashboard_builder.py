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
        next_two_days = data['today'] + data['tomorrow']
        return pd.DataFrame(next_two_days)

    def build_dashboard(self, data: dict) -> None:
        print("Building simple dashboard")
        print(data['tibber_data'])
        tibber_df = self.wrangle_tibber_data(data['tibber_data'])
        print(tibber_df)
        tibber_plot = sns.lineplot(data=tibber_df, x='startsAt', y='total')
        img_dir = os.path.join(os.getcwd(), 'img')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_tibber_plot.png"
        tibber_plot.get_figure().savefig(os.path.join(img_dir, img_name))