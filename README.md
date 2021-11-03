# Machine Learning Workflow - From EDA to Production

## Introduction
This repo tries to study & apply the least minimal steps involved in machine learning workflow the right way. It is compiled during the ["Machine Learning Zoomcamp"](https://datatalks.club/courses/2021-winter-ml-zoomcamp.html) course instructed by amazing [@alexeygrigorev](https://github.com/alexeygrigorev).
<br><br>


## Problem Description
 
<br><br>


## About the Dataset
The dataset used in this repo is a __"Tabular"__ one, meaning the data is represented in __rows__ and __columns__, corresponding to __samples__ and __features__ respectively.<br>
Data columns (features) are in both __categorical__ and __numerical__ types. The target column (the last column)...
Train and test datasets contain __188,318__ and __125,546__ rows (samples) respectively with __130__ columns as features, plus two more columns representing "claim id" and "target" named as _'id'_ and _'loss'_.
<br><br>


## Important Note
For the sake of simplicity, we assume that __"Data Collection"__ step is already done since we're going to use a publicly available Kaggle dataset. Please note though, this is not the case in real-world scenarios. Most of the time, tabular data is collected by querying multiple database tables and running pretty complex SQL commands. If you're planning to become a machine learning engineer, make sure you understand and know a good deal about databases and writing efficient SQL queries; that, ladies and gents, turns out to be an essential & invaluable asset to possess for a ML engineer.

The main intention in this workflow is not achieving the best benchmark score for the subject dataset, and by no way it claims to contain the most complete sub-steps.

Given the above line you might ask, what's the focus here? I can summarize the answer with following lines:
- To take a quick look at the minimal required steps involved in a machine learning problem, from EDA to production.
- Trying to avoid common slips, and conducting each step the right way.
- Keep in mind that the material here is only tip of the iceberg, but hopefully with a nice view 😉.
<br><br>