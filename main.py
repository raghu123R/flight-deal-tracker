import requests_cache
from pprint import pprint
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


# CACHE SETUP
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

#  INITIAL SETUP
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "BLR"

#  GET SHEET DATA
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)

#  UPDATE IATA CODES
data_manager.destination_data = sheet_data

# RETRIEVE CUSTOMER EMAILS
customer_data = data_manager.get_customer_emails()
customer_email_list = customer_data
print(f"Customer emails: {customer_email_list}")

#  DATE SETUP
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)
RETURN_DATE = six_month_from_today.strftime("%Y-%m-%d")

# FLIGHT SEARCH
for destination in sheet_data:
    city = destination["city"]
    iata_code = destination["iataCode"]
    lowest_price = destination["lowestPrice"]
    row_id = destination["id"]

    # skip origin city
    if iata_code == ORIGIN_CITY_IATA:
        continue

    print(f"\n✈️ Checking flights for {city}...")

    # DIRECT FLIGHTS
    flights = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        iata_code,
        from_time=tomorrow,
        to_time=six_month_from_today,
        is_direct=True
    )

    if flights is None:
        print("No direct flight data returned")
        continue

    cheapest_flight = find_cheapest_flight(
        flights,
        return_date=RETURN_DATE
    )

    print(f"Direct flight {city}: ₹{cheapest_flight.price}")

    #  INDIRECT FLIGHTS
    if cheapest_flight.price == "N/A":

        print(f"No direct flight found for {city}. Searching indirect flights...")

        flights = flight_search.check_flight(
            ORIGIN_CITY_IATA,
            iata_code,
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )

        if flights is None:
            print("No indirect flight data returned")
            continue

        cheapest_flight = find_cheapest_flight(
            flights,
            return_date=RETURN_DATE
        )

        print(f"Indirect flight {city}: ₹{cheapest_flight.price}")

    #  PRICE CHECK
    if (
        cheapest_flight.price != "N/A"
        and cheapest_flight.price < lowest_price
    ):
        print(f"🔥 Lower price found for {city}!")

        data_manager.update_lowest_price(row_id, cheapest_flight.price)

        #  BUILD MESSAGE
        if cheapest_flight.stops == 0:
            message = (
                f"✈️ Low price alert! Only ₹{cheapest_flight.price} to fly direct "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            )
        else:
            message = (
                f"✈️ Low price alert! Only ₹{cheapest_flight.price} to fly "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                f"with {cheapest_flight.stops} stop(s), "
                f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."
            )

        print(f"📩 Price drop found for {city}! Sending notifications...")

        # SEND SMS
        notification_manager.send_sms(message_body=message)

        # SEND EMAILS
        notification_manager.send_emails(
            email_list=customer_email_list,
            email_body=message
        )