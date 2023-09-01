
# Survey Data Analysis and Reporting Tool

## Overview

This Python script is designed to analyze survey data, generate insightful visualizations, and create a PDF report summarizing the findings. It is particularly useful for analyzing employee satisfaction survey data, but it can be adapted for other survey types.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using this code, ensure you have the following prerequisites:

- Python 3.x installed on your system
- Required Python libraries installed. You can install them using `pip`:

   ```
   pip install pandas matplotlib
   ```

## Usage

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/survey-analysis-tool.git
   ```

2. Navigate to the project folder:

   ```
   cd survey-analysis-tool
   ```

3. Place your survey data CSV files in the `DataInput` folder.

4. Open a terminal or command prompt and run the script:

   ```
   python secondSurveyEvaluation.py.py
   ```

5. The script will process the data, generate visualizations, and create a PDF report in the project folder named `Survey_Report_Entire_Tech_September_2023.pdf`.

6. You can customize the script by editing the relevant sections in `survey_analysis.py`.

## File Structure

The project directory is organized as follows:

- `DataInput/`: Place your survey data CSV files in this folder.
- `secondSurveyEvaluation.py`: The main Python script for data analysis and report generation.
- `README.md`: This README file.

## Customization

You can customize the script by making the following changes in `secondSurveyEvaluation.py`:

- Modify the column name mappings in the `numeric_columns_mapping` dictionary to match your survey questions.
- Adjust the formatting and content of the first page text (`firstPageText`) in the `main` function.
- Customize the appearance of visualizations and PDF pages to meet your preferences.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes. We welcome contributions and improvements!

