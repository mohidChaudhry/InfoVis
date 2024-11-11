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

absence_pivot = filtered_absences.pivot(index='School DBN', columns='Month', values='Absent').fillna(0)

fig, ax = plt.subplots()
cax = ax.imshow(absence_pivot, aspect='auto', cmap='YlGnBu')

fig.colorbar(cax, ax=ax, label='Total Absences')
ax.set_title("Monthly Absences by Selected 10 Schools")
ax.set_xlabel("Month")
ax.set_ylabel("School")

ax.set_xticks(range(len(absence_pivot.columns)))
ax.set_xticklabels(absence_pivot.columns.astype(str), rotation=45)
ax.set_yticks(range(len(absence_pivot.index)))
ax.set_yticklabels(absence_pivot.index)

fig.tight_layout()
plt.show()