from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


class Germinator:
    data: dict = {}
    readings: list = []
    processed_data: list = []

    def __init__(self, seed_data: dict):
        self.data = seed_data
        self.readings = self.data.get("data", [])
        self.__process_data()

    def __process_data(self):
        for reading in self.readings:
            created = reading.get("created_date")
            offset = timedelta(hours=-4)
            timestamp = datetime.fromisoformat(created.replace("Z", "+00:00")) + offset
            seed_data = reading.get("data", {})
            entry = {
                "timestamp": timestamp,
                "lights_on": seed_data.get("lights", False),
                "soil_temp": seed_data.get("soil", {}).get("soil_temp", 0),
                "soil_temp_target_high": 86,
                "soil_temp_target_low": 65,
                "soil_moisture": seed_data.get("soil", {}).get("moisture", 0),
                "soil_moisture_target_high": 1200,
                "soil_moisture_target_low": 800,
                "humidity_actual": seed_data.get("air", {})
                .get("humidity", {})
                .get("actual", 0),
                "humidity_target_low": seed_data.get("air", {})
                .get("humidity", {})
                .get("target", [])[0],
                "humidity_target_high": seed_data.get("air", {})
                .get("humidity", {})
                .get("target", [])[1],
                "temp_actual": seed_data.get("air", {})
                .get("temperature", {})
                .get("actual", 0),
                "temp_target_low": seed_data.get("air", {})
                .get("temperature", {})
                .get("target", [])[0],
                "temp_target_high": seed_data.get("air", {})
                .get("temperature", {})
                .get("target", [])[1],
            }
            self.processed_data.append(entry)


@st.cache_data(ttl=3600)
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=10)
    return response.json()


def germination(response_data: Germinator):
    df = pd.DataFrame(response_data.processed_data)
    df = df.sort_values(by="timestamp")

    # Device info
    st.header("Device Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Device ID", response_data.data.get("device_id", "Unknown"))
    with col2:
        phase = (
            response_data.data.get("notes", {}).get("phase", "Unknown")
            if response_data.data.get("notes")
            else "Unknown"
        )
        st.metric("Phase", phase)
    with col3:
        st.metric("Data Points", len(response_data.data.get("data", {})))

    # Humidity
    st.header("Humidity Monitoring")
    fig_humidity = go.Figure()

    fig_humidity.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["humidity_actual"],
            mode="lines+markers",
            name="Actual Humidity",
            line=dict(color="blue", width=3),
        )
    )

    fig_humidity.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["humidity_target_high"],
            mode="lines",
            name="Target High",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    fig_humidity.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["humidity_target_low"],
            mode="lines",
            name="Target Low",
            line=dict(color="green", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(0, 255, 0, 0.1)",
        )
    )

    fig_humidity.update_layout(
        title="Humidity Over Time with Target Range",
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

    # Temperature
    st.header("Temperature Monitoring")
    fig_temp = go.Figure()

    fig_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["temp_actual"],
            mode="lines+markers",
            name="Actual Temperature",
            line=dict(color="orange", width=3),
        )
    )

    fig_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["temp_target_high"],
            mode="lines",
            name="Target High",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    fig_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["temp_target_low"],
            mode="lines",
            name="Target Low",
            line=dict(color="green", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(0, 255, 0, 0.1)",
        )
    )

    fig_temp.update_layout(
        title="Temperature Over Time with Target Range",
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    # Soil Metrics
    st.header("Soil Conditions")

    # Soil Temperature Chart
    fig_soil_temp = go.Figure()
    fig_soil_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_temp"],
            mode="lines+markers",
            name="Soil Temperature",
            line=dict(color="brown", width=3),
        )
    )
    fig_soil_temp.update_layout(
        title="Soil Temperature Over Time",
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
    )

    fig_soil_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_temp_target_high"],
            mode="lines",
            name="Target High",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    fig_soil_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_temp_target_low"],
            mode="lines",
            name="Target Low",
            line=dict(color="green", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(0, 255, 0, 0.1)",
        )
    )

    fig_soil_temp.update_layout(
        title="Soil Temperature Over Time with Target Range",
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_soil_temp, use_container_width=True)

    # Soil Moisture Chart
    fig_soil_moisture = go.Figure()
    fig_soil_moisture.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_moisture"],
            mode="lines+markers",
            name="Soil Moisture",
            line=dict(color="blue", width=3),
        )
    )
    fig_soil_moisture.update_layout(
        title="Soil Moisture Over Time",
        xaxis_title="Time",
        yaxis_title="Moisture Reading",
    )

    fig_soil_moisture.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_moisture_target_high"],
            mode="lines",
            name="Target High",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    fig_soil_moisture.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["soil_moisture_target_low"],
            mode="lines",
            name="Target Low",
            line=dict(color="green", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(0, 255, 0, 0.1)",
        )
    )

    fig_soil_moisture.update_layout(
        title="Soil Moisture Over Time with Target Range",
        xaxis_title="Time",
        yaxis_title="Moisture",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_soil_moisture, use_container_width=True)

    # Show raw data
    st.header("Raw Data")
    if st.checkbox("Show raw data"):
        st.write(df)


st.set_page_config(
    page_title="The Germinator",
    page_icon=":seedling:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("The Germinator")

data = fetch_data(url=st.secrets["germinator_url"])
germinator = Germinator(seed_data=data)
germination(response_data=germinator)
