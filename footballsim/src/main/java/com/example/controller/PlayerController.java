package com.example.controller;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.model.Player;
import com.example.service.PlayerService;

@RestController
@RequestMapping("/players")
public class PlayerController {

    private final PlayerService playerService;

    public PlayerController(PlayerService playerService) {
        this.playerService = playerService;
    }

    @GetMapping
    public Page<Player> getAllPlayers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return playerService.getAllPlayers(page, size);
    }

    // GET /players/by-name?name=Messi
    @GetMapping("/name")
    public List<Player> getPlayersByName(@RequestParam String name) {
        return playerService.getPlayersByName(name);
    }

    // GET /players/by-nationality?nationality=Argentina
    @GetMapping("/nationality")
    public List<Player> getPlayersByNationality(@RequestParam String nationality) {
        return playerService.getPlayersByNationality(nationality);
    }

}
