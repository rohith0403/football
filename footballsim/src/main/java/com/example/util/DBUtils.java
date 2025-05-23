package com.example.util;

import org.hibernate.Session;

// DBUtils.java
public class DBUtils {

    public static void clearDBPostgres() {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            session.beginTransaction();

            // Truncate all tables and restart identity
            session.createNativeQuery("TRUNCATE TABLE matches, players, teams RESTART IDENTITY CASCADE", Object.class)
                    .executeUpdate();

            session.getTransaction().commit();
        }
    }
}
