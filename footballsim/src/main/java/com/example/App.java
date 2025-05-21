package com.example;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import com.example.model.League;
import com.example.model.Match;
import com.example.model.Player;
import com.example.model.Team;
import com.example.util.SquadGenerator;

public class App {
    public static void main(String[] args) {
        resetDatabase();
    }

    public static void generatePremierLeagueTeams() {
        // Configure Hibernate and build SessionFactory
        SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
                .addAnnotatedClass(Team.class) // Make sure your Team class is annotated or mapped
                .buildSessionFactory();

        Session session = null; // Initialize session to null

        try {
            // List of current Premier League teams (as of 2024-2025 season)
            List<String> premierLeagueTeams = Arrays.asList(
                    "Arsenal", "Aston Villa", "Bournemouth", "Brentford",
                    "Brighton & Hove Albion", "Chelsea", "Crystal Palace",
                    "Everton", "Fulham", "Ipswich Town", "Leicester City",
                    "Liverpool", "Manchester City", "Manchester United",
                    "Newcastle United", "Nottingham Forest", "Southampton",
                    "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers");

            session = factory.openSession(); // Open a new session

            // Begin transaction
            session.beginTransaction();

            System.out.println("Generating and saving Premier League teams...");

            // Iterate through the list and persist each team
            for (String teamName : premierLeagueTeams) {
                Team team = new Team(teamName, "Premier League");
                session.persist(team); // Use persist for new entities
                SquadGenerator.generateSquadForTeam(team); // Populate the squad with players
                System.out.println("Persisted team: " + team.getName());
            }

            // Commit the transaction
            session.getTransaction().commit();

            System.out.println("All Premier League teams saved successfully!");

        } catch (Exception e) {
            // Rollback transaction in case of error
            if (session != null && session.getTransaction() != null && session.getTransaction().isActive()) {
                session.getTransaction().rollback();
                System.err.println("Transaction rolled back.");
            }
            e.printStackTrace(); // Print the exception details
        } finally {
            // Close the session and factory
            if (session != null) {
                session.close();
            }
            if (factory != null) {
                factory.close();
            }
            System.out.println("SessionFactory and Session closed.");
        }
    }

    public static void clearDB() {
        SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
                .addAnnotatedClass(Player.class)
                .addAnnotatedClass(Team.class)
                .addAnnotatedClass(Match.class) // <--- add this

                .buildSessionFactory();

        try (Session session = factory.openSession()) {
            session.beginTransaction();

            session.createMutationQuery("DELETE FROM Player").executeUpdate();
            session.createMutationQuery("DELETE FROM Team").executeUpdate();
            session.createMutationQuery("DELETE FROM Match").executeUpdate();

            // Reset sequences
            session.createNativeQuery("ALTER SEQUENCE players_id_seq RESTART WITH 1", Void.class).executeUpdate();
            session.createNativeQuery("ALTER SEQUENCE teams_id_seq RESTART WITH 1", Void.class).executeUpdate();
            session.createNativeQuery("ALTER SEQUENCE matches_id_seq RESTART WITH 1", Void.class).executeUpdate();

            session.getTransaction().commit();
        } finally {
            factory.close(); // <== important
        }
    }

    public static List<Team> getAllTeams() {
        List<Team> teams;

        SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
                .addAnnotatedClass(Team.class)
                .addAnnotatedClass(Player.class)
                .addAnnotatedClass(Match.class) // <--- add this
                .buildSessionFactory();

        try (Session session = factory.openSession()) {
            session.beginTransaction();

            // HQL query to get all teams
            teams = session.createQuery("FROM Team", Team.class).getResultList();

            session.getTransaction().commit();
        }

        return teams;
    }

    public static void saveFixtures() {
        List<Team> teams = getAllTeams();
        List<List<Match>> matches = League.generateSchedule(teams);

        List<Match> allMatches = matches.stream()
                .flatMap(List::stream)
                .collect(Collectors.toList());

        SessionFactory factory = new Configuration()
                .configure("hibernate.cfg.xml")
                .addAnnotatedClass(Team.class)
                .addAnnotatedClass(Match.class)
                .buildSessionFactory();

        try (Session session = factory.openSession()) {
            session.beginTransaction();

            // save all matches
            for (Match match : allMatches) {
                session.persist(match);
            }

            session.getTransaction().commit();
        } finally {
            factory.close();
        }

    }

    public static void resetDatabase() {
        clearDB();
        generatePremierLeagueTeams();
        saveFixtures();
    }
}
