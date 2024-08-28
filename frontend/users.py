import streamlit as st

import toml

SECRETS = "./.streamlit/secrets.toml"
USERS = "./.streamlit/users.toml"

# TODO: So after reading the docs, we can't update `secrets.toml`
# and work with the updates without restarting the app.
# So I am thinking we might as well just change the file

user_data = toml.load(SECRETS)

st.header("Users")

# st.write(user_data)
with st.form("verification", border=False):
    modified_user_data = st.data_editor(
        user_data["users"],
        column_config={
            "id": st.column_config.NumberColumn("UVID", disabled=True, format="%i"),
            "verified": st.column_config.CheckboxColumn(
                "Verified?",
                help="Select to allow access",
                default=False,
            ),
        },
        # disabled
        use_container_width=True,
        hide_index=True,
    )
    submitted = st.form_submit_button(
        "Process Changes", type="primary", use_container_width=True
    )
    if submitted:
        with open(SECRETS, "w") as f:
            user_data["users"] = modified_user_data
            toml.dump(user_data, f)

        st.toast("success")
