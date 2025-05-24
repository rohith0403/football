package com.example.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.Query;

@Service
public class TeamService {

    @PersistenceContext
    private EntityManager entityManager;

    // DTO class inside the service to hold limited data (id and name only)
    public static class TeamSummary {
        private Long id;
        private String name;
        private String league;

        public TeamSummary(Long id, String name, String league) {
            this.id = id;
            this.name = name;
            this.league = league;
        }
    }

    public List<TeamSummary> getTeamSummaries() {
        // Native query selecting only id and name columns
        Query query = entityManager.createNativeQuery("SELECT id, name, league FROM teams");

        // Result list from query
        List<Object[]> results = query.getResultList();

        // Map each result to TeamSummary DTO
        List<TeamSummary> summaries = new ArrayList<>();
        for (Object[] row : results) {
            Long id = ((Number) row[0]).longValue();
            String name = (String) row[1];
            String league = (String) row[2];
            summaries.add(new TeamSummary(id, name, league));
        }

        return summaries;
    }
}
