package com.example;

public class Match {
    private Team homeTeam;
    private Team awayTeam;
    private int week;

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
}