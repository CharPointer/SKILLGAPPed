"""
Kowalski's responsibilities:
    * Read files into dataframes
    * Determine what kind of file is uploaded
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
    with open(filepath, "w",  newline='') as f:
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
    
def clean_dataframe(df):
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
    """Generate a focused summary of the DataFrame for plotting."""
    try:
        summary = []
        
        # Basic DataFrame info
        summary.append(f"Dataset Overview:")
        summary.append(f"- Total rows: {df.shape[0]}")
        summary.append(f"- Total columns: {df.shape[1]}")
        
        # Add only the most significant correlations
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr().round(2)
            # Find top 3 strongest correlations only
            corr_pairs = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    corr = corr_matrix.loc[col1, col2]
                    if abs(corr) > 0.5:  # Only include meaningful correlations
                        corr_pairs.append((col1, col2, corr))
            
            if corr_pairs:
                top_pairs = sorted(corr_pairs, key=lambda x: abs(x[2]), reverse=True)[:3]
                summary.append("\nStrong correlations:")
                for col1, col2, corr in top_pairs:
                    summary.append(f"- {col1} and {col2}: {corr:.2f}")
        
        summary.append("\nColumn Analysis:")
        
        # Analyze each column with focused statistics
        for col in df.columns:
            try:
                summary.append(f"\n## Column: {col}")
                dtype = df[col].dtype
                summary.append(f"- Data type: {dtype}")
                
                # Missing values
                missing = df[col].isna().sum()
                if missing > 0:
                    missing_percent = (missing / len(df)) * 100
                    summary.append(f"- Missing values: {missing} ({missing_percent:.1f}%)")
                
                # For numeric columns, add only key stats
                if pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        summary.append(f"- Range: {df[col].min()} to {df[col].max()}")
                        summary.append(f"- Mean: {df[col].mean():.2f}, Median: {df[col].median():.2f}")
                        
                        # Only add distribution hint if it seems important
                        if abs(df[col].skew()) > 1:
                            summary.append(f"- Note: Distribution is skewed ({df[col].skew():.1f})")
                    except:
                        pass
                
                # For datetime columns - just range
                elif pd.api.types.is_datetime64_dtype(df[col]):
                    summary.append(f"- Date range: {df[col].min().date()} to {df[col].max().date()}")
                
                # For categorical, focus on dominance
                elif df[col].dtype == 'object':
                    unique_count = df[col].nunique()
                    summary.append(f"- Unique values: {unique_count}")
                    
                    # Only show distribution if there's a clear dominant category
                    if 0 < unique_count <= 10:
                        top_value = df[col].value_counts().nlargest(1)
                        top_pct = (top_value.iloc[0] / df[col].count()) * 100
                        if top_pct > 50:
                            summary.append(f"- Dominant value: {top_value.index[0]} ({top_pct:.1f}%)")
                    
            except Exception as e:
                continue
        
    except Exception as e:
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
    cleaned_file = clean_dataframe(file)
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
