import streamlit as st

st.header("Current Session State")
st.write("---")

st.write(st.session_state)

st.write("cookies")
st.write(st.context.cookies)

st.write("headers")
st.write(st.context.headers)
