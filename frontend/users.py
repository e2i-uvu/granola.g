import streamlit as st

import toml

SECRETS = "./.streamlit/secrets.toml"

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
