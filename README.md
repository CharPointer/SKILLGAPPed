# SKILLGAPPed

THIS WILL INSTALL CUDA VERSION OF Llama_cpp_python CPU UNTESTED, MIGHT BE NEEDED TO REINSTALL Llama.cpp

To use server you need to:
1. Have node.js installed
2. Have npm installed

Pre-startup, do it only one time after download/update (if dependencies change):
1. download the source code
2. use "npm install" inside the projects directory
3. wait for modules to get installed
4. Run python venv commands:


    4.1. "python -m venv Aivenv && source Aivenv/bin/activate && pip install -r requirements.txt && deactivate" for Linux

    4.2. "python -m venv Aivenv && Aivenv\Scripts\activate && pip install -r requirements.txt && deactivate" for Windows


startup:
1. inside project directory type:

    1.1. "npm run devStart" to start server with live updates

    2.1. "node index.js" to start server without live updates


# Infrastructure

Backend:
Node.js with Express.js

Frontend: 
React

AI pipeline:
1. python script "Kasperski" which takes dataset (csv for now) Fixes it and generates prompt for LLM

2. LLM (using llama.cpp) which takes the prompt and generates .bumbuojam (pseudo) code for the interpreter

3. python script "Interpreter" it takes the .bumbuojam code and generates valid plotly vizualizations

4. Vizual LLM checks if vizualization is good, if not we go to step 2

4. server sends those vizualizations back to user