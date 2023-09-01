# Import necessary libraries
import glob  # For file path globbing
import pandas as pd  # For working with data in DataFrames
import os  # For interacting with the operating system
import matplotlib.pyplot as plt  # For creating plots
import textwrap  # For wrapping text
from matplotlib.backends.backend_pdf import PdfPages  # For creating PDFs

# Function to read the latest CSV file in a specified folder into a DataFrame
def read_csv_to_pandas(folder_path):
    # Find all CSV files in the specified folder and sort them by modification time
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    csv_files.sort(key=lambda x: -os.path.getmtime(x))

    # Check if any CSV files were found
    if not csv_files:
        raise ValueError("No CSV files found in the specified folder.")

    # Get the path of the latest CSV file
    latest_csv_path = csv_files[0]

    # Read the CSV file into a DataFrame
    dataframe = pd.read_csv(latest_csv_path)

    return dataframe

# Function to extract the first character of a cell as an integer
def get_first_char_as_int(cell_value):
    if isinstance(cell_value, str) and len(cell_value) > 0:
        return int(cell_value[0])
    return None  # Specify how to handle empty or invalid values

# Function to prepare data by extracting and converting numeric columns
def dataPreparation(rawDataFrame):
    # Define the columns to extract for numeric data
    columns_to_extract_for_numeric_data_df = ["Recognition and Appreciation (company)", "Recognition and Appreciation (colleagues)", 'Teamwork and Collaboration', 'Skill Utilization', 'Technology and Tools']
    
    # Copy the specified columns
    columns_with_numeric_data = rawDataFrame[columns_to_extract_for_numeric_data_df].copy()

    # Apply the get_first_char_as_int function to convert values to integers
    return columns_with_numeric_data.applymap(get_first_char_as_int)

# Function to split text into paragraphs of a specified maximum width
def split_text(text, max_width):
    # Split the text into individual sentences
    sentences = text.split('. ')
    
    # Initialize the current section of text
    current_section = ""
    
    # List to store the final sections
    final_sections = []
    
    for sentence in sentences:
        # Add the current sentence to the current section
        new_section = f"{current_section}{sentence}. "
        
        # Check if the current section exceeds the maximum width
        if len(new_section) <= max_width:
            current_section = new_section
        else:
            # Add the current section to the list of final sections
            final_sections.append(current_section)
            current_section = f"{sentence}. "
    
    # Add the last section to the list of final sections
    final_sections.append(current_section)
    
    # Join the sections with paragraph breaks
    result = "\n".join(final_sections)
    
    return result

# Function to sort DataFrame columns by median values
def sortByMedian(unsorted_df):
    # Select only numeric columns
    numeric_df = unsorted_df.select_dtypes(include=['number'])

    # Calculate medians for numeric columns
    medians = numeric_df.median()

    # Create a list of column names and their corresponding medians
    median_values = [(col, median) for col, median in medians.items()]

    # Sort the columns by median values in descending order
    sorted_median_values = sorted(median_values, key=lambda x: x[1], reverse=True)

    # Extract the sorted column names
    sorted_columns = [col for col, _ in sorted_median_values]
    
    return numeric_df[sorted_columns]

# Function to visualize and save data as a PDF
def visualize_and_save_as_pdf(firstDataFrame, secondDataFrame, firstPageText, pieData):
    pagesize = (12, 8.27)
    with PdfPages('Survey_Report_Entire_Tech_September_2023.pdf') as pdf:
        # Add text page to PDF
        fig0, ax0 = plt.subplots()
        ax0.text(0.5, 0.5, firstPageText, ha='center', va='center', fontsize=20)
        ax0.axis('off')
        fig0.set_size_inches(pagesize)
        pdf.savefig(fig0)
        plt.close(fig0)

        # Add first pie chart
        team_counts = pieData['Team'].value_counts()
        fig4, ax4 = plt.subplots()
        ax4.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Team', fontweight='bold')
        fig4.set_size_inches(pagesize)
        pdf.savefig(fig4)
        plt.close(fig4)

        # Add second pie chart
        LOE_counts = pieData['Length of employment'].value_counts()
        fig5, ax5 = plt.subplots()
        ax5.pie(LOE_counts, labels=LOE_counts.index, autopct='%1.1f%%', startangle=90)
        ax5.set_title('Length of employment', fontweight='bold')
        fig5.set_size_inches(pagesize)
        pdf.savefig(fig5)
        plt.close(fig5)

        # Add third pie chart
        WL_counts = pieData['Work location'].value_counts()
        fig6, ax6 = plt.subplots()
        ax6.pie(WL_counts, labels=WL_counts.index, autopct='%1.1f%%', startangle=90)
        ax6.set_title('Work location', fontweight='bold')
        fig6.set_size_inches(pagesize)
        pdf.savefig(fig6)
        plt.close(fig6)

        # Add boxplot explanation page to PDF
        boxplotExplanation = 'About Boxplots:\n\nThe Box: The box represents the area where most of the data lies. The lower limit of the box shows the value below which 25% of the data lies. The upper limit of the box shows the value below which 75% of the data lies. This means that most of the scores lie between these two values.\n\nThe orange line in the middle: This is the median. The median is the value that divides the data in half. This means that 50% of the numbers are below this value and 50% are above this value.\n\nThe lines outside the box (the "whiskers"): These lines show how far the data spreads out. They extend to the outermost data points that are not considered "outliers". Outliers are values that are far away from the other values.\n\nPoints outside the whiskers: If there are individual points outside the whiskers, these could be outliers that are much higher or lower than most of the other scores.'
        formatted_text = split_text(boxplotExplanation, 60)
        fig1, ax1 = plt.subplots()
        ax1.text(0.05, 0.95, formatted_text, ha='left', va='top', fontsize=14)
        ax1.axis('off')
        fig1.set_size_inches(pagesize)
        pdf.savefig(fig1)
        plt.close(fig1)

        # Add plot 1 (boxplots for numeric answers) to PDF
        fig2, ax2 = plt.subplots()
        ax2.boxplot(firstDataFrame)
        ax2.set_title("Boxplots for numeric answers (sorted by median)", fontweight='bold')
        max_width = 11
        wrapped_labels = ['\n'.join(textwrap.wrap(label, width=max_width, break_long_words=False)) for label in firstDataFrame.columns]
        ax2.set_xticklabels(wrapped_labels)
        plt.tight_layout()
        fig2.set_size_inches(pagesize)
        pdf.savefig(fig2)
        plt.close(fig2)

        # Add plot 2 (boxplot for NPS) to PDF
        fig3, ax3 = plt.subplots()
        ax3.boxplot(secondDataFrame)
        ax3.set_title("Boxplot for NPS", fontweight='bold')
        ax3.set_xticklabels(secondDataFrame.columns)
        plt.tight_layout()
        fig3.set_size_inches(pagesize)
        pdf.savefig(fig3)
        plt.close(fig3)

