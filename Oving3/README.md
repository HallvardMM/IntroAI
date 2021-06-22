# Oving3IntroAI

## prerequisite
- python 3
- pip

## How to run

### In multiagent folder:

On macOS and Linux:
`python3 -m venv env`

On Windows:
`py -m venv env`

### Run virtual enviroment
On macOS and Linux:
`source env/bin/activate`

Windows:
`.\env\Scripts\activate`

### Add required packages
`pip install -r requirements.txt`

## Add packages
After pip installing package do:
`pip freeze > requirements.txt`

## To leave virtual enviroment
Leaving the virtual environment:
`deactivate`

## To run the tasks
As specified in the questions, your code should be implemented by editing the classes:
- MinimaxAgent 
- AlphaBetaAgent 
in multiAgents.py. Your code should then be
tested for correctness by running respectively 
`python autograder.py -q q2` 
and 
`python autograder.py -q q3`
