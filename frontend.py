import streamlit as st
from chatbot import GeneralChat, FlightChat

st.title("✈️ Flight Booking Chatbot")

# ✅ Maintain chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ User input
user_input = st.text_input("You:", "", key="user_input")

if st.button("Send"):
    if user_input:
        # ✅ Detect if query is flight-related
        if "flight" in user_input.lower():
            response = FlightChat.chat_with_user(user_input)

        else:
            response = GeneralChat.chat(user_input)

        st.session_state.chat_history.append((user_input, response))


for index, (user_msg, bot_reply) in enumerate(st.session_state.chat_history):

    st.text(f"You: {user_msg}")

    # ✅ Check if the bot reply contains multiple flights
    if "✈" in bot_reply and "💰 Price:" in bot_reply:
        flights = bot_reply.strip().split("\n\n")  # ✅ Split multiple flights
        for flight_index, flight in enumerate(flights):
            
            # ✅ Check if "⏳ Duration:" exists in the text
            if "⏳ Duration:" not in flight:
                continue  # 🚀 Skip this flight if no duration is found
            
            with st.container():  # ✅ Create a button for each flight
                st.text(f"Bot: {flight}")
                if st.button("✈ Book This Flight", key=f"book_{index}_{flight_index}"):
                    st.success("✅ Your flight has been booked successfully!")
    else:
        st.text(f"Bot: {bot_reply}")
