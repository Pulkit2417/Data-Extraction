### Data Extraction and Transformation from PDF to Excel

## Introduction

This project involves developing a solution to extract data from a PDF file containing electoral roll data and format it into a specified Excel layout. The goal was to create a robust Python-based solution capable of accurately parsing the PDF, processing the extracted information, and delivering it in the required Excel format. The solution utilizes Python libraries, including google.generativeai, pdf2image, and pandas.

## Problem Breakdown

The task involved working with a PDF file that contained the electoral roll data of 30 individuals, some of whom were marked as deleted. The objective was to extract the details of the individuals not marked as deleted and organize them in a structured format consistent with a provided sample Excel file.

## Solution Approach

# 1. PDF Text Extraction
The PDF was first converted into a series of images using the pdf2image library, making it easier to process each page individually. Instead of using traditional Optical Character Recognition (OCR) tools like Tesseract and CV2, Google Generative AI was employed to extract structured data directly from the images. This decision was made because achieving over 90% accuracy with Tesseract and CV2 was challenging due to the lack of sufficient training data.

Google Generative AI provided a reliable method to interpret the text and return the data in a structured format. Each individual’s details, who was not marked as deleted, were structured as Python dictionaries. The dictionaries contained fields such as "Part S.No", "Voter Full Name", "Relative's Name", "Relation Type", "Age", "Gender", "House No", and "EPIC No".

# 2. Data Transformation
The extracted data was converted into a pandas DataFrame, allowing for easier manipulation and formatting to meet the Excel output requirements. A critical step was ensuring that all column names were converted to uppercase, maintaining consistency with the provided sample Excel file.

# 3. Data Formatting and Export
The DataFrame containing the extracted and transformed data was exported to an Excel file (final_output.xlsx) using pandas' to_excel function. This file matched the required format and layout, ensuring the solution met the assignment's criteria.

## Accuracy Verification
To validate the accuracy of the data extraction and transformation process, a comparison was made between the generated final_output.xlsx and the provided Output File.xlsx. The comparison script standardized column names, handled missing values, and normalized text case across both files. Using a merge operation on the EPIC No field, discrepancies between the two files were identified.

The accuracy of the solution was calculated by comparing the rows in both files. If a row matched across all columns, it was considered accurate. The final accuracy achieved by the solution was over 90%, demonstrating the effectiveness of the approach.

## Challenges Faced
Handling Irregularities in Text Extraction: Extracting structured data from images is challenging due to variations in text alignment, font, and other formatting inconsistencies. While traditional OCR methods like Tesseract and CV2 were considered, they were found insufficient for achieving the desired accuracy without extensive training data. Google Generative AI was selected as it provided a more accurate and reliable method for parsing the image content.

Ensuring Data Consistency: Converting the extracted data into a consistent format that aligned with the provided Excel file required careful handling of text cases, missing values, and column names. These challenges were addressed by implementing robust data cleaning and transformation steps.

## Conclusion
The solution successfully extracted and transformed the required data from the PDF file into an Excel format with high accuracy. The use of Google Generative AI, in conjunction with other Python libraries, proved to be an effective strategy for tackling the problem. This approach can be further refined by improving the text extraction logic and handling edge cases more effectively.

## Code
The complete code for this solution is available in this repository.
