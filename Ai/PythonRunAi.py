import sys
from llama_cpp import Llama

llm = Llama(
        model_path="./Ai/Model/Bollywood.gguf",
        n_gpu_layers=-1, # Uncomment to use GPU acceleration
        seed=1335, # Uncomment to set a specific seed
        #n_ctx=512, # Uncomment to increase the context window
        # n_ctx = 131070,
        # verbose=False
)

output = llm(
      """Create a fictional Bollywood song based on the provided theme. Your song should capture the essence of Bollywood music, incorporating catchy melodies, lively rhythms, and engaging lyrics.

### Instructio:
A neighbour who helped rescue horses from the property's stable said she was woken by an explosion and "looked out the window to see a sea of orange".

### Response:
""", # Prompt
      max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
      stop=["<|end_of_text|>", "\n"], # Stop generating just before the model would generate a new question
      echo=True # Echo the prompt back in the output
) # Generate a completion, can also call create_completion
print(output['choices'][0]['text'])

print("GAY", flush=True)
sys.stdout.flush()