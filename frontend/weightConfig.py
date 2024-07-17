import streamlit as st
import json
import os
#import logging
import numpy as np
from copy import deepcopy

# TODO: Add logging functionality?

if __name__ == "__main__":
    #configFile = "./frontend/.weightConfig.json"
    # TODO:  Maybe make this configFilePath a env?
    configFilePath: str = ".weightConfig.json"
    defaultConfig: str = '{"Enjoyment" : 3.0, "Social" : 2.0}'

    # """Import saved configuration."""
    try:
        if os.stat(configFilePath).st_size == 0:
            with open(configFilePath, "w") as configFile:
                configFile.write(defaultConfig)
        else:
            with open(configFilePath, "r") as configFile:
                _ = json.load(configFile)
    except JSONDecodeError:
        st.write("Configuration file is corrupted. Loading Default Configuration.")

    except FileNotFoundError:
        st.write("Configuration file not found.")
        with open(configFile, "w") as configFile:
            configFile.write(defaultConfig)

    finally:
        with open(configFilePath, "r") as configFile:
                ORIGINAL_CONFIG: dict[str, float] = json.load(configFile)
                st.session_state['weightConfig'] = deepcopy(ORIGINAL_CONFIG)


    # Display Configuration
    st.title("Weight Configuration")

    for key, value in st.session_state['weightConfig'].items():
        st.select_slider(label = key.title(),
                         options = np.arange(start = 1, stop = 11, step = 1),
                         value = value,
                         key = key)

    #"""Save new configuration."""
    if st.button("Save Configuration"):
        serializableConfigState = {}
        for key in st.session_state['weightConfig']:
            st.session_state['weightConfig'][key] = st.session_state[key]
            serializableConfigState[key] = int(st.session_state[key])

        with open(configFilePath, "w") as configFile:
            json.dump(obj = serializableConfigState, fp = configFile)

    #"""Restore Configuration"""
    if st.button("Restore Configuration"):
        st.session_state['weightConfig'] = deepcopy(ORIGINAL_CONFIG)
