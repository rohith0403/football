package com.example.util;
// HibernateUtil.java

import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import com.example.model.Match;
import com.example.model.Player;
import com.example.model.Team;

public class HibernateUtil {
    private static final SessionFactory sessionFactory;

    static {
        try {
            sessionFactory = new Configuration()
                    .configure("hibernate.cfg.xml")
                    .addAnnotatedClass(Player.class)
                    .addAnnotatedClass(Team.class)
                    .addAnnotatedClass(Match.class)
                    .buildSessionFactory();
        } catch (Throwable ex) {
            throw new ExceptionInInitializerError("SessionFactory initialization failed: " + ex);
        }
    }

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }

    public static void shutdown() {
        getSessionFactory().close();
    }
}
