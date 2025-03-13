import sys
import torch
import base64
import argparse
from google import genai
from llama_cpp import Llama
import PIL.Image

from llama_cpp import Llama

llm = Llama.from_pretrained(
	repo_id="FiditeNemini/Llama-3.1-Unhinged-Vision-8B-GGUF",
	filename="Llama-3.1-Unhinged-Vision-8B-q8_0.gguf",
    verbose=True,
    n_gpu_layers =-1,
    n_ctx = 256
)

def image_to_base64_data_uri(file_path):
    with open(file_path, "rb") as img_file:
        base64_data = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_data}"

def LamaVision_query(text_prompt, image_path):
    image_data_uri = image_to_base64_data_uri(image_path)
    prompt = {
        "image": image_data_uri,
        "text": text_prompt
    }
    response = llm(
        "Q: " + prompt["text"]  + ". A: ",
        max_tokens=256,
        stop=["\n"],
        echo=True
        )
    return response

gemini_version = "gemini-pro"
model_id = r"D:\Nauji reikalai\SKILLGAPPed\Ai\Model\Lama3V.gguf"#"./../Model/Lama3V.gguf"
client = genai.Client(api_key="AIzaSyDDlvzdRBfFmZpP0aXGoGxzXzq3oj-dUvE")

def gemini_query(prompt, image):      
    try:
        return client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, image])
    except Exception as e:
        return f"Error generating response from Gemini: {e}"  # get gemini response

def promptAI(WhichAi, Prompt, PhotoPath):
    main(WhichAi, Prompt, PhotoPath)

def PrePars():
    try:
        parser = argparse.ArgumentParser(description="AI Prompt")
        parser.add_argument('-WhichAi', type=str, required=True, help=f"Choose AI model (llama or {gemini_version})")
        parser.add_argument('-PhotoPath', type=str, required=True, help="Provide photo location in computer")
        args = parser.parse_args()
        response = main(args.WhichAi, args.Prompt, args.PhotoPath)
        print(response)
    except:
        print("Error")
        main("lama","check","Ai\VisualChecker\Graph.jpg")

def main(WhichAi, Prompt, PhotoPath):
    if WhichAi == gemini_version:          # load gemini model
        response = gemini_query(Prompt, PIL.Image.open())      # get gemini response
    elif WhichAi == "lama":
         print("check lama")
         response = LamaVision_query(Prompt, PhotoPath)      # get lama response
         print(response)
    else:
        return "Error: Unsupported AI model."
    return response

if __name__ == '__main__':
    PrePars()