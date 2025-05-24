package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.model.Team;

@Repository
public interface TeamRepository extends JpaRepository<Team, Long> {
    // No method implementations needed here
    // You get CRUD methods like save(), findById(), findAll(), deleteById(), etc.
    // for free
}
