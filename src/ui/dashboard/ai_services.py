import streamlit as st
import yaml
from pathlib import Path

def load_ai_services_config():
    config_path = Path("/opt/axentx/surrogate-1/src/config/ai_services_config.yaml")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_ai_services_config(config):
    config_path = Path("/opt/axentx/surrogate-1/src/config/ai_services_config.yaml")
    with open(config_path, 'w') as file:
        yaml.dump(config, file)

def ai_services_dashboard():
    st.title("AI Services Dashboard")

    config = load_ai_services_config()

    st.header("Configure AI Services")

    for service, settings in config.items():
        with st.expander(f"{service} Configuration"):
            st.subheader(f"{service} Settings")

            for key, value in settings.items():
                if isinstance(value, bool):
                    settings[key] = st.checkbox(key, value=value)
                elif isinstance(value, int):
                    settings[key] = st.number_input(key, value=value)
                else:
                    settings[key] = st.text_input(key, value=value)

    if st.button("Save Configuration"):
        save_ai_services_config(config)
        st.success("Configuration saved successfully!")

    st.header("Monitoring Information")
    st.write("Monitoring information will be displayed here.")