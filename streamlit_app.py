import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Indian Stock Market Insights")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask anything about NSE, BSE stocks, trends, and predictions...")

# Function to get related topics for Indian stock market insights
def get_related_topics():
    return [
        "Past performance of NSE-listed stocks",
        "Current trends in the NSE and BSE",
        "Predictions for NIFTY and SENSEX",
        "Sector-wise analysis of Indian stocks",
        "Best stocks for long-term investment in India",
        "Impact of government policies on NSE & BSE"
    ]

# Function to get a response from OpenAI focused on Indian stocks
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that specializes in the Indian stock market, particularly NSE and BSE. "
                "You provide insights into past stock performance, current trends, and future predictions. "
                "Your responses should be based on financial analysis, market conditions, and historical data. "
                "You must strictly avoid discussing non-financial topics or stock markets outside India."
            )}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"User has asked: {user_input}. Provide a response strictly related to NSE and BSE stock markets."
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        
    # Display related topics
    st.markdown("**Related Topics You Might Find Helpful:**")
    for topic in get_related_topics():
        st.markdown(f"- {topic}")
