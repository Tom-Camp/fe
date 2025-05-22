from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from base import BaseClass


class NuLayInn(BaseClass):

    def __init__(self, data: dict):
        super().__init__(data)
        self.__process_data()

    def __process_data(self):
        for reading in self.readings:
            created = reading.get("created_date")
            offset = timedelta(hours=-4)
            timestamp = datetime.fromisoformat(created.replace("Z", "+00:00")) + offset
            data = reading.get("data", {})
            entry = {
                "timestamp": timestamp,
                "battery": data.get("battery"),
                "outside_temp": data.get("outside", {}).get("air_temp", 0.0),
                "outside_humidity": data.get("outside", {}).get("humidity", 0.0),
                "coop_temp": data.get("coop", {}).get("coop_temp", 0.0),
                "coop_humidity": data.get("coop", {}).get("coop_humidity", 0.0),
                "coop_gas": data.get("coop", {}).get("coop_gas", 0.0),
                "gas_low": 0.0,
                "gas_high": 10000.0,
                "coop_pressure": data.get("coop", {}).get("coop_pressure", 0.0),
            }
            self.processed_data.append(entry)


@st.cache_data(ttl=3600)
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=10)
    return response.json()


def nulay_display(response_data: NuLayInn):
    df = pd.DataFrame(response_data.processed_data)
    df = df.sort_values(by="timestamp")

    # Temperature
    st.header("Temperature")
    fig_coop_temp = go.Figure()

    fig_coop_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["outside_temp"],
            mode="lines+markers",
            name="Outside Temperature",
            line=dict(color="blue", width=3),
        )
    )

    fig_coop_temp.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["coop_temp"],
            mode="lines",
            name="Inside Temperature",
            line=dict(color="red", width=3),
        )
    )

    fig_coop_temp.update_layout(
        title="Temperature Over Time Outside and Inside the COOP",
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_coop_temp, use_container_width=True)

    # Humidity
    st.header("Humidity")
    fig_coop_humid = go.Figure()

    fig_coop_humid.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["outside_humidity"],
            mode="lines+markers",
            name="Outside Humidity",
            line=dict(color="blue", width=3),
        )
    )

    fig_coop_humid.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["coop_humidity"],
            mode="lines",
            name="Inside Humidity",
            line=dict(color="red", width=3),
        )
    )

    fig_coop_humid.update_layout(
        title="Humidity Over Time Outside and Inside the COOP",
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_coop_humid, use_container_width=True)

    # Mox
    st.header("Volatile Organic Compound (VOX) Monitoring")

    # Mox Chart
    fig_mox = go.Figure()
    fig_mox.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["coop_gas"],
            mode="lines+markers",
            name="VOX level",
            line=dict(color="red", width=3),
        )
    )
    fig_mox.update_layout(
        title="Coop Volatile Organic Compounds (VOC) Over Time",
        xaxis_title="Time",
        yaxis_title="Gas",
    )

    fig_mox.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["gas_high"],
            mode="lines",
            name="Unclean air",
            line=dict(color="brown", width=2, dash="dash"),
        )
    )

    fig_mox.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["gas_low"],
            mode="lines",
            line=dict(color="brown", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(0, 255, 0, 0.1)",
        )
    )

    fig_mox.update_layout(
        title="Coop Metal Oxide (MOS) Gas Over Time with Poor Air Zone",
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_mox, use_container_width=True)

    # Mox
    st.header("Battery Level")

    # Battery Chart
    fig_bat = go.Figure()
    fig_bat.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["battery"],
            mode="lines+markers",
            name="Battery level",
            line=dict(color="red", width=3),
        )
    )
    fig_bat.update_layout(
        title="Sensor Battery Level Over Time",
        xaxis_title="Time",
        yaxis_title="Gas",
    )

    fig_bat.update_layout(
        title="Sensor Battery Level Over Time",
        xaxis_title="Time",
        yaxis_title="Battery Level (V)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_bat, use_container_width=True)


st.set_page_config(
    page_title="NuLay Inn",
    page_icon=":chicken:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("NuLay Inn")

data = fetch_data(url=st.secrets["nulay_url"])
print(data)
nu_lay = NuLayInn(data=data)
nulay_display(response_data=nu_lay)
