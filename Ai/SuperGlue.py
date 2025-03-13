import subprocess
import webbrowser
import sys
from google import genai
import json
import os
import time


cwd = os.getcwd()
with open(cwd + '/Ai/api.json') as f:
    Api = json.load(f)

API_KEY = Api["Gemini"]

client = genai.Client(api_key=API_KEY)

def prompt_LLM(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    print(f"\nLLM RESPONSE:\n{response.text}")
    return response.text

def read_file(filepath):
    """Reads the contents of a file and returns it as a string."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_script(script, filepath):
    """Writes a script (string) to a file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script)


def run_kowalski(data_csv):
    # Run Kowalsky.py with data.csv as argument
    result = subprocess.run(['python', 'Ai/Kowalski/Kowalski.py', data_csv], capture_output=True, text=True)
    
    # Check if the script ran successfully
    if result.returncode != 0:
        raise Exception(f"Kowalski.py failed with error: {result.stderr}")
    
    # Get the output CSV file path
    csv_output_path = result.stdout.strip()
    return csv_output_path

def run_interpreter(data_bumbuojam, csv_file_path):
    # Run Interpreter.py with data.bumbuojam and the CSV file path as arguments
    result = subprocess.run(['python', 'Ai/Interpreter/Interpreter.py', data_bumbuojam, csv_file_path], capture_output=True, text=True)
    
    # Check if the script ran successfully
    if result.returncode != 0:
        raise Exception(f"Interpreter.py failed with error: {result.stderr}")
    
    # Get the output (two paths separated by newline)
    interpreter_output = result.stdout.strip()
    return interpreter_output

def Cli():
    print(sys.argv)
    if len(sys.argv) != 2:
        data_csv = 'data.csv'
        script_path = 'script.bumbuojam'
    elif len(sys.argv) == 2:
        cwd = os.getcwd()

        Name = sys.argv[1]
        data_csv = cwd + f"/UploadedFiles/{Name}.csv"
        script_path = cwd + f"/Ai/BumbuojamFiles/{Name}.bumbuojam"
        Html = cwd + f"/Ai/VizualizationFiles/{Name}.html"
    else:
        NameCSV = sys.argv[1]
        NameScript = sys.argv[2]
        NameHtml = sys.argv[3]
        


    main(data_csv, script_path)

def Pipeline(data_csv, script_path="script.bumbuojam"):
    main(data_csv, script_path)

def main(data_csv, script_path):
    try:
        time1 = time.time()
        # Step 1: Run Kowalsky.py and get the CSV file path
        kowalski_output = run_kowalski(data_csv)
        time2 = time.time()

        print(f"\nKOWALSKI OUTPUT:\n{kowalski_output}")
        csv_output_path = kowalski_output.split('\n')[0]
        prompt_path = kowalski_output.split('\n')[1]

        print(f"\nRUNNING LLM WITH KOWALSKI PROMPT...\n")
        script = prompt_LLM(read_file(prompt_path))
        time3 = time.time()


        print(f"\nWRITING LLM .BUMBUOJAM SCRIPT TO FILE\n")
        write_script(script, script_path)
        
        # Step 2: Run Interpreter.py with the CSV file path and get the output
        interpreter_output = run_interpreter(script_path, csv_output_path)
        time4 = time.time()

        print(f"\nINTERPRETER_OUTPUT\n{interpreter_output}")
        plot_html_path = interpreter_output.split('\n')[0]
        plot_png_path = interpreter_output.split('\n')[1]

        print(f"""===================\nKOWALSKI TOOK:   {time2-time1} s\nLLM TOOK:        {time3-time2} s\nINTERPRETER TOOK:{time4-time3} s\n===================""")


        # webbrowser.open(plot_html_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    

if __name__ == "__main__":
    Cli()