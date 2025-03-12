# SKILLGAPPed

THIS WILL INSTALL CUDA VERSION OF Llama_cpp_python CPU UNTESTED, MIGHT BE NEEDED TO REINSTALL Llama.cpp

DEFAULT PORT: 3000

To use server you need to:
1. Have node.js installed
2. Have npm installed
3. Installed pytorch with cuda if you want to use GPU

Pre-startup, do it only one time after download/update (if dependencies change):
1. download the source code
2. use "npm install" inside the projects directory
3. wait for modules to get installed
4. Run python venv commands:


    4.1. "python -m venv Aivenv && source Aivenv/bin/activate && pip install -r requirements.txt && deactivate" for Linux

    4.2. "python -m venv Aivenv && Aivenv\Scripts\activate && pip install -r requirements.txt && deactivate" for Windows

5. For FrontEnd run command "cd front_end && npm install && npm build && cd .."


startup:
1. deployment

    1.1 inside project directory "node index.js" to start server without live updates

2. development

    2.1 programming backend: "npm run devStart" to start server with live updates (backend only)

    2.2 programming frontend: "cd front_end" and "npm run dev" (for working with only front end you dont need to build app, but for it to work with backend YOU WILL NEED to do that) 


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