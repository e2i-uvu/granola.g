import streamlit as st

st.title("Guide")

box_style_1 = """
    <style>
   .outer-box1 {
        border: 2px solid black;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
    }
    .inner-box1 {
        border: 2px solid #00FF00; /* UVU green */
        padding: 10px;
        # margin: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    </style>
"""

box_style_2 = """
    <style>
    .box2 {
        border: 4px solid #275D38;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    </style>
"""

st.markdown(box_style_1, unsafe_allow_html=True)
st.markdown(box_style_2, unsafe_allow_html=True)

box_content_1 = """
    <div class="outer-box1">
        <div class="inner-box1">
            <p>This is some text inside the second box!</p>
        </div>
    </div>
"""
box_content_2 = """
    <div class="box2">
        <p>This is some text inside a box!</p>
    </div>
"""
st.markdown(box_content_1, unsafe_allow_html=True)
st.markdown(box_content_2, unsafe_allow_html=True)
