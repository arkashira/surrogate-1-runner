"""
UI layout for visualizing disk geometry data.

This module exposes a FastAPI application with a single endpoint
`/disk-geometry` that renders an HTML page containing a responsive
Plotly bar chart. The chart displays key disk geometry parameters
(cylinders, heads, sectors per track, total sectors) in a clear
and organized manner.

The page uses Bootstrap 5 for responsive styling and includes
Plotly's CDN for chart rendering. No external templates are
required – the HTML is generated inline.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go

app = FastAPI(title="Disk Geometry Viewer")

def _get_disk_geometry() -> dict:
    """
    Return sample disk geometry data.

    In a real implementation this would query the underlying storage
    system or read from a configuration file. For the purposes of
    this UI demo we return hard‑coded values.
    """
    return {
        "cylinders": 1024,
        "heads": 16,
        "sectors_per_track": 63,
        "total_sectors": 1024 * 16 * 63,
    }

@app.get("/disk-geometry", response_class=HTMLResponse)
def disk_geometry_page() -> HTMLResponse:
    """
    Render the disk geometry visualization page.

    The page contains:
    * A Bootstrap‑styled header.
    * A Plotly bar chart showing the geometry parameters.
    * Responsive layout that works on mobile, tablet, and desktop.
    """
    data = _get_disk_geometry()

    # Build the bar chart
    fig = go.Figure(
        data=[
            go.Bar(name="Cylinders", x=["Cylinders"], y=[data["cylinders"]]),
            go.Bar(name="Heads", x=["Heads"], y=[data["heads"]]),
            go.Bar(name="Sectors/Track", x=["Sectors/Track"], y=[data["sectors_per_track"]]),
            go.Bar(name="Total Sectors", x=["Total Sectors"], y=[data["total_sectors"]]),
        ]
    )
    fig.update_layout(
        title="Disk Geometry",
        barmode="group",
        xaxis_title="Parameter",
        yaxis_title="Value",
        template="plotly_white",
    )

    # Render the chart as an HTML fragment
    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    # Full page markup
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Disk Geometry Viewer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
              rel="stylesheet"
              integrity="sha384-ENjdO4Dr2bkBIFxQpeoYbq5B5Z9g6yYh5Z9Y5q5Z9Y5Z9Y5Z9Y5Z9Y5Z9Y5Z9Y5"
              crossorigin="anonymous">
    </head>
    <body class="container py-4">
        <h1 class="mb-4">Disk Geometry Visualization</h1>
        {chart_html}
    </body>
    </html>
    """
    return HTMLResponse(content=page)