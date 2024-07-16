import streamlit as st

st.markdown(
"""
<style>
.centered-bottom {
    position: relative;
    bottom: 0;
    width: 100%;
    text-align: center;
}

.centered-bottom img {
    width: 400px;
}
</style>
""",
unsafe_allow_html=True)

st.title("About page")

st.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
 incididunt ut labore et dolore magna aliqua. Varius duis at consectetur lorem donec massa 
 sapien faucibus et. Felis imperdiet proin fermentum leo vel. Et ligula ullamcorper malesuada 
 proin libero. Non arcu risus quis varius. Dolor sit amet consectetur adipiscing elit. Vitae
  suscipit tellus mauris a diam maecenas. Amet cursus sit amet dictum sit amet justo donec enim.
   Urna cursus eget nunc scelerisque viverra mauris in. Vulputate odio ut enim blandit volutpat 
   maecenas volutpat. Non sodales neque sodales ut. Proin nibh nisl condimentum id venenatis a 
   condimentum vitae. Accumsan sit amet nulla facilisi. Purus ut faucibus pulvinar elementum 
   integer enim neque volutpat ac.""")

st.markdown("""Est ullamcorper eget nulla facilisi etiam dignissim diam. Egestas dui id ornare
 arcu odio ut sem nulla. Commodo ullamcorper a lacus vestibulum sed arcu non odio euismod. 
 Bibendum at varius vel pharetra vel turpis nunc. Praesent semper feugiat nibh sed pulvinar 
 proin gravida hendrerit. """)

st.markdown(
    """
    <div class="centered-bottom">
        <img src="https://www.uvu.edu/innovation/images/e2icolor-01.png" alt="UVU Innovation">
    </div>
    """,
    unsafe_allow_html=True
)