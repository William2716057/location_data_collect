# GeoAnalytics
## A program useful for gathering insights from geocoordinate data

## Features
- ability to add geocoordinate data to a map through user click or loading CSV file
- ability to visualise the data in point, cluster or heatmap form
- ability to view changes in data over time

### Contents
- analytics.html
- location_collect.py

## CSV Format
 
Uses a simple five-column CSV:
 
| Column | Description |
|---|---|
| `Count` | Row number (auto-incremented) |
| `Latitude` | Decimal degrees |
| `Longitude` | Decimal degrees |
| `Date` | `YYYY-MM-DD` |
| `Time` | `HH:MM:SS` |
