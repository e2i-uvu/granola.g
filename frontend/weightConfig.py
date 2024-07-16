#import streamlit as st
import json
import os
import logging
from copy import deepcopy

if __name__ == "__main__":
    #configFile = "./frontend/.weightConfig.json"
    configFilePath = ".weightConfig.json"
    defaultConfig = str(dict(enjoyment = 3.0, social = 2.0))

    """Confirm existence of configuration file."""
    try:
        if os.stat(configFilePath).st_size == 0:
            # print("File is empty")
            with open(configFile, "w") as configFile:
                configFile.write(defaultConfig)

    except FileNotFoundError:
        # print("File not found error!")
        with open(configFile, "w") as configFile:
            configFile.write(defaultConfig)

    """Import saved configuration."""
    with open(configFilePath, "r") as configFile:
        ORIGINAL_CONFIG: dict[str, float] = json.loads(configFile)
        weightConfig = deepcopy(ORIGINAL_CONFIG)

    """Save new configuration."""


    
