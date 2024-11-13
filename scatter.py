import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib as mpl
import pandas as pd
from matplotlib.transforms import Bbox

# Edit this to match your own device's file path
file_path = '2018-2019_Daily_Attendance_20240429.csv'
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['Month'] = df['Date'].dt.to_period('M')

monthly_absences = df.groupby(['School DBN', 'Month'])['Absent'].sum().reset_index()

selected_schools = monthly_absences['School DBN'].unique()[:10]
filtered_absences = monthly_absences[monthly_absences['School DBN'].isin(selected_schools)]

fig, ax = plt.subplots(figsize=(12, 6))  # Made figure larger for easier clicking
colors = mpl.colormaps.get_cmap('tab10')

# Dictionary to store scatter plots and their corresponding schools
scatter_plots = {}

# Convert months to numerical values for easier distance calculation
unique_months = filtered_absences['Month'].astype(str).unique()
month_to_num = {month: i for i, month in enumerate(unique_months)}

for i, school in enumerate(selected_schools):
    school_data = filtered_absences[filtered_absences['School DBN'] == school]
    # Use numerical x-values for the scatter plot
    x_values = [month_to_num[str(m)] for m in school_data['Month']]
    scatter = ax.scatter(x_values, 
                        school_data['Absent'], 
                        label=school, 
                        color=colors(i),
                        s=100)  # Made points larger
    scatter_plots[school] = {
        'plot': scatter, 
        'data': school_data,
        'x_values': x_values
    }

def on_click(event):
    if event.inaxes != ax:
        return
        
    x_click, y_click = event.xdata, event.ydata
    
    # Get the display coordinates of the click
    transform = ax.transData.inverted()
    
    # Find the closest point
    min_dist = float('inf')
    closest_point = None
    closest_school = None
    closest_month = None
    
    for school, scatter_data in scatter_plots.items():
        scatter = scatter_data['plot']
        points = scatter.get_offsets()
        
        for point_idx, (x, y) in enumerate(points):
            # Calculate distance in both x and y dimensions
            x_dist = abs(x - x_click)
            y_dist = abs(y - y_click)
            
            # Use a combination of x and y distance for better detection
            dist = np.sqrt(x_dist**2 + (y_dist / ax.get_ylim()[1])**2)
            
            if dist < min_dist:
                min_dist = dist
                closest_point = (x, y)
                closest_school = school
                closest_month = unique_months[int(round(x))]
    
    # Increased threshold for easier clicking
    if min_dist < 0.2:  # Adjusted threshold
        print(f"\nClicked point details:")
        print(f"School: {closest_school}")
        print(f"Month: {closest_month}")
        print(f"Absences: {closest_point[1]:.0f}")
        
        # Highlight the clicked point
        # Remove old highlight if it exists
        if hasattr(ax, 'highlight_point'):
            ax.highlight_point.remove()
        # Add new highlight
        ax.highlight_point = ax.scatter(closest_point[0], closest_point[1], 
                                      s=200, facecolors='none', 
                                      edgecolors='red', linewidth=2)
        plt.draw()
        

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Set up the axis labels using the month strings
ax.set_xticks(range(len(unique_months)))
ax.set_xticklabels(unique_months, rotation=45)

ax.set_title("Monthly Absences for 10 Schools")
ax.set_xlabel("Month")
ax.set_ylabel("Total Absences")
ax.legend(title="School DBN", bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()