import subprocess
import webbrowser
import sys
from google import genai
API_KEY = 'AIzaSyDDlvzdRBfFmZpP0aXGoGxzXzq3oj-dUvE'

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
    if len(sys.argv) != 2:
        data_csv = 'data.csv'
    else:
        data_csv = sys.argv[1]

    script_path = 'script.bumbuojam'

    main(data_csv, script_path)

def Pipeline(data_csv, script_path="script.bumbuojam"):
    main(data_csv, script_path)

def main(data_csv, script_path):
    try:
        # Step 1: Run Kowalsky.py and get the CSV file path
        kowalski_output = run_kowalski(data_csv)
        print(f"\nKOWALSKI OUTPUT:\n{kowalski_output}")
        csv_output_path = kowalski_output.split('\n')[0]
        prompt_path = kowalski_output.split('\n')[1]

        print(f"\nRUNNING LLM WITH KOWALSKI PROMPT...\n")
        script = prompt_LLM(read_file(prompt_path))

        print(f"\nWRITING LLM .BUMBUOJAM SCRIPT TO FILE\n")
        write_script(script, script_path)
        
        # Step 2: Run Interpreter.py with the CSV file path and get the output
        interpreter_output = run_interpreter(script_path, csv_output_path)
        print(f"\nINTERPRETER_OUTPUT\n{interpreter_output}")
        plot_html_path = interpreter_output.split('\n')[0]
        plot_png_path = interpreter_output.split('\n')[1]

        webbrowser.open(plot_html_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    

if __name__ == "__main__":
    main()