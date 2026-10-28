
#  Global Seismic Trends: Data-Driven Earthquake Insights.


Global Seismic Trends: Data-Driven Earthquake Insights is a data analytics project focused on analyzing global earthquake data to identify seismic patterns, understand earthquake frequency and magnitude, and explore the geographical distribution of seismic activity. The project uses historical earthquake records, data visualization, and statistical analysis to transform raw seismic data into meaningful insights.


## Features

 1. Load Data

    • Load the dataset directly from API or CSV into    Pandas.

    •  Convert date/time fields (time, updated) to datetime objects.

2. 	Clean Text Fields

    • Use Regex to extract country from place.

    •  Normalize alert field (if exists) to lowercase.

    • Ensure all string fields (magType, status, type, net, sources, types) are clean.

3. 	Clean Numeric Fields

    • Convert mag, depth_km, nst, dmin, rms, gap, magError, depthError, magNst, sig to numeric.

    • Fill missing numeric values with 0 or median if needed.

4. 	Add Derived Columns

    • Year, month, day, day_of_week from time.

    • Shallow/deep earthquake flag based on depth_km.

    • Strong/destructive flag based on mag thresholds.

5. 	Store Data in MySQL

    • Create table earthquakes with all 26 features and derived columns.

    •  Insert cleaned DataFrame using SQLAlchemy.
    


## Running Tests

Install Python – Install Python and VS Code.

Create Folder – Create a folder named Global_Seismic_Trends.

Open Terminal – Open the terminal in VS Code.

Install Libraries – Run:

```bash
    pip install pandas numpy matplotlib seaborn plotly streamlit
```

Download Dataset – Get earthquake data from the USGS Earthquake Catalog .

Create Python File – Create a file named app.py.

Load Data – Import the dataset using Pandas.

Analyze Data – Analyze earthquake magnitude, depth, location, and frequency.

Visualize Data – Create charts, graphs, and earthquake maps.

Run Project – Execute:

```bash
    streamlit run app.py
```

View Output – Open the local URL displayed in the terminal to view the interactive dashboard.

