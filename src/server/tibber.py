import os
import datetime
import time


import dotenv
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

    def get_price(self) -> dict:
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
        return data


def calculate_update_time(target_hour, target_minute, target_second=0):
    """
    calculates the time to sleep and target datetime until the specified time of day
    :param target_hour:
    :param target_minute:
    :param target_second:
    :return:
    """
    now = datetime.datetime.now()
    target_time_today = now.replace(hour=target_hour, minute=target_minute, second=target_second, microsecond=0)

    if target_time_today < now:
        # Target time has already passed today, so set it for tomorrow
        target_time = target_time_today + datetime.timedelta(days=1)
    else:
        # Target time has not yet passed today, so set it for today
        target_time = target_time_today

    time_to_sleep = (target_time - now).total_seconds()
    return {"target_time": target_time, "time_to_sleep": time_to_sleep}
