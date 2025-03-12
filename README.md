# SKILLGAPPed

Hackaton project

# Build

THIS WILL INSTALL CUDA VERSION OF Llama_cpp_python CPU UNTESTED, MIGHT BE NEEDED TO REINSTALL Llama.cpp

DEFAULT PORT: 3000

To use server you need to:
1. Have node.js installed
2. Have npm installed
3. Installed pytorch (with cuda if you want to use GPU)

Pre-startup, do it only one time after download/update (if dependencies change):
1. download the source code
2. run command:

    2.1 "npm run BuildProjectLinux" for linux

    2.2 "npm run BuildProjectWindows" for windows

startup:
1. deployment

    1.1 inside project directory "node index.js" to start server without live updates

2. development

    2.1 programming backend: "npm run devStart" to start server with live updates (backend only)

    2.2 for building front end there is command "npm run Build"

    2.3 programming frontend: "cd front_end" and "npm run dev" (for working with only front end you dont need to build app, but for it to work with backend YOU WILL NEED to do that) 


# Infrastructure

Backend:
Node.js with Express.js

Frontend: 
Reacte

AI pipeline:
1. python script "Kasperski" which takes dataset (csv for now) Fixes it and generates prompt for LLM

2. LLM (using llama.cpp) which takes the prompt and generates .bumbuojam (pseudo) code for the interpreter

3. python script "Interpreter" it takes the .bumbuojam code and generates valid plotly vizualizations

4. Vizual LLM checks if vizualization is good, if not we go to step 2

4. server sends those vizualizations back to user