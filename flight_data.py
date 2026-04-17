class FlightData:
    # Stores structured flight details
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    def __str__(self):
        return f"{self.origin_airport} → {self.destination_airport} | ₹{self.price} | {self.out_date} - {self.return_date} | Stops: {self.stops}"


def find_cheapest_flight(data, return_date):

    # Step 1: Validate input data
    if not data or ("best_flights" not in data and "other_flights" not in data):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Step 2: Combine all flights into one list
    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    if not all_flights:
        print("No flights found")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    print(f"Checking {len(all_flights)} flights...")

    # Step 3: Initialize tracking variables
    lowest_price = float('inf')
    cheapest_flight = None

    # Step 4: Loop through all flights
    for flight in all_flights:
        try:
            price = flight["price"]
            origin_airport = flight["flights"][0]["departure_airport"]["id"]
            destination_airport = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]

            # NEW: calculate number of stops
            stops = len(flight["flights"]) - 1

        except (KeyError, IndexError):
            continue  # skip broken flight entries

        # Step 5: compare price
        if price < lowest_price:
            lowest_price = price

            cheapest_flight = FlightData(
                price=price,
                origin_airport=origin_airport,
                destination_airport=destination_airport,
                out_date=out_date,
                return_date=return_date,
                stops=stops
            )

            print(f"New cheapest flight: {destination_airport} for ₹{price}")

    # Step 6: final safety check
    if cheapest_flight is None:
        print("No valid flights found")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    return cheapest_flight