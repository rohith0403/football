package com.example;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class League {
    // Step 1: Private static instance
    private static League instance;

    // Step 2: Private constructor
    private League() {
        // Initialize your league here (e.g., teams, matches, schedule)
    }

    // Step 3: Public static method to get the instance
    public static synchronized League getInstance() {
        if (instance == null) {
            instance = new League();
        }
        return instance;
    }

    public static List<List<Match>> generateSchedule(List<Team> teams) {
        Collections.shuffle(teams); // true randomness every time
        int numTeams = teams.size();
        int matchesPerRound = numTeams / 2;

        List<List<Match>> schedule = new ArrayList<>();
        Map<Team, Integer> homeStreak = new HashMap<>(); // Track home streaks per team

        // Generate first half of the schedule (round-robin)
        List<Team> rotation = new ArrayList<>(teams);
        for (int round = 0; round < numTeams - 1; round++) {
            List<Match> matches = new ArrayList<>();
            for (int match = 0; match < matchesPerRound; match++) {
                Team home = rotation.get(match);
                Team away = rotation.get(numTeams - 1 - match);

                if (home != null && away != null) {
                    // Check home streaks and swap if necessary
                    int homeStreakCount = homeStreak.getOrDefault(home, 0);
                    int awayStreakCount = homeStreak.getOrDefault(away, 0);

                    if (homeStreakCount >= 2 && awayStreakCount < 2) {
                        Team temp = home;
                        home = away;
                        away = temp;
                    }

                    matches.add(new Match(home, away, round + 1));

                    // Update streaks
                    homeStreak.put(home, homeStreak.getOrDefault(home, 0) + 1);
                    homeStreak.put(away, 0); // reset away team's home streak
                }
            }
            schedule.add(matches);

            // Rotate teams (except first)
            rotation.add(1, rotation.remove(rotation.size() - 1));
        }

        // Reset streaks for second half
        homeStreak.clear();

        // Generate second half by swapping home and away, rounds continue
        for (int round = 0; round < numTeams - 1; round++) {
            List<Match> matches = new ArrayList<>();
            for (Match m : schedule.get(round)) {
                Team home = m.getAwayTeam();
                Team away = m.getHomeTeam();

                int homeStreakCount = homeStreak.getOrDefault(home, 0);
                int awayStreakCount = homeStreak.getOrDefault(away, 0);

                if (homeStreakCount >= 2 && awayStreakCount < 2) {
                    Team temp = home;
                    home = away;
                    away = temp;
                }

                matches.add(new Match(home, away, round + 1 + (numTeams - 1)));

                // Update streaks
                homeStreak.put(home, homeStreak.getOrDefault(home, 0) + 1);
                homeStreak.put(away, 0);
            }
            schedule.add(matches);
        }

        // Print schedule
        for (List<Match> round : schedule) {
            System.out.println("Week " + round.get(0).getWeek() + ":");
            for (Match m : round) {
                System.out.println(m.getHomeTeam().getName() + " vs " + m.getAwayTeam().getName());
            }
            System.out.println();
        }
        return schedule;
    }

    public static void simulateMatch(Team team1, Team team2) {
        // Logic to simulate a match between two teams
        // This could involve randomizing the outcome based on player stats
    }
}
