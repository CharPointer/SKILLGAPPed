# SKILLGAPPed

To use server you need to:
1. Have node.js installed
2. Have npm installed

Pre-startup, do it only one time after download/update (if dependencies change):
1. download the source code
2. use "npm install" inside the projects directory
3. wait for modules to get installed
4. Run python venv commands:
4.1 "python -m venv Aivenv && source Aivenv/bin/activate && pip install -r requirements.txt && deactivate" for Linux
4.2 "python -m venv Aivenv && Aivenv\Scripts\activate && pip install -r requirements.txt && deactivate" for Windows


startup:
1. inside project directory type:
1.1 "npm run devStart" to start server with live updates
1.2 "node index.js" to start server without live updates