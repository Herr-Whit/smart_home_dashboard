import os
import datetime

import dotenv
import pandas as pd
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

dotenv.load_dotenv(dotenv.find_dotenv())


class TibberClient:
    TIBBER_API_URL = "https://api.tibber.com/v1-beta/gql"
    TIBBER_API_TOKEN = os.environ["TIBBER_API_TOKEN"]

    def __init__(self):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(
            url=self.TIBBER_API_URL,
            headers={"Authorization": f"Bearer {self.TIBBER_API_TOKEN}"},
        )

        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    @staticmethod
    def wrangle_tibber_data(data: dict) -> pd.DataFrame:
        next_two_days = data["today"] + data["tomorrow"]
        df = pd.DataFrame(next_two_days)
        df["startsAt"] = pd.to_datetime(df["startsAt"])
        df["hour"] = df["startsAt"].dt.hour
        df["day"] = df["startsAt"].dt.day
        df["Zeit"] = df["day"].astype(str) + ". " + df["hour"].astype(str)
        df["Preis in ct"] = df["total"] * 100
        return df

    def get_price(self) -> pd.DataFrame:
        """
        First this function checks whether there is a record of price data available in the given path.
        If not, it will fetch it from the tibber API.
        :return:
        """
        if self.current_file_exists():
            data = self.fetch_from_file()
        else:
            data = self.fetch_from_api()
            if data.shape[0] != 48:
                data = self.fetch_from_api()
        return data

    def fetch_from_api(self):
        query = gql(
            """
            {
            viewer {
                homes {
                  currentSubscription{
                    priceInfo{
                      current{
                        total
                        energy
                        tax
                        startsAt
                      }
                      today {
                        total
                        energy
                        tax
                        startsAt
                      }
                      tomorrow {
                        total
                        energy
                        tax
                        startsAt
                      }
                    }
                  }
                }
              }
            }

        """
        )
        result = self.client.execute(query)
        data = result["viewer"]["homes"][0]["currentSubscription"]["priceInfo"]
        df = self.wrangle_tibber_data(data)
        if datetime.datetime.now().hour >= 13 and df.shape[0] == 48:
            if not os.path.exists("data"):
                os.makedirs("data")
            df.to_csv(self.get_current_file_path(), index=False)
        return df

    def current_file_exists(self):
        return os.path.exists("data") and os.path.isfile(self.get_current_file_path())

    @staticmethod
    def get_current_file_path(date=None):
        if date is None:
            now = datetime.datetime.now()
            if now.hour < 13:
                date = now - datetime.timedelta(days=1)
            else:
                date = now
        return f"data/{date.strftime('%Y-%m-%d')}.csv"

    def fetch_from_file(self):
        df = pd.read_csv(self.get_current_file_path())
        return df
