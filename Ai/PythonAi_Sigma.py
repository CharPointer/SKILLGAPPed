import sys
import argparse
from google import genai
import os
cwd = os.getcwd()
gemini_version = "gemini"
client = genai.Client(api_key="AIzaSyBNMG2PVxAhrpTdRQAD2qzo8AFyrIRVPuc")


def llama_cpp(text_prompt):
    from llama_cpp import Llama

    model_path = cwd + "/Ai/Model/llama3.gguf"
    
    llm = Llama(
    	model_path,
        verbose=True,
        chat_format="llama-3",
        n_gpu_layers =-1,
        n_ctx = 2512
    )
    response = llm.create_chat_completion(
        seed=-1,
        messages = [
        {"role": "system", "content": "You are an assistant who perfectly does what he is asked by user, without any errors and nothing more."},
        {
            "role": "user",
            "content": text_prompt
        }
      ],
    )
    return response["choices"][0]["message"]["content"]

def gemini_query(prompt):      
    try:
        # print(prompt)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
        text = response.text
        return text
    except Exception as e:
        print(f"Error generating response from Gemini: {e}" ) # get gemini response
        return "Exhausted API change it/wait"

def promptAI(WhichAi, Prompt):
    main(WhichAi, Prompt)

def PrePars():
    # try:
        # parser = argparse.ArgumentParser(description="AI Prompt")
        # parser.add_argument('-WhichAi', type=str, required=True, help=f"Choose AI model (llama or {gemini_version})")
        # parser.add_argument('-Prompt', type=str, required=True, help=f"Prompt")
        # args = parser.parse_args()

        WhichAi = sys.argv[1]
        Prompt = sys.argv[2]
        # print(WhichAi + Prompt)
        response = main(WhichAi, Prompt)
        print("Response: "+ response)
    # except:
    #     print("Error")
    #     main("gemini-pro","Q:How many strawberries in r?")

def main(WhichAi, Prompt):
    if WhichAi == gemini_version:          # load gemini model
        response = gemini_query(Prompt)      # get gemini response
        # print(response)
    elif WhichAi == "lama":
        response = llama_cpp(Prompt)
        #  response = LamaVision_query(Prompt)      # get lama response
    else:
        return "Error: Unsupported AI model."
    return response

if __name__ == '__main__':
    PrePars()