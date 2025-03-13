"""
Kowalski's responsibilities:
    * Read files into dataframes
    * Determine what kind of file is uploaded (file extension, maybe how well-structured it is)
    * Convert all files to .csv or return that it's unconvertable
    * Clean the .csv file - turn strings to numerical if they should be numerical, deal with na values, etc.
    * Generate prompt for LLM

    Use:
    python Kowalski.py {data file path}
    Returns:
    {unconvertable} or {clean .csv file path} {prompt .txt file path}
"""
import pandas as pd
import re
import csv
import sys

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# Reads many kinds of files into pandas DataFrames
# Supported formats: txt, csv, json, xls, xlsx, tsv, parquet, xml, html, h5, feather, orc, dta, sav
def read_file(filepath, extension='txt'):
    if extension == 'txt':
        with open(filepath, 'r', encoding="utf-8") as f:
            return f.read()
    elif extension == 'csv':
        return pd.read_csv(filepath)
    elif extension == 'json':
        try:
            return pd.read_json(filepath)
        except ValueError:
            return pd.read_json(filepath, lines=True)
    elif extension in ['xls', 'xlsx']:
        return pd.read_excel(filepath, engine="openpyxl")
    elif extension == 'tsv':
        return pd.read_csv(filepath, sep='\t')
    elif extension == 'parquet':
        return pd.read_parquet(filepath)
    elif extension == 'xml':
        return pd.read_xml(filepath)
    elif extension == 'html':
        return pd.read_html(filepath)[0]  # note: extracts first table
    elif extension == 'h5':
        return pd.read_hdf(filepath)
    elif extension == 'feather':
        return pd.read_feather(filepath)
    elif extension == 'orc':
        return pd.read_orc(filepath)
    elif extension == 'dta':
        return pd.read_stata(filepath)
    elif extension == 'sav':
        return pd.read_spss(filepath)
    else:
        raise ValueError(f"Unsupported file type: {extension}")
# Returns the extension of file
def get_extension(filepath):
    parts = filepath.split(".")
    return parts[len(parts)-1]
# Converts dataframe to .csv file for writing
def convert_to_csv(file):
    try:
        if isinstance(file, pd.DataFrame):
            return file.to_csv()
    except Exception as e:
        return "unconvertable"
# Saves .csv after cleaning
def save_file(file, filepath):
    with open(filepath, "w") as f:
        f.write(file)
    return
def clean_currency(x):
    """Convert currency strings to numbers."""
    if isinstance(x, str):
        try:
            # Remove currency symbols, commas and convert to float
            return float(re.sub(r'[^\d.-]', '', x))
        except:
            return x
    return x
def clean_percentage(x):
    """Convert percentage strings to numbers."""
    if isinstance(x, str) and '%' in x:
        try:
            # Remove % sign and convert to float
            return float(re.sub(r'[^\d.-]', '', x))
        except:
            return x
    return x
# Cleans dataframe (converts currency and percentage strings to numbers, fills NaN values)
def clean_dataframe(df):
    """
    Clean the DataFrame by:
    - Converting currency strings to numeric
    - Converting percentage strings to numeric
    - Handling NaN values
    """
    try:
        # Make a copy to avoid modifying the original
        df_clean = df.copy()
        
        # Process each column
        for col in df_clean.columns:
            try:
                # Skip if column is empty
                if df_clean[col].isna().all():
                    continue
                
                # Get non-NA string values for pattern detection
                sample_values = df_clean[col].dropna().astype(str)
                
                # Skip if no values to process
                if len(sample_values) == 0:
                    continue
                
                # Check for currency pattern
                if sample_values.str.contains(r'^\s*[$£€¥]').any() or sample_values.str.contains(r',\d{3}').any():
                    df_clean[col] = df_clean[col].apply(clean_currency)
                    
                # Check for percentage pattern
                elif sample_values.str.contains('%').any():
                    df_clean[col] = df_clean[col].apply(clean_percentage)
                
                # Try to convert to numeric if possible
                if not pd.api.types.is_numeric_dtype(df_clean[col]):
                    try:
                        numeric_col = pd.to_numeric(df_clean[col], errors='coerce')
                        # If most values convert successfully, use numeric version
                        if numeric_col.notna().sum() > df_clean[col].notna().sum() * 0.8:
                            df_clean[col] = numeric_col
                    except:
                        pass
            except Exception as e:
                # If any column processing fails, just keep the original column
                print(f"Could not process column {col}: {str(e)}")
                continue
        
        # Basic NA handling - fill numeric with 0, others with 'Unknown'
        for col in df_clean.columns:
            try:
                if df_clean[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df_clean[col]):
                        df_clean[col] = df_clean[col].fillna(0)
                    else:
                        df_clean[col] = df_clean[col].fillna('Unknown')
            except:
                # If filling fails, just continue
                continue
                
        return df_clean
    
    except Exception as e:
        print(f"Error in clean_dataframe: {str(e)}")
        # If cleaning fails, return original dataframe
        return df
    
