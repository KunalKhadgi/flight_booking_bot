import os 
import requests
from dotenv import load_dotenv  # ✅ Import dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API Key from .env
API_KEY = os.getenv("SERPAPI_KEY")
if not API_KEY:
    raise ValueError("Error: SERPAPI_KEY is not set. Please check your .env file.")

def fetch_flights(departure, arrival, date, preferred_airline=None, seating_class=None):
    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": date,
        "currency": "INR",
        "hl": "en",
        "type": "2",  # One-way
        "api_key": API_KEY,
        # "airline": preferred_airline,  # ✅ Preferred airline (e.g., "AA" for American Airlines)
        # "travel_class": seating_class  # ✅ Seating class (e.g., "economy", "business", "first")


#  airline and travel_class won't work since its not in the api code params :/                    

    }

    

#   print(preferred_airline, seating_class)

# search engine
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code != 200:
        return f"API Error: {response.status_code}"

    results = response.json()
    if "best_flights" not in results:
        return "No flights found."

    flights = results["best_flights"]
    response_text = "**Available Flights:**\n\n"


# seperates the given text 
    for flight in flights:
        details = flight["flights"][0]

        print(preferred_airline, seating_class, '\n')

        # ✅ Execute further if preferred_airline and seating_class match (or are None)
        if preferred_airline and preferred_airline != details.get("airline"):
            continue  # ❌ Skip flights that don’t match the preferred airline (if specified)

        if seating_class and seating_class.lower() != flight.get("travel_class", "").lower():
            continue  # ❌ Skip flights that don’t match the seating class (if specified)

        # ✅ If both are None or match, continue execution

        response_text += (
            f"✈ **{details['airline']}** ({details['flight_number']})\n"
            f"🛫 Depart: {details['departure_airport']['name']} at {details['departure_airport']['time']}\n"
            f"🛬 Arrive: {details['arrival_airport']['name']} at {details['arrival_airport']['time']}\n"
            f"⏳ Duration: {flight['total_duration']} min\n"
            f"💰 Price: INR {flight.get('price', 'N/A')}\n"    # N/A to avoid error if no price
            f"🪑 Seating Class: {flight.get("travel_class")}\n\n"  # ✅ Fetching seating class from API response

        )
        # print(response_text)      

    return response_text
