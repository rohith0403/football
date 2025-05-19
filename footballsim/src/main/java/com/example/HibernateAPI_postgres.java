package com.example;

import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;

public class HibernateAPI_postgres {

    public static void main(String[] args) { // Added main method

        SessionFactory sessionFactory = null;
        Session session = null;
        Transaction transaction = null;

        try {
            // Build SessionFactory - typically done once per application
            sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();

            // Open a new Session
            session = sessionFactory.openSession();

            // Begin a transaction
            transaction = session.beginTransaction();

            // Create and execute the HQL query
            // Use the entity name "Player" as defined in your mapping
            Query<Player> query = session.createQuery("FROM Player", Player.class);
            List<Player> players = query.getResultList();

            // Process the results
            if (players.isEmpty()) {
                System.out.println("No players found.");
            } else {
                System.out.println("List of Players:");
                for (Player player : players) {
                    System.out.println("ID: " + player.getId() + ", Name: " + player.getName());
                }
            }

            // Commit the transaction
            transaction.commit();

        } catch (Exception e) {
            // Rollback the transaction in case of an error
            if (transaction != null) {
                transaction.rollback();
            }
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace(); // Print the stack trace for debugging
        } finally {
            // Close the Session and SessionFactory in the finally block
            // This ensures resources are released even if errors occur
            if (session != null && session.isOpen()) {
                session.close();
            }
            if (sessionFactory != null && !sessionFactory.isClosed()) {
                sessionFactory.close();
            }
        }
    }
}