import threading
import requests
import re
from back import update_data, get_last_datetime
from module.utils import create_chart

from flet import (
    Page, ThemeMode, Container, app, Theme, Colors, Text,
    FontWeight, ElevatedButton, Icons, padding, Column, Row, TextField
)
from datetime import datetime

API_URL = "http://localhost:8000/history"

def fetch_history():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        processed_rows = []
        for record in data:
            dt = datetime.fromisoformat(record["datetime"])
            timestamp = int(dt.timestamp())
            processed_rows.append((timestamp, record["temperature"], record["efficiency"]))
        return processed_rows
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return []

def main(page: Page):
    page.padding = 0
    page.title = "ThermoTrack"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = ThemeMode.DARK
    page.theme = Theme(color_scheme_seed="ORANGE")

    update_thread = None
    stop_thread = False
    current_city = "São Paulo"

    rows = fetch_history()
    data = [(row[0], row[1]) for row in rows]  # timestamp, temperature

    chart_container = Container(
        content=create_chart(data, Colors.ORANGE),
        expand=True,
    )

    legend_text = Text("Temperature (°C)", size=18, weight=FontWeight.BOLD)

    log_message = Text("", size=14, color=Colors.RED)

    def update_last_reading():
        last_dt_str = get_last_datetime()
        if last_dt_str:
            try:
                dt = datetime.fromisoformat(last_dt_str)
                last_reading = dt.strftime("%d/%m/%Y %H:%M:%S")
            except Exception:
                last_reading = "invalid data"
        else:
            last_reading = "no data"
        date_time.value = f"Last reading: {last_reading}"
        page.update()

    last_dt_str = get_last_datetime()
    if last_dt_str:
        try:
            dt = datetime.fromisoformat(last_dt_str)
            last_reading = dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            last_reading = "invalid data"
    else:
        last_reading = "no data"

    date_time = Text(f"Last reading: {last_reading}")

    def switch_dataset(e):
        dataset = e.control.data
        rows = fetch_history()

        if dataset == "temp":
            data = [(row[0], row[1]) for row in rows]
            color = Colors.ORANGE
            legend = "Temperature (°C)"
            page.theme.color_scheme_seed = "ORANGE"
        elif dataset == "eff":
            data = [(row[0], row[2]) for row in rows]
            color = Colors.GREEN
            legend = "Efficiency (%)"
            page.theme.color_scheme_seed = "GREEN"
        else:
            data = []
            color = Colors.GRAY
            legend = ""
            page.theme.color_scheme_seed = "GRAY"

        chart_container.content = create_chart(data, color)
        legend_text.value = legend

        update_last_reading()
        page.update()

    buttons = Row(
        alignment="center",
        spacing=20,
        controls=[
            ElevatedButton("Temperature", on_click=switch_dataset, data="temp", icon=Icons.SUNNY_SNOWING),
            ElevatedButton("Efficiency", on_click=switch_dataset, data="eff", icon=Icons.AUTO_GRAPH),
        ],
    )

    searchCity = TextField(
        label="Search",
        hint_text="Search for a city..",
        counter_text="{value_length}/{max_length} chars used",
        max_length=30,
        prefix_icon=Icons.SEARCH,
        on_submit=None  # will be set later to use the function defined below
    )

    # Simple validation: letters, spaces and hyphens only
    def validate_city_name(city: str) -> bool:
        pattern = r"^[a-zA-Z\s\-]+$"
        return re.match(pattern, city) is not None

    def update_data_wrapper(city):
        nonlocal stop_thread
        while not stop_thread:
            update_data(city)

    def on_search_submit(e):
        nonlocal update_thread, stop_thread, current_city

        city = searchCity.value.strip()

        if not city:
            log_message.value = "⚠️ City field is empty."
            page.update()
            return
        
        if not validate_city_name(city):
            log_message.value = "❌ Invalid name! Use only letters, spaces, and hyphens."
            page.update()
            return

        log_message.value = f"🔍 Searching data for city: {city}"
        page.update()

        stop_thread = True
        if update_thread and update_thread.is_alive():
            update_thread.join(timeout=1)

        stop_thread = False
        current_city = city

        update_thread = threading.Thread(target=update_data_wrapper, args=(current_city,), daemon=True)
        update_thread.start()

        rows = fetch_history()
        data = [(row[0], row[1]) for row in rows]
        chart_container.content = create_chart(data, Colors.ORANGE)
        legend_text.value = "Temperature (°C)"
        update_last_reading()
        page.update()

    searchCity.on_submit = on_search_submit

    page.add(
        Container(
            expand=True,
            content=Column(
                spacing=20,
                controls=[
                    Container(
                        padding=padding.only(top=10),
                        content=Column(
                            [
                                Text(
                                    "Temperature and Efficiency Data",
                                    size=24,
                                    weight=FontWeight.BOLD,
                                ),
                                buttons,
                                legend_text,
                                date_time,
                                Container(
                                    padding=5,
                                    width=400,
                                    content=searchCity
                                ),
                                log_message,  # visible log message to the user
                            ],
                            alignment="center",
                            horizontal_alignment="center",
                        ),
                    ),
                    Container(
                        expand=True,
                        padding=15,
                        content=chart_container
                    ),
                ],
            ),
        )
    )

    update_thread = threading.Thread(target=update_data_wrapper, args=(current_city,), daemon=True)
    update_thread.start()

if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "São Paulo"
    threading.Thread(target=update_data, args=(city,), daemon=True).start()

    app(target=main)