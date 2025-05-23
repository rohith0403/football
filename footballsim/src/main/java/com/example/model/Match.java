package com.example.model;

import java.util.Random;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "matches")
public class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "home_team_id", nullable = false)
    private Team homeTeam;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "away_team_id", nullable = false)
    private Team awayTeam;

    @Column(name = "week")
    private int week;

    @Column(name = "home_score")
    private int homeScore;

    @Column(name = "away_score")
    private int awayScore;

    public int getHomeScore() {
        return this.homeScore;
    }

    public void setHomeScore(int homeScore) {
        this.homeScore = homeScore;
    }

    public int getAwayScore() {
        return this.awayScore;
    }

    public void setAwayScore(int awayScore) {
        this.awayScore = awayScore;
    }

    public Match(Team home, Team away, int week) {
        this.homeTeam = home;
        this.awayTeam = away;
        this.week = week;
    }

    public Team getHomeTeam() {
        return homeTeam;
    }

    public Team getAwayTeam() {
        return awayTeam;
    }

    public int getWeek() {
        return week;
    }

    public void playMatch(Match match) {
        Team homeTeam = match.getHomeTeam();
        Team awayTeam = match.getAwayTeam();

        // Base score calculation using team ratings
        double homeBaseScore = (homeTeam.getAttack() * 0.4 +
                homeTeam.getMidfield() * 0.3 +
                homeTeam.getDefense() * 0.3) * 1.2; // Home advantage

        double awayBaseScore = (awayTeam.getAttack() * 0.4 +
                awayTeam.getMidfield() * 0.3 +
                awayTeam.getDefense() * 0.3);

        // Add randomness (gaussian distribution for more realistic scores)
        Random random = new Random();
        double homeRandomFactor = random.nextGaussian() * 0.5 + 1.0;
        double awayRandomFactor = random.nextGaussian() * 0.5 + 1.0;

        // Calculate final scores
        int finalHomeScore = (int) Math.round(homeBaseScore * homeRandomFactor);
        int finalAwayScore = (int) Math.round(awayBaseScore * awayRandomFactor);

        // Ensure non-negative scores
        finalHomeScore = Math.max(0, finalHomeScore);
        finalAwayScore = Math.max(0, finalAwayScore);

        // Set the scores
        match.setHomeScore(finalHomeScore);
        match.setAwayScore(finalAwayScore);

        // Update match statistics
        updateStats(match);
    }

    public static void updateStats(Match match) {
        Team home = match.getHomeTeam();
        Team away = match.getAwayTeam();
        int hg = match.getHomeScore();
        int ag = match.getAwayScore();

        // Update global stats
        home.setGoalsScored(home.getGoalsScored() + hg);
        home.setGoalsConceded(home.getGoalsConceded() + ag);
        home.setMatchesPlayed(home.getMatchesPlayed() + 1);

        away.setGoalsScored(away.getGoalsScored() + ag);
        away.setGoalsConceded(away.getGoalsConceded() + hg);
        away.setMatchesPlayed(away.getMatchesPlayed() + 1);

        // Update home/away stats
        home.setHomeMatchesPlayed(home.getHomeMatchesPlayed() + 1);
        home.setHomeGoalsScored(home.getHomeGoalsScored() + hg);
        home.setHomeGoalsConceded(home.getHomeGoalsConceded() + ag);

        away.setAwayMatchesPlayed(away.getAwayMatchesPlayed() + 1);
        away.setAwayGoalsScored(away.getAwayGoalsScored() + ag);
        away.setAwayGoalsConceded(away.getAwayGoalsConceded() + hg);

        // Win/loss/draw
        if (hg > ag) {
            home.setWins(home.getWins() + 1);
            home.setPoints(home.getPoints() + 3);
            home.setHomeWins(home.getHomeWins() + 1);

            away.setLosses(away.getLosses() + 1);
            away.setAwayLosses(away.getAwayLosses() + 1);
        } else if (hg < ag) {
            away.setWins(away.getWins() + 1);
            away.setPoints(away.getPoints() + 3);
            away.setAwayWins(away.getAwayWins() + 1);

            home.setLosses(home.getLosses() + 1);
            home.setHomeLosses(home.getHomeLosses() + 1);
        } else {
            home.setDraws(home.getDraws() + 1);
            away.setDraws(away.getDraws() + 1);

            home.setPoints(home.getPoints() + 1);
            away.setPoints(away.getPoints() + 1);

            home.setHomeDraws(home.getHomeDraws() + 1);
            away.setAwayDraws(away.getAwayDraws() + 1);
        }

        // You can add logic here to update streaks too}
        // Update streaks
        if (hg > ag) { // Home win
            home.setHomeStreak(updateStreak(home.getHomeStreak(), true));
            away.setAwayStreak(updateStreak(away.getAwayStreak(), false));
        } else if (hg < ag) { // Away win
            away.setAwayStreak(updateStreak(away.getAwayStreak(), true));
            home.setHomeStreak(updateStreak(home.getHomeStreak(), false));
        } else { // Draw
            home.setHomeStreak(0);
            away.setAwayStreak(0);
        }
    }

    private static int updateStreak(int current, boolean win) {
        if (win) {
            return current >= 0 ? current + 1 : 1;
        } else {
            return current <= 0 ? current - 1 : -1;
        }
    }

}