package com.example;

import com.example.model.Goalkeeper;
import com.example.model.Player;
import com.github.javafaker.Faker;

public class PlayerFactory {

    private static final Faker faker = new Faker();

    public static Player createRandomPlayer() {
        String name = faker.name().firstName() + " " + faker.name().lastName();
        String nationality = faker.country().name();
        int attack = faker.number().numberBetween(1, 10);
        int midfield = faker.number().numberBetween(1, 10);
        int defense = faker.number().numberBetween(1, 10);

        return new Player(name, nationality, "", attack, midfield, defense);
    }

    // Optionally add more methods for specific player types
    public static Player createDefender() {
        return new Player(
                faker.name().fullName(),
                faker.country().name(),
                "DEFENDER",
                faker.number().numberBetween(10, 40), // low attack
                faker.number().numberBetween(30, 60), // average midfield
                faker.number().numberBetween(70, 100) // high defense
        );
    }

    public static Player createAttacker() {
        return new Player(
                faker.name().fullName(),
                faker.country().name(),
                "ATTACKER",
                faker.number().numberBetween(70, 100), // high attack
                faker.number().numberBetween(30, 60),
                faker.number().numberBetween(10, 40));
    }

    public static Player createMidfielder() {
        return new Player(
                faker.name().fullName(),
                faker.country().name(),
                "MIDFIELDER",
                faker.number().numberBetween(30, 60),
                faker.number().numberBetween(70, 100), // high midfield
                faker.number().numberBetween(10, 60));
    }

    public static Player createGoalkeeper() {
        return new Goalkeeper(
                faker.name().fullName(),
                faker.country().name(),
                "GOALKEEPER",
                faker.number().numberBetween(50, 100),
                faker.number().numberBetween(50, 100),
                faker.number().numberBetween(50, 100)); // high defense
    }
}
