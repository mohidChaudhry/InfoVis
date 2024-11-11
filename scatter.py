import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl
import pandas as pd

# Edit this to match your own device's file path
file_path = '2018-2019_Daily_Attendance_20240429.csv'
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['Month'] = df['Date'].dt.to_period('M')

monthly_absences = df.groupby(['School DBN', 'Month'])['Absent'].sum().reset_index()

selected_schools = monthly_absences['School DBN'].unique()[:10]
filtered_absences = monthly_absences[monthly_absences['School DBN'].isin(selected_schools)]

fig, ax = plt.subplots()

colors = mpl.colormaps.get_cmap('tab10')

for i, school in enumerate(selected_schools):
    school_data = filtered_absences[filtered_absences['School DBN'] == school]
    ax.scatter(school_data['Month'].astype(str), school_data['Absent'], label=school, color=colors(i))

ax.set_title("Monthly Absences for 10 Schools")
ax.set_xlabel("Month")
ax.set_ylabel("Total Absences")
ax.legend(title="School DBN", bbox_to_anchor=(1, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()