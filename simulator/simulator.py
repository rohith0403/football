def match_simulator(teamA, teamB):
    if teamA.get_overall_ability() > teamB.get_overall_ability():
        return teamA
    elif teamA.get_overall_ability() < teamB.get_overall_ability():
        return teamB
    return 0
