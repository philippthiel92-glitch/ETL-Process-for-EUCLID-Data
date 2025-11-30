# EBA Euclid Register – JSON to CSV Conversion for Tableau

In this project, I download the official EBA Euclid Register file from the following source:

> https://euclid.eba.europa.eu/register/pir/registerDownload

The file is provided in **JSON format** and contains structured information on supervised institutions.

## Purpose

The goal of this project is to convert the JSON file into a **clean, structured CSV format**, which can then be easily imported and visualized in **Tableau**.

## Process

1. **Download the JSON File**  
   - Retrieve the current register file from the URL above  
   - Save it locally (e.g., as `eba_register.json`)

2. **Transform JSON → CSV**  
   - Load and parse the JSON file  
   - Extract relevant fields (e.g., identifiers, countries, categories, status)  
   - Restructure the data into a tabular format (rows = entries, columns = attributes)  
   - Export the cleaned dataset as `eba_register_clean.csv`

3. **Visualization in Tableau**  
   - Import the CSV file into Tableau  
   - Build dashboards and visualizations (e.g., number of institutions per country, category distributions, time-based trends)

## Technologies

- Data transformation: Python (pandas) or any other tool capable of processing JSON  
- Visualization: Tableau

## Benefit

By converting the JSON file into a structured CSV, the Euclid dataset becomes directly usable for **interactive analysis and visualization** in Tableau, enabling clear insights into regulatory and supervisory information.
