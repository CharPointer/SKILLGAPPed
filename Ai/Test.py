from SuperGlue import Pipeline as pipes
import os
cwd = os.getcwd()

csv = cwd + "/UploadedFiles/Cities.csv"
bumbuojam = cwd + "/Ai/BumbuojamFiles/Cities.bumbuojam"

pipes(csv,bumbuojam)