import streamlit as st
import pandas as pd

# test data
employees = {
        "eid": [1,2,3],
        "ename": ["Pedro","Alfonso","Pikachu"],
        "escore": [100, 9000, 3],
        "pname": ["Windows", "ChadLinux","IDRobber"]
    }

projects  = ["Windows", "ChadLinux","IDRobber"]

columnConfig = {
    "eid": st.column_config.Column(label="eid", disabled = True),
    "ename": st.column_config.Column(label="ename", disabled = True),
    "escore": st.column_config.Column(label="escore", disabled = True),
    "pname": st.column_config.SelectboxColumn(label="pname", options = projects)
}

if __name__ == "__main__":
    st.title("Team Building")
    st.data_editor(employees, column_config = columnConfig)
