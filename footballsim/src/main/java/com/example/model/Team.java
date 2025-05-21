package com.example.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity // Marks this class as a database entity
@Table(name = "teams") // Specifies the table name (optional, defaults to class name)
public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "name")
    private String name;

    @Column(name = "league")
    private String league;

    @OneToMany(mappedBy = "team", cascade = CascadeType.ALL, orphanRemoval = false, fetch = FetchType.LAZY)
    private List<Player> squad = new ArrayList<>();

    // Team attributes
    @Column(name = "attack")
    private int attack;
    @Column(name = "midfield")
    private int midfield;
    @Column(name = "defense")
    private int defense;
    @Column(name = "goalkeepeing")
    private int goalkeeping;

    public int getAttack() {
        return attack;
    }

    public void setAttack(int attack) {
        this.attack = attack;
    }

    public int getMidfield() {
        return midfield;
    }

    public void setMidfield(int midfield) {
        this.midfield = midfield;
    }

    public int getDefense() {
        return defense;
    }

    public void setDefense(int defense) {
        this.defense = defense;
    }

    public int getGoalkeeping() {
        return goalkeeping;
    }

    public void setGoalkeeping(int goalkeeping) {
        this.goalkeeping = goalkeeping;
    }

    // Team stats
    @Column(name = "wins")
    private int wins;
    @Column(name = "losses")
    private int losses;
    @Column(name = "draws")
    private int draws;
    @Column(name = "goals_scored")
    private int goalsScored;
    @Column(name = "goals_conceded")
    private int goalsConceded;
    @Column(name = "points")
    private int points;
    @Column(name = "matches_played")
    private int matchesPlayed;
    @Column(name = "home_streak")
    private int homeStreak;
    @Column(name = "away_streak")
    private int awayStreak;
    @Column(name = "home_wins")
    private int homeWins;
    @Column(name = "away_wins")
    private int awayWins;
    @Column(name = "home_losses")
    private int homeLosses;
    @Column(name = "away_losses")
    private int awayLosses;
    @Column(name = "home_draws")
    private int homeDraws;
    @Column(name = "away_draws")
    private int awayDraws;
    @Column(name = "home_goals_scored")
    private int homeGoalsScored;
    @Column(name = "away_goals_scored")
    private int awayGoalsScored;
    @Column(name = "home_goals_conceded")
    private int homeGoalsConceded;
    @Column(name = "away_goals_conceded")
    private int awayGoalsConceded;
    @Column(name = "home_matches_played")
    private int homeMatchesPlayed;
    @Column(name = "away_matches_played")
    private int awayMatchesPlayed;
    @Column(name = "home_points")
    private int homePoints;
    @Column(name = "away_points")
    private int awayPoints;

    public int getWins() {
        return wins;
    }

    public void setWins(int wins) {
        this.wins = wins;
    }

    public int getLosses() {
        return losses;
    }

    public void setLosses(int losses) {
        this.losses = losses;
    }

    public int getDraws() {
        return draws;
    }

    public void setDraws(int draws) {
        this.draws = draws;
    }

    public int getGoalsScored() {
        return goalsScored;
    }

    public void setGoalsScored(int goalsScored) {
        this.goalsScored = goalsScored;
    }

    public int getGoalsConceded() {
        return goalsConceded;
    }

    public void setGoalsConceded(int goalsConceded) {
        this.goalsConceded = goalsConceded;
    }

    public int getPoints() {
        return points;
    }

    public void setPoints(int points) {
        this.points = points;
    }

    public int getMatchesPlayed() {
        return matchesPlayed;
    }

    public void setMatchesPlayed(int matchesPlayed) {
        this.matchesPlayed = matchesPlayed;
    }

    public int getHomeStreak() {
        return homeStreak;
    }

    public void setHomeStreak(int homeStreak) {
        this.homeStreak = homeStreak;
    }

    public int getAwayStreak() {
        return awayStreak;
    }

    public void setAwayStreak(int awayStreak) {
        this.awayStreak = awayStreak;
    }

    public int getHomeWins() {
        return homeWins;
    }

    public void setHomeWins(int homeWins) {
        this.homeWins = homeWins;
    }

    public int getAwayWins() {
        return awayWins;
    }

    public void setAwayWins(int awayWins) {
        this.awayWins = awayWins;
    }

    public int getHomeLosses() {
        return homeLosses;
    }

    public void setHomeLosses(int homeLosses) {
        this.homeLosses = homeLosses;
    }

    public int getAwayLosses() {
        return awayLosses;
    }

    public void setAwayLosses(int awayLosses) {
        this.awayLosses = awayLosses;
    }

    public int getHomeDraws() {
        return homeDraws;
    }

    public void setHomeDraws(int homeDraws) {
        this.homeDraws = homeDraws;
    }

    public int getAwayDraws() {
        return awayDraws;
    }

    public void setAwayDraws(int awayDraws) {
        this.awayDraws = awayDraws;
    }

    public int getHomeGoalsScored() {
        return homeGoalsScored;
    }

    public void setHomeGoalsScored(int homeGoalsScored) {
        this.homeGoalsScored = homeGoalsScored;
    }

    public int getAwayGoalsScored() {
        return awayGoalsScored;
    }

    public void setAwayGoalsScored(int awayGoalsScored) {
        this.awayGoalsScored = awayGoalsScored;
    }

    public int getHomeGoalsConceded() {
        return homeGoalsConceded;
    }

    public void setHomeGoalsConceded(int homeGoalsConceded) {
        this.homeGoalsConceded = homeGoalsConceded;
    }

    public int getAwayGoalsConceded() {
        return awayGoalsConceded;
    }

    public void setAwayGoalsConceded(int awayGoalsConceded) {
        this.awayGoalsConceded = awayGoalsConceded;
    }

    public int getHomeMatchesPlayed() {
        return homeMatchesPlayed;
    }

    public void setHomeMatchesPlayed(int homeMatchesPlayed) {
        this.homeMatchesPlayed = homeMatchesPlayed;
    }

    public int getAwayMatchesPlayed() {
        return awayMatchesPlayed;
    }

    public void setAwayMatchesPlayed(int awayMatchesPlayed) {
        this.awayMatchesPlayed = awayMatchesPlayed;
    }

    public int getHomePoints() {
        return homePoints;
    }

    public void setHomePoints(int homePoints) {
        this.homePoints = homePoints;
    }

    public int getAwayPoints() {
        return awayPoints;
    }

    public void setAwayPoints(int awayPoints) {
        this.awayPoints = awayPoints;
    }

    public Team() {
        // no-arg constructor required by Hibernate
    }

    public Team(String name, String league) {
        this.name = name;
        this.league = league;
    }

    public long getId() {
        return this.id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLeague() {
        return this.league;
    }

    public void setLeague(String league) {
        this.league = league;
    }

    public List<Player> getSquad() {
        return this.squad;
    }

    public void setSquad(List<Player> squad) {
        this.squad = squad;
    }

    public void generateAttributes() {
        System.out.println("Generating attributes for team: " + this.name);

        List<Player> gks = new ArrayList<>();
        List<Player> defs = new ArrayList<>();
        List<Player> mids = new ArrayList<>();
        List<Player> atts = new ArrayList<>();

        for (Player player : this.squad) {
            if (player instanceof Goalkeeper) {
                gks.add(player);
            } else {
                String pos = player.getPosition(); // "Defender", "Midfielder", "Attacker"
                switch (pos) {
                    case "DEFENDER" -> defs.add(player);
                    case "MIDFIELDER" -> mids.add(player);
                    case "ATTACKER" -> atts.add(player);
                }

            }
        }

        // Sort by relevant stats
        gks.sort(Comparator.comparingInt(
                p -> ((Goalkeeper) p).getDiving() + ((Goalkeeper) p).getReflexes() + ((Goalkeeper) p).getHandling()));
        Collections.reverse(gks); // highest first

        defs.sort(Comparator.comparingInt(Player::getDefense).reversed());
        mids.sort(Comparator.comparingInt(Player::getMidfield).reversed());
        atts.sort(Comparator.comparingInt(Player::getAttack).reversed());

        List<Player> top11 = new ArrayList<>();
        if (!gks.isEmpty())
            top11.add(gks.get(0)); // 1 GK
        top11.addAll(defs.stream().limit(4).toList()); // 4 DEF
        top11.addAll(mids.stream().limit(3).toList()); // 3 MID
        top11.addAll(atts.stream().limit(3).toList()); // 3 ATT

        // Compute averages
        int totalAttack = 0, totalMid = 0, totalDef = 0;
        for (Player p : top11) {
            totalAttack += p.getAttack();
            totalMid += p.getMidfield();
            totalDef += p.getDefense();
        }

        int size = top11.size();
        this.setAttack(totalAttack / size);
        this.setMidfield(totalMid / size);
        this.setDefense(totalDef / size);

        System.out.printf("Team %s - Avg Attack: %d, Midfield: %d, Defense: %d\n",
                name, this.getAttack(), this.getMidfield(), this.getDefense());
    }

}
