import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from germinator import Germinator


def configure_page():
    st.set_page_config(
        page_title="Tom.Camp Data",
        page_icon=":wave:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def configure_header():
    st.markdown("## Tom.Camp Data\n")


@st.cache_data
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=10)
    return response.json()


def germination(response_data: Germinator):
    df = pd.DataFrame(response_data.processed_data)

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
        st.metric("Data Points", len(response_data.data))

    # Humidity
    st.header("Humidity Monitoring")
    fig_humidity = go.Figure()

    # Add actual humidity line
    fig_humidity.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["humidity_actual"],
            mode="lines+markers",
            name="Actual Humidity",
            line=dict(color="blue", width=3),
        )
    )

    # Add target range as a filled area
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

    # Add target range as a filled area
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
    col1, col2 = st.columns(2)

    with col1:
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
        st.plotly_chart(fig_soil_temp, use_container_width=True)

    with col2:
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
        st.plotly_chart(fig_soil_moisture, use_container_width=True)

    # Show raw data
    st.header("Raw Data")
    if st.checkbox("Show raw data"):
        st.write(df)


def main():
    configure_page()
    configure_header()
    data = fetch_data(url="https://data.tom.camp/api/devices/67e0a7e5237033b03c44a99a")
    germinator = Germinator(data=data)
    germination(germinator)


if __name__ == "__main__":
    main()
