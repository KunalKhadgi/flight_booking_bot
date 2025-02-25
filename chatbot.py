import os
import json
import flight_fetcher
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API Key from .env
api_key = os.getenv("GOOOGLE_API_KEY")
if not api_key:
    raise ValueError("Error: GOOGLE_API_KEY is not set. Please check your .env file.")

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

# --------------------------- General Chat --------------------------- #
class GeneralChat:
    """Handles general user queries that are not related to flight booking."""

    @staticmethod
    def chat(user_input):
        """Uses Google Gemini AI to handle general conversation."""
        response = llm.invoke(user_input)
        return response

# --------------------------- Flight Booking Chat --------------------------- #
class FlightChat:
    """Handles flight booking-related queries, extracting travel details."""

    @staticmethod
    def extract_flight_details(user_input):
        """
        Extracts departure, arrival, date, preferred airline, and seating class from user input.
        Converts relative dates like 'tomorrow' to YYYY-MM-DD format.
        """
        prompt = (
            f"Extract the departure airport, arrival airport, date, preferred airline (if mentioned), "
            f"and seating class (if mentioned) from this text: '{user_input}'. "
            "Convert city names to their respective 3-letter IATA airport codes. "
            "Convert relative dates (e.g., 'tomorrow', 'next Monday') into the YYYY-MM-DD format after checking live date from internet or web browser. "
            "If no airline or seating class is specified, return null for those values. "
            "Return the response in strict JSON format with keys: 'departure_airport', 'arrival_airport', 'date', 'preferred_airline', and 'seating_class'."
            "For flight name eg. airindia -> 'Air India'. Similarly 'Air India Express', 'SpiceJet', 'IndiGo', 'Akasa Air"
            'Ensure the seating class is extracted in one of the standard categories: - "Economy" - "Premium Economy"  - "Business"  - "First Class"  - None (if unspecified)'
        )
        
        response = llm.invoke(prompt)
        print("Raw Response:", response)  # ✅ Print raw response
        print("Response Type:", type(response))  # ✅ Check type before decoding
        try:
            cleaned_response = response.strip("```json").strip("```").strip()
            details = json.loads(cleaned_response)  # ✅ Safe JSON parsing
            print("Parsed JSON:", details,"\n")  # Debugging Step
          # print("Available Keys:", details.keys())  # Check key names
    
            return (
                details.get("departure_airport"), 
                details.get("arrival_airport"), 
                details.get("date"), 
                details.get("preferred_airline"), 
                details.get("seating_class")
            )
        except json.JSONDecodeError:
           # print("returned_none")
            return None, None, None, None, None

    @staticmethod
    def chat_with_user(user_input):
        """
        Processes user input, extracts flight details, fetches flight data, and returns the response.
        """
        departure, arrival, date, preferred_airline, seating_class = FlightChat.extract_flight_details(user_input)

        if departure and arrival and date:
            flights = flight_fetcher.fetch_flights(departure, arrival, date,preferred_airline, seating_class)
            return flights if flights else "No flights found."
        else:
            return "Please provide a valid departure location, arrival location, and date."
