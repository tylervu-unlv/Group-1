from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from collections import defaultdict
import numpy as np

def parse_csv_file(filepath):
    """
    Reads the authors_file_touches CSV file and extracts relevant data.
    """
    files_data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                files_data.append({
                    'filepath': row['File Path'],
                    'authors': row['Authors'].split('; ') if row['Authors'] != 'Unknown' else [],
                    'all_dates': row['All Change Dates'].split('; ') if row['All Change Dates'] != 'Unknown' else [],
                    'first_date': row['First Change Date'],
                    'last_date': row['Last Change Date'],
                    'touches': int(row['Number of Touches'])
                })
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    return files_data

def calculate_weeks_since_start(date_str, repo_start_date):
    """
    Calculates the number of weeks between repo start date and given date.
    """
    try:
        # Parse date strings (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
        date_str = date_str.split('T')[0] if 'T' in date_str else date_str
        date = datetime.strptime(date_str, '%Y-%m-%d')
        start = datetime.strptime(repo_start_date, '%Y-%m-%d')
        
        delta = date - start
        weeks = delta.days / 7.0
        return weeks
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return None

def create_scatter_plot(files_data):
    """
    Creates a scatter plot visualization of file activity over time.
    X-axis: weeks since repository start
    Y-axis: source files
    Color: author
    """
    
    if not files_data:
        print("No data to plot")
        return
    
    # Find the earliest date (repository start)
    earliest_date = None
    for file_info in files_data:
        if file_info['first_date'] and file_info['first_date'] != 'Unknown':
            date_str = file_info['first_date'].split('T')[0] if 'T' in file_info['first_date'] else file_info['first_date']
            if earliest_date is None:
                earliest_date = date_str
            else:
                earliest_date = min(earliest_date, date_str)
    
    if not earliest_date:
        print("Could not determine repository start date")
        return
    
    print(f"Repository start date: {earliest_date}")
    
    # Collect all unique authors and assign colors
    all_authors = set()
    for file_info in files_data:
        all_authors.update(file_info['authors'])
    
    all_authors = sorted(list(all_authors))
    print(f"Total unique authors: {len(all_authors)}")
    
    # Create color map for authors
    colors = plt.cm.tab20c(np.linspace(0, 1, len(all_authors)))
    if len(all_authors) > 20:
        colors = plt.cm.hsv(np.linspace(0, 1, len(all_authors)))
    
    author_colors = {author: colors[i] for i, author in enumerate(all_authors)}
    
    # Create file to y-axis mapping
    file_to_y = {file_info['filepath']: i for i, file_info in enumerate(files_data)}
    
    # Prepare plot data
    x_values = []
    y_values = []
    point_colors = []
    point_authors = []
    
    # Collect all data points
    for file_info in files_data:
        filepath = file_info['filepath']
        y_pos = file_to_y[filepath]
        
        # For each date when this file was changed
        for date_str in file_info['all_dates']:
            if date_str and date_str != 'Unknown':
                weeks = calculate_weeks_since_start(date_str, earliest_date)
                if weeks is not None:
                    # Find which author made changes around this date
                    # For simplicity, we'll distribute changes among all authors who touched the file
                    for author in file_info['authors']:
                        if author in author_colors:
                            x_values.append(weeks)
                            y_values.append(y_pos)
                            point_colors.append(author_colors[author])
                            point_authors.append(author)
    
    if not x_values:
        print("No data points to plot")
        return
    
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(16, 12))
    
    scatter = ax.scatter(x_values, y_values, c=point_colors, s=60, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Set labels and title
    ax.set_xlabel('Weeks Since Repository Start', fontsize=12, fontweight='bold')
    ax.set_ylabel('Source Files', fontsize=12, fontweight='bold')
    ax.set_title('Repository File Activity Over Time\n(Color represents author)', fontsize=14, fontweight='bold')
    
    # Set y-axis to show file names
    if len(files_data) <= 50:
        ax.set_yticks(range(len(files_data)))
        ax.set_yticklabels([file_info['filepath'] for file_info in files_data], fontsize=8)
    else:
        # For large number of files, show only some labels
        step = max(1, len(files_data) // 30)
        ax.set_yticks(range(0, len(files_data), step))
        ax.set_yticklabels([files_data[i]['filepath'] for i in range(0, len(files_data), step)], fontsize=8)
    
    # Create legend for authors
    legend_elements = [mpatches.Patch(facecolor=author_colors[author], edgecolor='black', label=author) 
                       for author in all_authors]
    
    # Place legend outside the plot if there are many authors
    if len(all_authors) > 15:
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8, ncol=1)
    else:
        ax.legend(handles=legend_elements, loc='best', fontsize=9)
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure
    output_path = 'FinnWant_file_activity.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Scatter plot saved to: {output_path}")
    
    # Display plot statistics
    print(f"\nPlot Statistics:")
    print(f"  - Total data points: {len(x_values)}")
    print(f"  - Files displayed: {len(files_data)}")
    print(f"  - Authors represented: {len(all_authors)}")
    print(f"  - Time span: {min(x_values):.1f} to {max(x_values):.1f} weeks")
    
    plt.show()

def main():
    # GitHub repo (must match what was used in FinnWant_collect_files.py)
    repo = 'scottyab/rootbeer'
    # repo = 'Skyscanner/backpack'
    # repo = 'k9mail/k-9'
    # repo = 'mendhak/gpslogger'
    
    file = repo.split('/')[1]
    
    # Read the CSV file generated by FinnWant_authors_file_touches.py
    input_file = f'data/authors_file_touches_{file}.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        print("Please run FinnWant_authors_file_touches.py first to generate the author data.")
        return
    
    print(f"Reading file activity data from {input_file}...")
    files_data = parse_csv_file(input_file)
    
    if files_data:
        print(f"Successfully loaded {len(files_data)} files with author and date information.")
        create_scatter_plot(files_data)
    else:
        print("Failed to load data from CSV file.")

if __name__ == "__main__":
    main()
