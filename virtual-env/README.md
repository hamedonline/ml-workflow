# Introduction
Imagine a folder named "prediction-app" containing our _inference&#46;py_ and _model&#46;bin_ files. Now we want to add all the packages & libraries required to run the inference file inside this folder without any concerns regarding compatibility or messing with our machine's libraries. Virtual environments enable us to achieve exactly this in a very hassle-free fashion, without compromising other packages in our system and avoiding __dependency hell__ complications.


# Prerequisites
You would need to have _python3_, _pip_ and _pipenv_ already installed on your system. You may like to do manual install via official guides, or use an existing platform like [Anaconda](https://www.anaconda.com) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for convenient library installs.


# Creating a Virtual Environment
Creating a virtual environment is easy and straightforward. We'll use __*pipenv*__ to manage our virtual environment. There are also other good options, but that is another story for us to study & explore.

First of all, prepare the folder and put your files (just like the ml-flow example) inside it. Open up a terminal (Linux) or command prompt (Windows) or Anaconda prompt (if you're using Anaconda or Miniconda).
Navigate to inside of this folder in your terminal and run the following command:
```
pip install -r requirements.txt
```

This will take care of creating a virtual environment (in your folder) and installing dependencies for you.
From now on, all you need to do is to activate the virtual environment and run your commands from it's shell.
To activate folder's virtual shell, we should run the following command inside our folder:
```
pipenv shell
```

That command launches a __subshell__ in our virtual environment and we can run any commands we like related to our specific environment from here. For example, if we want to run our flask app and expose an API endpoint, we can set in motion by running this from subshell:
```
python inference.py
```
or
```
python -m inference
```
__Warning__: Don't forget to update model path inside _inference&#46;py_ accordingly ;)

You can do the same steps for this entire repo in similar manner.