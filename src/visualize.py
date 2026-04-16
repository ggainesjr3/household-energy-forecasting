import pandas as pd
import matplotlib.pyplot as plt
from preprocess import load_and_clean_data # Importing your previous logic

def create_comparison_plot(df, df_hourly):
    # Grab one day of data (1440 mins vs 24 hours)
    one_day_min = df.iloc[:1440] 
    one_day_hour = df_hourly.iloc[:24]

    plt.figure(figsize=(12, 8))

    # Plot 1: The Raw Signal (High Frequency)
    plt.subplot(2, 1, 1)
    plt.plot(one_day_min['Global_active_power'], color='#e74c3c', alpha=0.6)
    plt.title('Minute-by-Minute: The "Noisy" Raw Signal')
    plt.ylabel('Kilowatts')

    # Plot 2: The Integrated Signal (Low Frequency)
    plt.subplot(2, 1, 2)
    plt.plot(one_day_hour['Global_active_power'], color='#3498db', linewidth=2)
    plt.title('Hourly Resampled: The "Clean" Trend')
    plt.ylabel('Kilowatts')

    plt.tight_layout()
    
    # Save the plot so you can view it even if you're in a headless terminal
    plt.savefig('comparison_plot.png')
    print("Plot saved as comparison_plot.png")
    
    # Try to show it (will work if you have a GUI/X11 setup)
    plt.show()

if __name__ == "__main__":
    # Path to your UCI data
    path = 'data/household_power_consumption.txt'
    
    print("Loading data...")
    raw_df = load_and_clean_data(path)
    
    print("Resampling...")
    hourly_df = raw_df.resample('H').mean()
    
    create_comparison_plot(raw_df, hourly_df)