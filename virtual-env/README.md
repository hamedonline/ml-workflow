# A Quick Guide to Creating and Employing Virtual Environments

## Introduction

Imagine a folder named "prediction-app" containing our ``inference.py`` and ``model.bin`` files. Now we want to add all the packages & libraries required to run the inference file inside this folder without any concerns regarding compatibility or messing with our machine's libraries. Virtual environments enable us to achieve exactly this in a very hassle-free fashion, without compromising other packages in our system and avoiding __dependency hell__ complications.

## Prerequisites

You would need to have __*python3*__, __*pip*__ and __*pipenv*__ already installed on your system. You may like to do manual install via official guides, or use an existing platform like [Anaconda](https://www.anaconda.com) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for convenient library installs. As the name _"pip"_ suggests, we are using pip package-management system that finds & installs libraries through [PyPI](https://pypi.org).

## Creating Virtual Environments

### Method (A): Using ``requirements.txt`` File

Creating a virtual environment is easy and straightforward. We'll use __*pipenv*__ to manage our virtual environment. There are also other good options, but that is another story for us to study & explore.

First of all, prepare the folder and put your files inside it (just like the inference example mentioned in introduction section above). Create an additional file, named ``requirements.txt``. This is the file holding the names of libraries we'd like our virtual environment to have. Inside ``requirements.txt`` file, put in each required library name (this should be equal to the name used when installing by pip, for instance: pip install __sklearn__); each line must have only one library name. This is what a typical ``requirements.txt`` file should look like:

⬇️ __requirements&#46;txt__

```text
numpy
pandas
sklearn
xgboost
flask
waitress
```

It is a good advice to include the version number you're using for each library. If you have deterministic approach, you won't risk a possible conflict between your out-of-date code and break-down-type changes in future versions of libraries.

```text
...
sklearn==1.0.1
...
```

Now that you have your ``requirements.txt`` file ready, open up a terminal (Linux) or command prompt (Windows) or Anaconda prompt (if you're using Anaconda or Miniconda).
Navigate to this folder in your terminal and run the following command:

```shell
pipenv install -r requirements.txt
```

### Method (B): Using ``Pipfile`` & ``Pipfile.lock`` Files

These are the files that get created and filled during a successful method (A) run process. Having access to only these two would let you replicate the environment on any other machine without a need for ``requirements.txt`` file. The good thing about this method is that each library's version number is specified and the chance of any incompatibilities goes to zero. If you don't already have access to these two files though, you've got no choice but to go with method (A).

With these two files inside the folder you like to have new environment in, run the following command in your terminal (Linux) or command prompt (Windows) or Anaconda prompt (if you're using Anaconda or Miniconda):

```shell
pipenv install
```

That's all! Your new virtual environment is ready.

## Activating the Virtual Environment

Both methods (A) and (B) can take care of creating a virtual environment (inside your desired folder) and install dependencies for you. Having the virtual environment set, all you need to do is to activate it and run your commands from it's shell.
To activate folder's virtual shell, we should run the following command inside our folder:

```shell
pipenv shell
```

That command launches a __subshell__ in our virtual environment that allows us to run any commands we like related to our specific environment from here. For example, if we want to run our flask app and expose an API endpoint, we can set it in motion by running below line from subshell:

```shell
python inference.py
```

or

```shell
python -m inference
```

__Warning__: Don't forget to copy ``inference.py`` and ``model/model.bin`` to your virtual environment folder (these files are provided inside __``script``__ folder of this repository). In addition, you must update model path variable in ``inference.py`` accordingly.

I've already provided ``requirements.txt``, ``Pipfile`` and ``Pipfile.lock`` files inside this folder and you can try either methods as an exercise. Just as a side note, you can even try method (A) for this entire repo using ``requirements.txt`` file in repository's root.

## Bonus: Generating a ``requirements.txt`` file from Pipfile

It is possible to generate back ``requirements.txt`` file using ``Pipfile`` and ``Pipfile.lock`` files. All you need to do is to run the following command inside a folder containing Pipfiles:

```shell
pipenv lock -r > requirements.txt
```

Last but not least, make sure to check out some very useful advanced tips on ``pipenv`` [here](https://github.com/pypa/pipenv/blob/main/docs/advanced.rst).
