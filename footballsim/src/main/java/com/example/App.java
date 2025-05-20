package com.example;

import java.util.Arrays;
import java.util.List;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class App {
    public static void main(String[] args) {
        // SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
        //         .addAnnotatedClass(Player.class)
        //         .buildSessionFactory();

        // Session session = factory.openSession();
        // try {
        //     Player player1 = new Player("Player 1", "ENG");
        //     System.out.println(player1);
        //     session.beginTransaction();
        //     session.persist(player1);
        //     session.getTransaction().commit();

        //     System.out.println("User saved with ID: " + player1.getId());
        // } finally {
        //     factory.close();
        // }
        generateTeams();
    }

    public static void generateTeams() {
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
}