# Function to create boxplots for different groups (needs to be modified for PDF creation)
def create_boxplots_for_groups(dataframe, group_column, value_columns):
    grouped = dataframe.groupby(group_column)

    for group_name, group_data in grouped:
        print(group_data)
        sorted_group_data = sortByMedian(group_data)
        fig, ax = plt.subplots()
        data_to_plot = [sorted_group_data[col] for col in value_columns]
        ax.boxplot(data_to_plot, labels=value_columns)
        wrapped_labels = ['\n'.join(textwrap.wrap(label, width=11, break_long_words=False)) for label in value_columns]
        plt.title(f'Boxplots for Team {group_name}', fontweight='bold')
        ax.set_xticklabels(wrapped_labels)
        plt.xticks(range(1, len(value_columns) + 1), wrapped_labels)
        plt.show()

# Main function
def main():
    data_input_folder = 'DataInput'

    # Read CSV data into a DataFrame
    rawDataFrame = read_csv_to_pandas(data_input_folder)

    # Define the text for the first page of the PDF
    firstPageText = f'Tech satisfaction survey\nSeptember 2023\nn = {rawDataFrame.index.size} of ~39'

    # Rename columns for better readability
    numeric_columns_mapping = {
        "How well does the company recognize and value your team's contributions?": "Recognition and Appreciation (company)",
        "How well do the colleagues and managers, you work directly with, recognize and value your contributions?": "Recognition and Appreciation (colleagues)",
        'How would you rate the level of cooperation and teamwork within your team?': 'Teamwork and Collaboration',
        'How well do you feel your skills and expertise are being used in your current project?': 'Skill Utilization',
        'How satisfied are you with the technology and tools provided by the company to do your job?': 'Technology and Tools',
        'How likely is it that you would recommend working at MAYD to a friend?': 'NPS (MAYD Recommendation)',
        'Which team are you on?': 'Team',
        'How long have you been working in this company?': 'Length of employment',
        'Do you work primarily remotely or on-site?': 'Work location'
    }
    
    rawDataFrame.rename(columns=numeric_columns_mapping, inplace=True)

    # Extract data for pie charts
    pieData = rawDataFrame[['Team','Length of employment','Work location']].copy()
    
    # Extract data for NPS (Net Promoter Score) boxplot
    NPS_df = rawDataFrame[['NPS (MAYD Recommendation)']].copy()

    # Prepare numeric data by converting it to integers
    columns_with_numeric_data_int = dataPreparation(rawDataFrame)

    # Sort numeric data columns by median values
    sorted_columns_with_numeric_data_int = sortByMedian(columns_with_numeric_data_int)

    # Visualize and save data as a PDF
    visualize_and_save_as_pdf(sorted_columns_with_numeric_data_int, NPS_df, firstPageText, pieData)

    ############################# Teamevaluation starts ###################################
    columns_with_numeric_data_int['Team'] = rawDataFrame['Team']

    # Call a function to create boxplots for different teams (needs modification for PDF creation)
    # create_boxplots_for_groups(columns_with_numeric_data_int, 'Team', ["Recognition and Appreciation (company)", "Recognition and Appreciation (colleagues)", 'Teamwork and Collaboration', 'Skill Utilization', 'Technology and Tools'])

if __name__ == "__main__":
    main()
