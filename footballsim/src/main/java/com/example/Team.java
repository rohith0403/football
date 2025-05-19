package com.example;

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;

public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "name")
    private String name;

    @Column(name = "league")
    private String league;

    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL, orphanRemoval = false)
    private List<Player> squad = new ArrayList<>();
    
    
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
        // Generate attributes for the team
        // This is just a placeholder method. You can implement your own logic here.
        System.out.println("Generating attributes for team: " + this.name);
    }
    
}
