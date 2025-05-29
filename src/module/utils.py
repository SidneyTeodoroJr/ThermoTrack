import os
import sqlite3
from datetime import datetime
from flet import (
    Text, LineChart, Colors, LineChartData, 
    LinearGradient, alignment, LineChartDataPoint
)

DB_FILE = os.path.join("assets", "data", "data-base.db")

def get_history():
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT datetime, temperature, efficiency FROM records ORDER BY datetime")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        processed_rows = []
        for dt_str, temp, eff in rows:
            dt = datetime.fromisoformat(dt_str)
            timestamp = int(dt.timestamp())
            processed_rows.append((timestamp, temp, eff))
        return processed_rows
    except Exception as e:
        print(f"Error retrieving history: {e}")
        return []

def create_chart(data, color):
    if not data:
        return Text("No data to display.", size=16)

    y_values = [y for _, y in data]
    x_values = [x for x, _ in data]

    min_y = min(y_values)
    max_y = max(y_values)

    y_range = max_y - min_y if max_y != min_y else 1
    min_y -= y_range * 0.1
    max_y += y_range * 0.1

    min_x = min(x_values)
    max_x = max(x_values)

    return LineChart(
        tooltip_bgcolor=Colors.with_opacity(0.8, Colors.BLACK),
        min_y=min_y,
        max_y=max_y,
        min_x=min_x,
        max_x=max_x,
        expand=True,
        data_series=[
            LineChartData(
                color=color,
                stroke_width=1,
                curved=False,
                stroke_cap_round=True,
                below_line_gradient=LinearGradient(
                    begin=alignment.top_center,
                    end=alignment.bottom_center,
                    colors=[Colors.with_opacity(0.25, color), "transparent"],
                ),
                data_points=[LineChartDataPoint(x, y) for x, y in data],
            )
        ],
    )