# Deepseek's implementation of the clean_dataframe function, no time to check this, but it may be better than default
def clean_dataframe_deepseek(df):
    """
    Clean the DataFrame by:
    - Converting currency strings to numeric
    - Converting percentage strings to numeric
    - Handling NaN values
    - Removing extra whitespace
    - Standardizing date formats
    - Removing duplicate rows
    - Converting categorical data to lowercase
    """
    try:
        # Make a copy to avoid modifying the original
        df_clean = df.copy()
        
        # Process each column
        for col in df_clean.columns:
            try:
                # Skip if column is empty
                if df_clean[col].isna().all():
                    continue
                
                # Remove extra whitespace from string columns
                if df_clean[col].dtype == 'object':
                    df_clean[col] = df_clean[col].str.strip()
                
                # Get non-NA string values for pattern detection
                sample_values = df_clean[col].dropna().astype(str)
                
                # Skip if no values to process
                if len(sample_values) == 0:
                    continue
                
                # Check for currency pattern
                if sample_values.str.contains(r'^\s*[$£€¥]').any() or sample_values.str.contains(r',\d{3}').any():
                    df_clean[col] = df_clean[col].apply(clean_currency)
                    
                # Check for percentage pattern
                elif sample_values.str.contains('%').any():
                    df_clean[col] = df_clean[col].apply(clean_percentage)
                
                # Check for date pattern
                elif sample_values.str.match(r'\d{2}/\d{2}/\d{4}').any() or sample_values.str.match(r'\d{4}-\d{2}-\d{2}').any():
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                
                # Try to convert to numeric if possible
                if not pd.api.types.is_numeric_dtype(df_clean[col]):
                    try:
                        numeric_col = pd.to_numeric(df_clean[col], errors='coerce')
                        # If most values convert successfully, use numeric version
                        if numeric_col.notna().sum() > df_clean[col].notna().sum() * 0.8:
                            df_clean[col] = numeric_col
                    except:
                        pass
            except Exception as e:
                # If any column processing fails, just keep the original column
                print(f"Could not process column {col}: {str(e)}")
                continue
        
        # Basic NA handling - fill numeric with 0, others with 'Unknown'
        for col in df_clean.columns:
            try:
                if df_clean[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df_clean[col]):
                        df_clean[col] = df_clean[col].fillna(0)
                    else:
                        df_clean[col] = df_clean[col].fillna('Unknown')
            except:
                # If filling fails, just continue
                continue
        
        # Remove duplicate rows
        df_clean = df_clean.drop_duplicates()
        
        # Convert categorical data to lowercase
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].str.lower()
                
        return df_clean
    
    except Exception as e:
        print(f"Error in clean_dataframe: {str(e)}")
        # If cleaning fails, return original dataframe
        return df

# Creates summary of clean dataframe (or .csv, same thing basically)
def summarize_dataframe(df):
    """
    Generate a simple summary of the DataFrame.
    """
    try:
        summary = []
        
        # Basic DataFrame info
        summary.append(f"Dataset Overview:")
        summary.append(f"- Total rows: {df.shape[0]}")
        summary.append(f"- Total columns: {df.shape[1]}")
        summary.append("\nColumn Analysis:")
        
        # Analyze each column
        for col in df.columns:
            try:
                summary.append(f"\n## Column: {col}")
                
                # Data type
                dtype = df[col].dtype
                summary.append(f"- Data type: {dtype}")
                
                # Missing values
                missing = df[col].isna().sum()
                missing_percent = (missing / len(df)) * 100 if len(df) > 0 else 0
                summary.append(f"- Missing values: {missing} ({missing_percent:.2f}%)")
                
                # Skip empty columns
                if missing == len(df):
                    summary.append("- Column is empty")
                    continue
                
                # For numeric columns, add basic stats
                if pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        summary.append(f"- Min: {df[col].min()}")
                        summary.append(f"- Max: {df[col].max()}")
                        summary.append(f"- Mean: {df[col].mean():.2f}")
                    except:
                        summary.append("- Could not calculate numeric statistics")
                
                # For other columns, show unique values count
                else:
                    try:
                        unique_count = df[col].nunique()
                        summary.append(f"- Unique values: {unique_count}")
                        
                        # If few unique values, show distribution
                        if 0 < unique_count <= 5:
                            summary.append("- Value distribution:")
                            value_counts = df[col].value_counts().nlargest(5)
                            for value, count in value_counts.items():
                                percent = (count / df[col].count()) * 100 if df[col].count() > 0 else 0
                                summary.append(f"  * {value}: {count} ({percent:.2f}%)")
                    except:
                        summary.append("- Could not analyze categorical values")
            
            except Exception as e:
                summary.append(f"- Error analyzing column: {str(e)}")
                continue
        
    except Exception as e:
        print(f"Error in summarize_dataframe: {str(e)}")
        return "Could not generate summary due to an error."

    return "\n".join(summary)
# Generates final prompt
def generate_prompt(csv_summary, base_prompt):
    return base_prompt + csv_summary

def main():

    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python Kowalski.py {.bumbuojam path} {data file path}")
        sys.exit(1)

    # Filepath
    base_prompt_filepath = dir_path + "/base_prompt.txt" # hard-coded path to 
    # Filepaths from command-line arguments
    data_filepath = sys.argv[1]  # Path to data file

    input_extension = get_extension(data_filepath)

    import os
    cwd = os.getcwd()

    name = data_filepath.split(".")[-2].split("/")[-1]

    # Returned paths
    cleaned_csv_filepath = cwd + f"/Ai/CleanedData/{name}_cleaned_data.csv" # automatically generated
    prompt_filepath = cwd + f"/Ai/CleanedData/{name}_prompt.txt"          # automatically generated

    # Read files and convert to .csv
    extension = get_extension(data_filepath)
    file = read_file(data_filepath, extension)
    base_prompt = read_file(base_prompt_filepath)

    # Clean files and save them
    cleaned_file = clean_dataframe_deepseek(file)
    file_summary = summarize_dataframe(cleaned_file)
    save_file(convert_to_csv(cleaned_file), cleaned_csv_filepath)

    # Combine base prompt with file summary to get final prompt
    prompt = generate_prompt(file_summary, base_prompt)
    save_file(prompt, prompt_filepath)

    #
    #   FOR DEBUG
    #
    #print(prompt)

    print(f"{cleaned_csv_filepath}\n{prompt_filepath}")
    return cleaned_csv_filepath, prompt_filepath

main()
