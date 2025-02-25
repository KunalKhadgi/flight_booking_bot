
Initialises chat and sends the input to llm i.e. GoogleGenerativeAI
It decides weather to continue general chat or a booking chat based on the keyword 'flight' in chat
If booking chat it requests the serpapi in flight_fetcher.py to fetch flight 
LLM shows the fetched flights to the user 
User gets book flight button on frontend to simulate booking 
