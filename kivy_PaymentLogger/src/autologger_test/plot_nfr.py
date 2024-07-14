import pandas as pd
import matplotlib.pyplot as plt

def plot_data(csv_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter out rows with placeholders or missing data if any
    df = df[df['L_mean'] != '-']
    
    # Convert data to appropriate types
    df['Ordinal'] = df['Ordinal'].astype(int)
    df['L_mean'] = df['L_mean'].astype(float)
    df['L_std_dev'] = df['L_std_dev'].astype(float)
    
    # Create a plot with two series on the same graph
    fig, ax1 = plt.subplots(figsize=(16, 10))

    # Plotting L_mean vs Ordinal
    color = 'tab:red'
    ax1.set_xlabel('Ordinal (count of concurrent asynchronous load of message)')
    ax1.set_ylabel('L_mean (mean latency delay in seconds)', color=color)
    mean_line, = ax1.plot(df['Ordinal'], df['L_mean'], color=color, label='Mean Latency Delay')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Mark extrema for L_mean
    mean_max = df.loc[df['L_mean'].idxmax()]
    mean_min = df.loc[df['L_mean'].idxmin()]
    ax1.scatter([mean_max['Ordinal'], mean_min['Ordinal']], [mean_max['L_mean'], mean_min['L_mean']], color='darkred')

    # Create a second y-axis to plot L_std_dev
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('L_std_dev (Jitter, standard deviation of latency delay in seconds)', color=color)
    std_dev_line, = ax2.plot(df['Ordinal'], df['L_std_dev'], color=color, label='Jitter (Standard Deviation)')
    ax2.tick_params(axis='y', labelcolor=color)

    # Mark extrema for L_std_dev
    std_dev_max = df.loc[df['L_std_dev'].idxmax()]
    std_dev_min = df.loc[df['L_std_dev'].idxmin()]
    ax2.scatter([std_dev_max['Ordinal'], std_dev_min['Ordinal']], [std_dev_max['L_std_dev'], std_dev_min['L_std_dev']], color='darkblue')

    # Add grid, legend, and title
    ax1.grid(True)
    fig.legend(handles=[mean_line, std_dev_line], loc='upper left')
    plt.title('Mean Latency Delay and Jitter vs Ordinal')
    plt.suptitle('This plot shows how the mean latency delay and its variability (jitter) change with the number of concurrent message loads.')

    # Tight layout to adjust for subtitle
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot to a file
    plt.savefig('latency_analysis.png')
    plt.show()

if __name__ == "__main__":
    # Take the CSV filepath as an input
    csv_file = input("Enter the path to the CSV file: ")
    plot_data(csv_file)
