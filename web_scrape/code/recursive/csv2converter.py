import argparse
import pandas as pd
from docx import Document
import os

def read_csv_and_write_to_docx(csv_filename, output_dir):
    """
    Read the 'text' column from a CSV file and write each row's text into a separate .docx file.

    Args:
    csv_filename (str): The path to the CSV file.
    output_dir (str): The directory where the .docx files will be saved.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the CSV file
    df = pd.read_csv(csv_filename)
    
    # Iterate through each row and create a .docx file
    for index, row in df.iterrows():
        text = row['text']
        doc = Document()
        doc.add_paragraph(text)
        
        # Define the output file path
        output_filename = os.path.join(output_dir, f'document_{index + 1}.docx')
        doc.save(output_filename)
        print(f"Saved {output_filename}")

def read_csv_and_write_to_csv(csv_filename, output_dir):
    """
    Read the 'text' column from a CSV file, split each row's text into paragraphs, 
    and write the modified text into a new CSV file.

    Args:
    csv_filename (str): The path to the input CSV file.
    output_dir (str): The directory where the output CSV file will be saved.
    output_csv_filename (str): The name of the output CSV file.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the input CSV file
    df = pd.read_csv(csv_filename)

    for index, row in df.iterrows():
        # print(row)
        text = pd.DataFrame({"text": [row['text']]})

        # Define the output file path
        output_csv_path = os.path.join(output_dir, f'document_{index + 1}.csv')
        
        # Write the modified DataFrame to a new CSV file
        text.to_csv(output_csv_path, index=False, header=False)

def read_csv_and_write_to_txt(csv_filename, output_dir):
    """
    Read the 'text' column from a CSV file, split each row's text into paragraphs,
    and write the modified text into separate .txt files.

    Args:
    csv_filename (str): The path to the input CSV file.
    output_dir (str): The directory where the .txt files will be saved.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the input CSV file
    df = pd.read_csv(csv_filename)

    for index, row in df.iterrows():
        text = row['text']
        
        # Split text into paragraphs
        paragraphs = text.split('.')
        paragraphs = [paragraph.strip() + '.' for paragraph in paragraphs if paragraph.strip()]
        formatted_text = '\n\n'.join(paragraphs)
        
        # Define the output file path
        output_txt_path = os.path.join(output_dir, f'document_{index + 1}.txt')
        
        # Write the modified text to a new .txt file
        with open(output_txt_path, 'w') as file:
            file.write(formatted_text)
        
        print(f"Saved {output_txt_path}")



def main():
    parser = argparse.ArgumentParser(description='convert csv to docx')
    parser.add_argument('--csv_filepath', type=str, help='path to csv')
    parser.add_argument('--output_dir', type=str, help='path to save docx', default=2)
    args = parser.parse_args()

    read_csv_and_write_to_txt(args.csv_filepath, args.output_dir)

# Run the main function
if __name__ == "__main__":   
    main()