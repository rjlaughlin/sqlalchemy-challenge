# sqlalchemy-challenge

## Overview
This project conducts a climate analysis for Honolulu, Hawaii, to support trip planning decisions. Using a SQLite database of climate data, the analysis explores precipitation patterns and station activity and creates a Flask API to provide access to key climate insights.

## Features

### Part 1: Climate Data Analysis
#### Precipitation Analysis
- Extracts precipitation data for the last 12 months using SQLAlchemy ORM queries.
- Loads data into a Pandas DataFrame for analysis and visualization.
- Plots precipitation trends over time.
- Summarizes precipitation data using descriptive statistics.

#### Station Analysis
- Identifies the number of weather stations in the dataset.
- Finds the most active station based on observation counts.
- Calculates temperature statistics (minimum, maximum, and average) for the most active station.
- Retrieves and visualizes the last year of temperature observations as a histogram.

### Part 2: Flask API Development
Creates a Flask application with the following routes:
- `/`: Homepage displaying available API routes.
- `/api/v1.0/precipitation`: JSON representation of the last 12 months of precipitation data.
- `/api/v1.0/stations`: JSON list of all weather stations.
- `/api/v1.0/tobs`: JSON list of temperature observations for the most active station from the last year.
- `/api/v1.0/<start>`: JSON list of minimum, average, and maximum temperatures from a given start date to the end of the dataset.
- `/api/v1.0/<start>/<end>`: JSON list of temperature statistics for a specified start and end date range.

## Deliverables
- **Jupyter Notebook**: Contains SQLAlchemy queries and data analysis. - `climate.ipynb)`
- **Flask App**: Implements API routes based on the analysis. - `app.py`
- **Resources Folder**: Includes the SQLite database (`hawaii.sqlite`) and other data files.
- **Visualization Outputs**: Precipitation trends and temperature histograms.

## Setup and Dependencies

Before starting, ensure you have the following libraries installed:

```python
# Dependencies
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, desc, func

from flask import Flask, jsonify
```

## Running the Analysis
- Clone the repository and navigate to the project directory.
- Install dependencies as shown above.
- Run the Jupyter Notebook to generate the analysis and visualizations and the Python script to run the Flask API.

