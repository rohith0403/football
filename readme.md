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


In Version (v2):
    1. Added DB which stores a seasons table. And each season generates a teams table and a league history table
    2. Added multi season support where the league can be run through multiple seasons.
    3. Added Dynamic offense and defense for teams which are based on the performance of the team in the previous season.
    4. Added Budget and prize money allotment.
    5. Added Pylint to the application and refactored the code.
    6. Added a match engine to demo the predict outcome of a model.
    Current Flow of the application.
        Step 1 : Click on Initialize DB.
        Step 2 : Click on Run Full season
        Step 3 : Click on Generate New season
        Step 4 : Repeat Step2 and Step 3.
    7. Added form factor to the team. (though currently not taken into account in the final predict_outcome. Still prototyping)


Major updates post v2:
- Add players, budget to teams, multiple leagues, reinforcement learning models