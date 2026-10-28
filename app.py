import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title='Earthquake Data Analysis Dashboard', layout= 'wide')

@st.cache_resource
def get_connection():
    engine = create_engine('mysql+pymysql://GUVI:sami8754@localhost:3306/guvi_project1')
    return engine
    
engine = get_connection()

st.title('End-to-End Earthquake Data Analysis Dashboars')
st.sidebar.header('Select Task Category')

category = st.sidebar.selectbox('Choose Category', [
    '1. Magnitude & Depth',
    '2. Time Analysis',
    '3. Event Type & Quality Metrics',
    '4. Seismic Pattern & Trends',
    '5. Depth, Location & Distance Analysis'
])

if category == '1. Magnitude & Depth':
    st.header('Magnitude & Depth Analysis')
    task = st.selectbox('Select Task', [
        '1. Top 10 Strongest Earthquakes (Magnitude)',
        '2. Top 10 Deepest Earthquake (depth_km)',
        '3. Shallow Earthquakes (depth_km and Magnitude)',
        '4. Average depth per Country',
        '5. Average Magnitude per Magnitude Type'
    ])

    if '1.' in task:
        query = 'SELECT place, mag, depth_km, time FROM earthquakes ORDER BY mag DESC LIMIT 10;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '2.' in task:
        query = 'SELECT place, mag, depth_km, time FROM earthquakes ORDER BY depth_km DESC LIMIT 10;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '3.' in task:
        query = 'SELECT place, mag, depth_km, time FROM earthquakes WHERE depth_km < 50 AND mag > 7.5;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '4.' in task:
        query = 'SELECT country, AVG(depth_km) AS avg_depth FROM earthquakes GROUP BY country;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '5.' in task:
        query = 'SELECT magType, AVG(mag) AS avg_mag FROM earthquakes GROUP BY magType;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)

elif category == '2. Time Analysis':
    st.header('Time Analysis')
    task = st.selectbox('Select Task', [
        '6. Year with Most Earthquakes',
        '7. Month with Highest Number of Earthquakes',
        '8. Day of Week with Most Earthquakes',
        '9. Most Active Reporting Network (net)'
    ])

    if '6.' in task:    
        query = 'SELECT year, COUNT(*) AS count FROM earthquakes GROUP BY year ORDER BY count DESC;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
        st.bar_chart(df.set_index('year'))
    elif '7.' in task:
        query = 'SELECT month, COUNT(*) AS count FROM earthquakes GROUP BY month ORDER BY count DESC;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '8.' in task:
        query = 'SELECT day_of_week, COUNT(*) AS count FROM earthquakes GROUP BY day_of_week ORDER BY count DESC;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '9.' in task:
        query = 'SELECT net, COUNT(*) AS count FRoM earthquakes GROUP BY net ORDeR BY count DESC LIMIT 5;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)

elif category == '3. Event Type & Quality Metrics':
    st.header('3. Event Type & Quality Metrics')
    task = st.selectbox('Select Task', [
        '10. Count of Reviewed vs Automatic Earthquakes (Status)',
        '11. Count of Earthquakes Type (Type)',
        '12. Number of Earthquakes by Data Type (Types)',
        '13. Average Root Mean Squared(RMS) and Global Average Pooling(gap) per Country',
        '14. Events with High Station Coverage (nst > threshold)'
    ])

    if '10.' in task:
        query = 'SELECT status, COUNT(*) AS count FROM earthquakes GROUP BY status;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '11.' in task:
        query = 'SELECT type, COUNT(*) AS count FROM earthquakes GROUP BY type;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '12.' in task:
        query = 'SELECT types, COUNT(*) AS count FROM earthquakes GROUP BY types;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '13.' in task:
        query = 'SELECT country, AVG(rms) AS avg_rms, AVG(gap) AS avg_gap FROM earthquakes GROUP BY country;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '14.' in task:
        query = 'SELECT code, place, nst FROM earthquakes WHERE nst > 30 ORDER BY nst DESC LIMIT 10;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
        
