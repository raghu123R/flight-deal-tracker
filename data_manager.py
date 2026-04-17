import requests
from dotenv import load_dotenv
import os



load_dotenv()

class DataManager:
    """Handles interaction with Google Sheet via Sheety API"""

    def __init__(self):
        self.destination_data = []
        self.customer_data = []

        # endpoints
        self.prices_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.users_endpoint = os.getenv("SHEETY_USER_ENDPOINT")

        # auth (your method)
        self.header = {
            "Authorization": f"Bearer {os.getenv('SHEETY_API_KEY')}"
        }

    # GET PRICES
    def get_destination_data(self):
        try:
            response = requests.get(self.prices_endpoint, headers=self.header)
            response.raise_for_status()

            data = response.json()
            self.destination_data = data.get("prices", [])

            return self.destination_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices: {e}")
            return []

    # UPDATE PRICE
    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }

        try:
            response = requests.put(
                url=f"{self.prices_endpoint}/{row_id}",
                json=new_data,
                headers=self.header
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Error updating data: {e}")

    # GET USER EMAILS
    def get_customer_emails(self):
        try:
            response = requests.get(self.users_endpoint, headers=self.header)
            response.raise_for_status()

            data = response.json()
            self.customer_data = data.get("users", [])
            print(self.customer_data)

            # convert to list of emails ONLY
            email_list = [user["whatIsYourEmail?"] for user in self.customer_data]

            return email_list

        except requests.exceptions.RequestException as e:
            print(f"Error fetching users: {e}")
            return []
