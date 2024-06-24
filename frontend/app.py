"""
Entrypoint for the streamlit frontend
"""

import streamlit as st

# can add pages here
pages = {"Interview": [st.Page("interview.py", title="Interview")]}

pg = st.navigation(pages)
pg.run()
