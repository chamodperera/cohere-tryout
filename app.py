import streamlit as st
import asyncio
from chat import urlValidator, response

st.set_page_config(layout="wide")

with st.sidebar:
    website = st.text_input('Enter web source link')
    st.write(f"Link: {website}")
    if not (urlValidator(website)):
        st.warning('Please enter a valid URL', icon='⚠️')


def run_async(func):
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    @run_async
    async def getResponse():
        return response(query, website)

    with st.spinner('Generating response...'):
        reply, documents = getResponse()

    st.session_state.documents = documents

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


with st.sidebar:
    for document in st.session_state.documents:
        st.divider()
        st.subheader(document['title'])
        st.markdown(document['snippet'])
