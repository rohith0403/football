package com.example;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class SQLiteConnection {

    public static void connect() {
        Connection conn = null;
        try {
            // Database URL: "jdbc:sqlite:" followed by the database file path.
            // If the database file doesn't exist, it will be created.
            // Use ":memory:" for an in-memory database.
            String url = "jdbc:sqlite:my_database.db"; // Creates/connects to my_database.db in the project directory

            // Explicitly loading the driver is often not needed in modern Java/JDBC,
            // but some environments might require it.
            // Class.forName("org.sqlite.JDBC");

            // Create a connection to the database
            conn = DriverManager.getConnection(url);

            System.out.println("Connection to SQLite has been established.");

        } catch (SQLException e) {
            System.err.println("Error connecting to the database: " + e.getMessage());
        } finally {
            try {
                if (conn != null) {
                    conn.close();
                    System.out.println("Connection closed.");
                }
            } catch (SQLException ex) {
                System.err.println("Error closing the connection: " + ex.getMessage());
            }
        }
    }
}