import os

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

    def get_price(self):
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


