package com.example;

import java.sql.Connection;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class App {
    public static void main(String[] args) {

        SQLiteConnection.connect();

    }

    public static void openPostgresConnection() {
        SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
                .addAnnotatedClass(Player.class)
                .buildSessionFactory();

        Session session = factory.openSession();
        try {
            Player player1 = new Player("Player 1", "ENG");
            System.out.println(player1);
            session.beginTransaction();
            session.persist(player1);
            session.getTransaction().commit();

            System.out.println("User saved with ID: " + player1.getId());
        } finally {
            factory.close();
        }

    }

    public static void generateTeams() {
        SessionFactory factory = new Configuration().configure("hibernate.cfg.xml")
                .addAnnotatedClass(Team.class)
                .buildSessionFactory();
        Session session = factory.openSession();
        try {
            Team team1 = new Team("Team 1", "League 1");
            System.out.println(team1);
            session.beginTransaction();
            session.persist(team1);
            session.getTransaction().commit();
            System.out.println("Team saved with ID: " + team1.getId());
        } finally {
            factory.close();
        }
    }
}
