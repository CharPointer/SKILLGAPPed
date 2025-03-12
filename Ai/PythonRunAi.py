import sys
import argparse
from google import generativeai
from llama_cpp import Llama

gemini_version = "gemini-pro"
model_path = "./Ai/Model/DeepSeekTest.gguf"
generativeai.configure(api_key="your-google-api-key")

def load_llama_model(model_path):
    try:
        return Llama(
            model_path,
            n_gpu_layers=-1,  # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            n_ctx=50048,  # Uncomment to increase the context window
            # n_ctx = 131070,
            # verbose=False
        )
    except Exception as e:
        return f"Error loading Llama model: {e}"

def llama_query(llm, prompt):     
    try:
        output = llm(
            prompt, # Prompt
            max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
            stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
            echo=True # Echo the prompt back in the output
        ) # Generate a completion, can also call create_completion
        return output['choices'][0]['text']                   # get llama response
    except Exception as e:
        return f"Error generating response from Llama: {e}"

def gemini_query(prompt):         
    try:
        response = generativeai.generate_text(prompt, gemini_version)
        return response.text
    except Exception as e:
        return f"Error generating response from Gemini: {e}"  # get gemini response

def promptAI(args):
    if args.WhichAi == "llama":                   # load llama model
        llm = load_llama_model(model_path)
        if isinstance(llm, str):
            return llm
        response = llama_query(llm, args.Prompt)  # get llama response
    elif args.WhichAi == gemini_version:          # load gemini model
        response = gemini_query(args.Prompt)      # get gemini response
    else:
        return "Error: Unsupported AI model."
    return response

def main():
    parser = argparse.ArgumentParser(description="AI Prompt")
    parser.add_argument('-WhichAi', type=str, required=True, help=f"Choose AI model (llama or {gemini_version})")
    parser.add_argument('-Prompt', type=str, required=True, help="Provide the prompt for the chosen AI")

    args = parser.parse_args()

    # Example command line call:
    # python ./Ai/PythonRunAi.py -WhichAi llama -Prompt "What is 2+2?"

    response = promptAI(args)
    print(response)

if __name__ == '__main__':
    main()