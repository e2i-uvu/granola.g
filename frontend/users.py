import streamlit as st

import toml

USERS = "./.streamlit/users.toml"

user_data = toml.load(USERS)

st.title("Users :material/person_check:")
st.write("---")

users = [u for u in user_data["users"] if u["role"] != "developer"]
devs = [u for u in user_data["users"] if u["role"] == "developer"]

# st.write(user_data)
with st.form("verification", border=False):
    modified_user_data = st.data_editor(
        users,
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
        # list(modified_user_data).append(devs)
        with open(USERS, "w") as f:
            user_data["users"] = modified_user_data + devs
            toml.dump(user_data, f)

        st.toast(
            ":green-background[Successfully Updated Users]",
            icon=":material/done_outline:",
        )
