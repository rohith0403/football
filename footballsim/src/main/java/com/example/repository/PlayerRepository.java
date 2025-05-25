package com.example.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.model.Player;

@Repository
public interface PlayerRepository extends JpaRepository<Player, Long> {
    // No method implementations needed here
    // You get CRUD methods like save(), findById(), findAll(), deleteById(), etc.
    // for free
    List<Player> findByNameContainingIgnoreCase(String name);

    List<Player> findByNationalityContainingIgnoreCase(String nationality);
}
