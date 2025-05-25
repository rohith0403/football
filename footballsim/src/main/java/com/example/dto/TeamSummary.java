package com.example.dto;

// DTO class inside the service to hold limited data (id and name only)
public class TeamSummary {
    private Long id;
    private String name;
    private String league;

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getLeague() {
        return league;
    }

    public TeamSummary(Long id, String name, String league) {
        this.id = id;
        this.name = name;
        this.league = league;
    }
}