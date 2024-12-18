Install the packages in the requirements.txt with the command:

pip install -r requirements.txt


To run the application, run the command:

streamlit run main.py


In Version v1:

A simple application with the following features:
    1. A team class with name, offense, defense.
    2. A league which can do the following:
        a. predict the outcome of two mathces based on poisson distribution
        b. generate fixtures randomly both for home and away.
        c. Stores the table each week
    3. Displays the table for all 38 gameweeks through a slider.


Coming in the future: (v2)
- sqlite and store the data
- dynamice offense and defense based on morale

Major updates post v2:
- Add players, budget to teams, multiple leagues, reinforcement learning models