import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from classes.League import League
from db.store import (
    create_new_season,
    create_tables,
    fetch_league_history_from_season_table,
    fetch_season_id,
    fetch_teams_from_season_table,
    update_offense_defense_ratings_for_new_season,
    wipe_season_data,
)
from generators.team_generator import initialize_teams


class FootballLeagueSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Football League Simulation")

        # Initialize main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.splitter = QSplitter()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.splitter)
        self.main_widget.setLayout(self.main_layout)

        # Sidebar (left column)
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget.setLayout(self.sidebar_layout)

        # Add icon buttons to the left column
        self.icon_button_1 = QPushButton()
        self.icon_button_1.setIcon(QIcon("icons/league.png"))
        self.icon_button_1.setIconSize(QSize(32, 42))
        self.icon_button_1.clicked.connect(
            lambda: self.update_content("League Content")
        )
        self.sidebar_layout.addWidget(self.icon_button_1)

        self.icon_button_2 = QPushButton()
        self.icon_button_2.setIcon(QIcon("icons/teams.png"))
        self.icon_button_2.setIconSize(QSize(32, 42))
        self.icon_button_2.clicked.connect(lambda: self.update_content("Teams Content"))
        self.sidebar_layout.addWidget(self.icon_button_2)

        self.icon_button_3 = QPushButton()
        self.icon_button_3.setIcon(QIcon("icons/players.png"))
        self.icon_button_3.setIconSize(QSize(32, 42))
        self.icon_button_3.clicked.connect(
            lambda: self.update_content("Players Content")
        )
        self.sidebar_layout.addWidget(self.icon_button_3)

        self.sidebar_layout.addStretch()

        # Add sidebar to the splitter
        self.splitter.addWidget(self.sidebar_widget)

        # Right column: Main content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        # Add main content area to the splitter
        self.splitter.addWidget(self.content_widget)

        # Configure the splitter sizes (20% for sidebar, 80% for main content)
        self.splitter.setSizes([100, 900])  # Adjust values as necessary

        # Add default content
        self.default_label = QLabel("Welcome to the Football League Simulation!")
        self.content_layout.addWidget(self.default_label)

        # Initialize state variables
        self.current_content = None
        self.current_season_id = None
        self.league = None

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                print(f"Removing widget: {widget.objectName()}")
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                print("Clearing nested layout")
                self.clear_layout(item.layout())

    def update_content(self, content):
        """Update the main content widget based on the selected icon."""
        if self.current_content == content:
            return

        self.clear_layout(self.content_layout)

        self.current_content = content
        if content == "League Content":
            # Additional action buttons
            self.button_layout = QHBoxLayout()
            self.content_layout.addLayout(self.button_layout)

            self.initialize_db_button = QPushButton("Initialize DB")
            self.initialize_db_button.clicked.connect(self.initialize_db)
            self.button_layout.addWidget(self.initialize_db_button)

            self.new_season_button = QPushButton("Generate New Season")
            self.new_season_button.clicked.connect(self.generate_new_season)
            self.button_layout.addWidget(self.new_season_button)

            self.run_season_button = QPushButton("Run Season")
            self.run_season_button.clicked.connect(self.run_season)
            self.run_season_button.setEnabled(False)  # Initially disabled
            self.button_layout.addWidget(self.run_season_button)

            # Dropdown for selecting seasons
            self.season_selector = QComboBox()
            self.season_selector.currentIndexChanged.connect(
                self.update_gameweek_slider
            )
            self.season_selector.currentIndexChanged.connect(self.update_league_table)
            self.content_layout.addWidget(self.season_selector)

            # Slider for selecting game weeks
            self.gameweek_slider = QSlider(Qt.Orientation.Horizontal)
            self.gameweek_slider.setEnabled(False)
            self.gameweek_slider.valueChanged.connect(self.update_league_table)
            self.content_layout.addWidget(self.gameweek_slider)

            # League Table Display
            self.league_table = QTableWidget()
            self.content_layout.addWidget(self.league_table)

        else:
            # Fallback content for other icons
            new_label = QLabel(content)
            new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(new_label)

    def fetch_initial_state(self):
        """Fetch the initial state for the application."""
        self.current_season_id = fetch_season_id()
        teams = fetch_teams_from_season_table(self.current_season_id)
        self.league = League(teams)
        self.update_season_selector()

    def initialize_db(self):
        """Refresh the database."""
        wipe_season_data()
        create_tables()
        # self.fetch_initial_state()
        self.run_season_button.setEnabled(False)

    def generate_new_season(self):
        """Generate a new season."""
        create_new_season()
        new_season_id = fetch_season_id()
        if new_season_id == 1:
            initialize_teams(new_season_id)
        else:
            update_offense_defense_ratings_for_new_season(
                new_season_id - 1, new_season_id
            )
        self.fetch_initial_state()
        self.run_season_button.setEnabled(True)

    def run_season(self):
        """Run the current season."""
        if self.league:
            self.league.run_season(self.current_season_id)
            self.run_season_button.setEnabled(False)
            self.update_league_table()
            self.update_gameweek_slider()

    def update_season_selector(self):
        """Update the season selector dropdown."""
        self.season_selector.clear()
        for i in range(self.current_season_id):
            self.season_selector.addItem(f"Season {i + 1}")
        self.update_league_table()

    def update_gameweek_slider(self):
        """Update the game week slider based on the selected season."""
        selected_season = self.season_selector.currentIndex() + 1
        selected_season_data = fetch_league_history_from_season_table(selected_season)
        self.gameweek_slider.setMaximum(len(selected_season_data))
        self.gameweek_slider.setMinimum(1)
        self.gameweek_slider.setValue(len(selected_season_data))
        self.gameweek_slider.setEnabled(True)

    def update_league_table(self):
        """Update the league table display."""
        selected_season = self.season_selector.currentIndex() + 1
        selected_season_data = fetch_league_history_from_season_table(selected_season)
        if len(selected_season_data) > 0:
            selected_gameweek = self.gameweek_slider.value()
            selected_week_snapshot = selected_season_data[selected_gameweek - 1]
            self.league_table.clear()
            self.league_table.setRowCount(len(selected_week_snapshot))
            self.league_table.setColumnCount(8)
            self.league_table.setHorizontalHeaderLabels(
                [
                    "Team",
                    "Points",
                    "Wins",
                    "Draws",
                    "Losses",
                    "Goals Scored",
                    "Goals Conceded",
                    "Form",
                ]
            )
            sorted_teams = sorted(
                selected_week_snapshot, key=lambda x: x["points"], reverse=True
            )
            for row_idx, team in enumerate(sorted_teams):
                self.league_table.setItem(row_idx, 0, QTableWidgetItem(team["name"]))
                self.league_table.setItem(
                    row_idx, 1, QTableWidgetItem(str(team["points"]))
                )
                self.league_table.setItem(
                    row_idx, 2, QTableWidgetItem(str(team["wins"]))
                )
                self.league_table.setItem(
                    row_idx, 3, QTableWidgetItem(str(team["draws"]))
                )
                self.league_table.setItem(
                    row_idx, 4, QTableWidgetItem(str(team["losses"]))
                )
                self.league_table.setItem(
                    row_idx, 5, QTableWidgetItem(str(team["goals_scored"]))
                )
                self.league_table.setItem(
                    row_idx, 6, QTableWidgetItem(str(team["goals_against"]))
                )
                self.league_table.setItem(
                    row_idx,
                    7,
                    QTableWidgetItem(
                        ", ".join(team["form"])
                        if isinstance(team["form"], list)
                        else str(team["form"])
                    ),
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = FootballLeagueSimulator()
    simulator.show()
    sys.exit(app.exec())
