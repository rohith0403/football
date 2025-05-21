package com.example.util;

import java.util.ArrayList;
import java.util.List;

import com.example.PlayerFactory;
import com.example.model.Player;
import com.example.model.Team;

public class SquadGenerator {

    public static void generateSquadForTeam(Team team) {
        int numGoalkeepers = 4;
        int numDefenders = 7;
        int numMidfielders = 7;
        int numAttackers = 7;

        List<Player> squad = new ArrayList<>();

        for (int i = 0; i < numGoalkeepers; i++) {
            Player player = PlayerFactory.createGoalkeeper();
            player.setTeam(team);
            squad.add(player);
        }

        for (int i = 0; i < numDefenders; i++) {
            Player player = PlayerFactory.createDefender();
            player.setTeam(team);
            squad.add(player);
        }

        for (int i = 0; i < numMidfielders; i++) {
            Player player = PlayerFactory.createMidfielder();
            player.setTeam(team);
            squad.add(player);
        }

        for (int i = 0; i < numAttackers; i++) {
            Player player = PlayerFactory.createAttacker();
            player.setTeam(team);
            squad.add(player);
        }

        team.getSquad().clear();
        team.getSquad().addAll(squad);
    }
}
