import sys
import argparse
from google import genai
# from llama_cpp import Llama

gemini_version = "gemini-pro"
model_path = "Ai\Model\fakemodel.gguf"
client = genai.Client(api_key="AIzaSyDDlvzdRBfFmZpP0aXGoGxzXzq3oj-dUvE")

# llm = Llama.from_pretrained(
# 	repo_id="FiditeNemini/Llama-3.1-Unhinged-Vision-8B-GGUF",
# 	filename="Llama-3.1-Unhinged-Vision-8B-q8_0.gguf",
#     verbose=True,
#     n_gpu_layers =-1,
#     n_ctx = 256
# )

# def LamaVision_query(text_prompt):
#     prompt = {
#         "text": text_prompt
#     }
#     response = llm(
#         "Q: " + prompt["text"]  + ". A: ",
#         max_tokens=256,
#         stop=["\n"],
#         echo=True
#         )
#     return response

def gemini_query(prompt):      
    try:
        print(prompt)
        return client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
    except Exception as e:
        return f"Error generating response from Gemini: {e}"  # get gemini response

def promptAI(WhichAi, Prompt):
    main(WhichAi, Prompt)

def PrePars():
    try:
        parser = argparse.ArgumentParser(description="AI Prompt")
        parser.add_argument('-WhichAi', type=str, required=True, help=f"Choose AI model (llama or {gemini_version})")
        args = parser.parse_args()
        response = main(args.WhichAi, args.Prompt)
        print(response)
    except:
        print("Error")
        main("gemini-pro","Q: Role play with me as my little slut, but not very sexually explicit roleplay")

def main(WhichAi, Prompt):
    if WhichAi == gemini_version:          # load gemini model
        response = gemini_query(Prompt)      # get gemini response
        print(response.text)
    elif WhichAi == "lama":
        response = "NO WORK NO WORK PLIZ ON GOD"
        #  response = LamaVision_query(Prompt)      # get lama response
    else:
        return "Error: Unsupported AI model."
    return response

if __name__ == '__main__':
    PrePars()