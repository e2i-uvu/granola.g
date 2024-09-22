import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

st.header("Current Session State")
st.write("---")

st.write(st.session_state)

st.header("employees")

r = requests.get(
    st.session_state.backend["url"] + "employees",
    auth=HTTPBasicAuth(
        st.session_state.backend["username"], st.session_state.backend["password"]
    ),
)
if r.status_code == 200:
    st.write(r.json())
else:
    st.error("get wrecked")

st.write()

st.header("cookies")
st.write(st.context.cookies)

st.header("headers")
st.write(st.context.headers)
