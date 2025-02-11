import time
import os
import streamlit as st
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
import toml

secrets = toml.load('.streamlit\secrets.toml')

# Hosting local client (LM studio), work on openai API
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=secrets['api_key']['GROQ_API_KEY'])
pc = Pinecone(api_key=secrets['api_key']['PC_API_KEY'])
index = pc.Index('akgec-data')

# Similarity Search and context generation from pinecone
def response(query, k):
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )
    results = index.query(
        namespace="doc1",
        vector=query_embedding[0].values,
        top_k=k,
        include_values=False,
        include_metadata=True
    )
    string=[]
    for i in range(k):
        string.append((results["matches"][i]['metadata']['source_text']))
    context=" ".join(string)

    return context

#funtion for calling chat model
def call_openai_chat_model(model, user_input, context):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": """You are a helpful chatbot for Ajay Kumar Garg Engineering College(akgec),
                                            Never answer to the question does not belongs to college or out of context.
                                            provide clear concise and well-formatted information from the context.
                                            - **Bold** key points.
                                            - Use *italics* for emphasis.
                                            - Utilize headings to organize long responses.
                                            - Use bullet points or numbered lists for multiple items.
                                            - Include tables where appropriate."""},
            {"role": "user", "content": f"context : {context}"},
            {"role": "user", "content": user_input}
        ],
        max_tokens=400,
        stream=False
    )
    return response.choices[0].message.content
     
# Streamlit Application
st.title("AKGEC ChatBot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def add_message():
    user_input = st.session_state["user_input"]
    if user_input:
        start = time.time()
        st.session_state['messages'].append(("User", user_input))
        context = response(user_input, k=5)
        ai_response = call_openai_chat_model(model="llama-3.3-70b-versatile", user_input=user_input, context=context)
        chat_end = time.time()
        t = f"{(chat_end-start):.2f} s"
        st.session_state['messages'].append(("AI", ai_response))
        st.session_state['messages'].append(("Time", t))
        st.session_state["user_input"] = ""

# Display messages
for role, message in st.session_state['messages']:
    st.write(f"**{role}**:  {message}")

# User input
st.text_input("You:", key="user_input", on_change=add_message)

# Clear chat
if st.button("Clear Chat"):
    st.session_state['messages'] = []
