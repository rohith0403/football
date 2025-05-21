package com.example.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

@Entity
@DiscriminatorValue("GOALKEEPER")
public class Goalkeeper extends Player {
    private int diving;
    private int handling;
    private int reflexes;

    public Goalkeeper() {
        super();
    }

    public Goalkeeper(String name, String nationality, String position, int diving, int handling, int reflexes) {
        super(name, nationality, position);
        this.diving = diving;
        this.handling = handling;
        this.reflexes = reflexes;
    }

    public int getDiving() {
        return diving;
    }

    public void setDiving(int diving) {
        this.diving = diving;
    }

    public int getHandling() {
        return handling;
    }

    public void setHandling(int handling) {
        this.handling = handling;
    }

    public int getReflexes() {
        return reflexes;
    }

    public void setReflexes(int reflexes) {
        this.reflexes = reflexes;
    }

    // getters and setters
}