elif category == '4. Seismic Pattern & Trends':
    st.header('Seismic Pattern & Trends Analysis')
    task = st.selectbox('Select Task', [
        '15. Number of Tsunamis Triggered per Year',
        '16. Count Earthquakes by Alert Levels',
        '17. Top 5 Countries with Highest Average Magnitude in past 5 Years',
        '18. Countries with both Shallow & Deep Earthquakes in same Month',
        '19. Year-Over-Year Growth Rate in Total Earthquakes',
        '20. Top 3 Most Seismically Active Regions (Frequency & AVG Magnitude)'
    ])

    if'15.' in task:
        query = 'SELECT year(time) AS earthquakes_year, SUM(tsunami) AS earthquakes_tsunami FROM earthquakes GROUP BY earthquakes_year ORDER BY earthquakes_tsunami;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '16.' in task:
        query = 'SELECT alert, COUNT(*) AS count FROM earthquakes GROUP BY alert;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '17.' in task:
        query = 'SELECT country, AVG(mag) AS avg_mag FROM earthquakes WHERE time >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR) GROUP BY country ORDER BY avg_mag DESC LIMIT 5;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '18.' in task:
        query = """
        SELECT country
        FROM earthquakes
        GROUP BY country, year(time), month(time)
        HAVING SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) > 0
           AND SUM(CASE WHEN depth_km >= 70 THEN 1 ELSE 0 END) > 0
        LIMIT 20;
        """
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '19.' in task:
        query = """
        WITH yearly_counts AS (
            SELECT year(time) AS yr, COUNT(*) AS cnt
            FROM earthquakes
            GROUP BY yr
        )
        SELECT yr, cnt,
            LAG(cnt) OVER (ORDER BY yr) AS pre_year_count,
            ((cnt - LAG(cnt) OVER (ORDER BY yr)) / NULLIF(LAG(cnt) OVER (ORDER BY yr), 0)) * 100 AS yoy_growth_rate
            FROM yearly_counts;
        """
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '20.' in task:
        query = """
        SELECT country, COUNT(*) AS frequency, AVG(mag) AS avg_magnitude, (COUNT(*) * AVG(mag)) AS seismic_score
        FROM earthquakes
        GROUP BY country
        ORDER BY seismic_score DESC
        LIMIT 3;
        """
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
        
elif category == '5. Depth, Location & Distance Analysis':
    st.header('Depth, Location & Distance Analysis')
    task = st.selectbox('Select Task', [
        '21. Average Depth of Earthquakes within of Euator',
        '22. Countries Having Highest Ratio of Shallow to Deep Earthquakes',
        '23. Average Magnitude Difference (Tsunami vs Non-Tsunami)',
        '24. Events with Lowest Data Reliability (Highest Error Margins)',
        '25. Consective Earthquakes Paris within 50km & 1 hour',
        '26. Regions with highest Frequency of Deep-Earthquakes (>300km)'
    ])

    if '21.' in task:
        query = 'SELECT country, AVG(depth_km) AS avg_depth FROM earthquakes WHERE latitude BETWEEN -5 AND 5 GROUP BY country;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '22.' in task:
        query = """
        SELECT country,
            SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN depth_km >= 70 THEN 1 ELSE 0 END), 0) AS shallow_to_deep_ratio
        FROM earthquakes
        GROUP BY country
        ORDER BY shallow_to_deep_ratio DESC
        LIMIT 10;
        """
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '23.' in task:
        query = 'SELECT tsunami, AVG(mag) AS avg_mag FROM earthquakes GROUP BY tsunami;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '24.' in task:
        query = 'SELECT code, place, mag, rms, gap, (rms + gap) AS error_margin FROM earthquakes ORDER BY error_margin DESC LIMIT 10;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '25.' in task:
        query = """
        SELECT e1.code AS eq1_code, e2.code AS eq2_code, e1.time AS eq1_time, e2.time AS eq2_time
        FROM earthquakes e1
        JOIN earthquakes e2 ON e1.time < e2.time
          AND TIMESTAMPDIFF(MINUTE, e1.time, e2.time) <= 60
          AND ABS(e1.latitude - e2.latitude) < 0.5
          AND ABS(e1.longitude - e2.longitude) < 0.5
        LIMIT 10;
        """
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)
    elif '26.' in task:
        query = 'SELECT country, COUNT(*) AS count FROM earthquakes WHERE depth_km >300 GROUP BY country ORDER BY count DESC LIMIT 10;'
        df = pd.read_sql(query, con= engine)
        st.dataframe(df)