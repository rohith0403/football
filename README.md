# ⚽ Football Match Engine

## Overview

This is a command-line football league simulation application that models clubs, players, and league seasons. It simulates matches based on aggregated club and player attributes, tracks league standings across multiple seasons, and includes basic player dynamics like morale and injuries.

## 🎯 Project Goals

- Model realistic football clubs and players with core attributes.
- Simulate matches with simplified logic and randomized outcomes.
- Track league standings over multiple seasons.
- Incorporate simple player dynamics: injuries and morale.
- Provide console-based outputs for match results and standings.

---

## 📦 Core Features

### 🧩 Data Model

#### Player Entity
- **Attributes**:
  - `Attack`
  - `Defence`
  - `Stamina`
  - `Morale`
  - `Injury Status`

#### Club Entity
- **Attributes**:
  - Derived from aggregated attributes of all current players.

---

### ⚔️ Match Simulation

- Compare aggregated club stats to determine match outcome.
- Incorporate randomness for realism.
- Factor in:
  - Player morale
  - Injury status (reducing effectiveness)
- Output:
  - Match scorecard
  - Basic match report (e.g., goals scored)

---

### 🏆 League Simulation

- Full league season with round-robin structure (e.g., home & away).
- Track standings with:
  - Points
  - Wins, Draws, Losses
  - Goals For / Against
  - Goal Difference
- Update standings after each match.

---

### 🔄 Multi-Season Progression

- Persist clubs and players across seasons.
- Player attributes:
  - Slight improvement or decline per season.
- Transfer Window:
  - Random or basic player transfers in off-season.

---

### 🧠 Player Dynamics

- **Injuries**:
  - Varying duration
  - Reduce effectiveness or sideline players

- **Morale System**:
  - Influenced by match results
  - Affects match performance

---

## 📤 Output

- Final league standings at the end of each season.
- Match results available for:
  - A specific week
  - A specific club

---

## 🛠️ Technology Stack

| Component         | Technology           |
|------------------|----------------------|
| Programming      | Java                 |
| ORM              | Hibernate            |
| Database         | PostgreSQL           |
| Build Tool       | Maven or Gradle      |
| Testing          | JUnit                |
| Logging          | SLF4j + Logback/Log4j2 |

---

## 🔧 Development Scope (2 Weeks)

- Command-line interface (CLI)
- No GUI
- No Spring Boot or web frameworks
- Focus on:
  - Data modeling
  - Simulation logic
  - Persistence layer

---

## 🧩 Out of Scope (Future Enhancements)

- Play-by-play match simulation
- Tactical systems/formations
- Player positions/roles
- Youth academies or player generation
- Financial systems or advanced transfers
- Real-time simulation
- GUI

---

## 🚀 Getting Started (Suggested Steps)

1. **Design Data Models**: Player and Club entities.
2. **Build Match Simulation Logic**: Including morale and injury factors.
3. **Create League Engine**: Schedule fixtures, simulate season.
4. **Implement Multi-Season Logic**: Attribute evolution, transfers.
5. **Set Up Hibernate + PostgreSQL**: For persistent storage.
6. **CLI Interface**: For running simulations and viewing results.
7. **Testing & Logging**: Add JUnit tests and logging framework.

---

## 📚 Learning Outcomes

- Master object-oriented design for simulation modeling.
- Learn Hibernate and database integration.
- Practice simulation logic and probability handling.
- Explore multi-season game logic and state management.

---

## 📄 License

This project is for educational purposes and not intended for commercial use. Feel free to modify and expand for learning or personal projects.

