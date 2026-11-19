# Step by step on opening and running

## Step 1: Cloning the Repo thru GitHub into VSCode
This step is assuming that you have vscode installed and have linked your GitHub account through vscode (as well as downloaded git and set it up through your computer).
If you have not, go ahead and do that now.

1. Open VSCode
2. Make sure you have GitHub linked and Git set up, then press Ctrl + Shift + P (or click on the top bar and type ">"), type "Git: Clone", paste the link of the GitHub Repository into the bar, and click enter. It should prompt you to open a folder for the Repo to go to.

## Step 2: Creating the Virtual Environment
IMPORTANT: You NEED Python 3.12 or 3.13 to run this. If you downloaded Python recently for this class, you are likely on the later versions of 3.14 or the new 3.15, which does not support a lot of the libraries that are used for this project. Go to python.org to download an older version (3.12 runs the best).

3. Once the folder is open, press Ctrl + ` or click on the top left "Terminal" selection and choose "New Terminal"
4. Alternatively, you can press Ctrl + Shift + P again and choose "Python: Create Environment", then venv, then your Python version. It will also prompt you to install dependencies, which are in the requirements.txt file (it should automatically ask you if you want to download those files). Allow it to do so.
5. If you are using the terminal, run python -m pip install --upgrade pip 
6. Then run pip install -r requirements.txt to download dependencies. 
7. Now, download ffmpeg through the terminal: winget install Gyan.FFmpeg
8. Once everything finishes downloading (may take a while), close and reopen vscode so that the ffmpeg can load and update correctly

## Step 3: Running the files
9. These files cannot be run traditionally through a "play" button. make sure the virtual environment is open, in the terminal, it should show (.venv) before your folder destination, which shows you are in the virtual environment.
10. run: "manimgl fourier_viz.py FourierWindingMachine" through the terminal. This is the fourier_viz file, running the FourierWindingMachine class in the code.

## Step 4: Running Streamlit
11. Running streamlit also does not work through clicking the "play" button. in the terminal, run "streamlit run streamlit_test.py". This should open a local host tab in your browser, from which you can run the code. Try the website out to see if it works. 
