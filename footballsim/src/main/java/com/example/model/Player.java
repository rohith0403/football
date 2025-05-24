package com.example.model;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.Column;
import jakarta.persistence.DiscriminatorColumn;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Inheritance;
import jakarta.persistence.InheritanceType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "players")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE) // or JOINED or TABLE_PER_CLASS
@DiscriminatorColumn(name = "player_type")
public class Player {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "name")
    private String name;

    @Column(name = "nationality")
    private String nationality;

    @Column(name = "attack")
    private int attack;

    @Column(name = "midfield")
    private int midfield;

    @Column(name = "defense")
    private int defense;

    @Column(name = "position")
    private String position;

    // This defines the many-to-one relationship from Player to Team.
    // This is the owning side, so the foreign key will be in the 'players' table.
    @ManyToOne(fetch = FetchType.LAZY) // Many players belong to one team. Lazy fetching is default and good.
    @JoinColumn(name = "team_id", nullable = true) // This creates the 'team_id' foreign key column in the 'players'
                                                   // table
    @JsonBackReference // This prevents infinite recursion when serializing to JSON
    private Team team; // The field that holds the reference to the Team entity

    public Team getTeam() {
        return this.team;
    }

    public void setTeam(Team team) {
        this.team = team;
    }

    public long getId() {
        return this.id;
    }

    public Player() {
        // no-arg constructor required by Hibernate
    }

    public Player(String name, String nationality, String position) {
        this.name = name;
        this.nationality = nationality;
        this.position = position;
    }

    public Player(String name, String nationality, String position, int attack, int midfield, int defense) {
        this.name = name;
        this.nationality = nationality;
        this.position = position;
        this.attack = attack;
        this.midfield = midfield;
        this.defense = defense;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getNationality() {
        return this.nationality;
    }

    public void setNationality(String nationality) {
        this.nationality = nationality;
    }

    public Integer getAttack() {
        return this.attack;
    }

    public void setAttack(int attack) {
        this.attack = attack;
    }

    public Integer getDefense() {
        return this.defense;
    }

    public void setDefense(int defense) {
        this.defense = defense;
    }

    public int getMidfield() {
        return this.midfield;
    }

    public void setMidfield(int midfield) {
        this.midfield = midfield;
    }

    public String getPosition() {
        return this.position;
    }

    public void setPosition(String position) {
        this.position = position;
    }
}
