from models.models import Attributes


class Player:
    """Player class"""

    def __init__(
        self,
        uid: str,
        name: str,
        age: int,
        nationalities: list[str],
        attributes: Attributes,
        position=None,
        current_ability=0,
        team="",
        league="",
        price=100,
        stats=None,
        form=None,
    ):
        self.uid = uid
        self.name = name
        self.age = age
        self.nationalities = nationalities
        self.team = team
        self.league = league
        self.price = price
        self.attributes = attributes
        self.stats = [] if stats is None else stats
        self.form = [] if form is None else form
        if position is None:
            self.position, self.current_ability = (
                self.calculate_best_position_and_ability()
            )
        else:
            self.position = position
            self.current_ability = current_ability

    def assign_team(self, team):
        """
        Assign team to a player
        """
        self.team = team

    def increment_age(self):
        """
        Update age each season
        """
        self.age += 1

    def update_price(self, new_price):
        """
        Update price of the player
        """
        self.price = new_price

    def calculate_best_position_and_ability(self) -> str:
        """Get the best position of player"""
        all_technical = [
            self.attributes.technical.Crossing,
            self.attributes.technical.Dribbling,
            self.attributes.technical.Finishing,
            self.attributes.technical.FirstTouch,
            self.attributes.technical.FreeKickTaking,
            self.attributes.technical.Heading,
            self.attributes.technical.Long_Shots,
            self.attributes.technical.Long_Throws,
            self.attributes.technical.Marking,
            self.attributes.technical.Passing,
            self.attributes.technical.Tackling,
        ]
        all_mental = [
            self.attributes.mental.Aggression,
            self.attributes.mental.Bravery,
            self.attributes.mental.Composure,
            self.attributes.mental.Concentration,
            self.attributes.mental.Decisions,
            self.attributes.mental.Determination,
            self.attributes.mental.Flair,
            self.attributes.mental.Leadership,
            self.attributes.mental.Positioning,
            self.attributes.mental.Teamwork,
            self.attributes.mental.Vision,
            self.attributes.mental.WorkRate,
        ]
        all_physical = [
            self.attributes.physical.NaturalFitness,
            self.attributes.physical.Pace,
            self.attributes.physical.Stamina,
            self.attributes.physical.Strength,
        ]
        all_gk = [
            self.attributes.gk.GKDiving,
            self.attributes.gk.GKHandling,
            self.attributes.gk.GKKicking,
            self.attributes.gk.GKPositioning,
            self.attributes.gk.GKReflexes,
        ]

        # Define positions with primary, secondary, and tertiary attributes
        positions = {
            "GK": {
                "primary": [
                    self.attributes.gk.GKDiving,
                    self.attributes.gk.GKHandling,
                    self.attributes.gk.GKKicking,
                    self.attributes.gk.GKPositioning,
                    self.attributes.gk.GKReflexes,
                ],
                "secondary": [
                    self.attributes.mental.Concentration,
                    self.attributes.mental.Composure,
                ],
            },
            "CB": {
                "primary": [
                    self.attributes.technical.Marking,
                    self.attributes.technical.Tackling,
                    self.attributes.technical.Heading,
                ],
                "secondary": [
                    self.attributes.physical.Strength,
                    self.attributes.mental.Positioning,
                ],
            },
            "FB": {
                "primary": [
                    self.attributes.technical.Crossing,
                    self.attributes.technical.Marking,
                    self.attributes.technical.Tackling,
                ],
                "secondary": [
                    self.attributes.physical.Pace,
                    self.attributes.physical.Stamina,
                    self.attributes.mental.Teamwork,
                ],
            },
            "DM": {
                "primary": [
                    self.attributes.mental.Positioning,
                    self.attributes.technical.Marking,
                    self.attributes.technical.Tackling,
                ],
                "secondary": [
                    self.attributes.mental.Vision,
                    self.attributes.technical.Passing,
                    self.attributes.physical.Stamina,
                ],
            },
            "HM": {
                "primary": [
                    self.attributes.technical.Passing,
                    self.attributes.mental.Decisions,
                ],
                "secondary": [
                    self.attributes.mental.Teamwork,
                    self.attributes.physical.Stamina,
                    self.attributes.mental.Composure,
                ],
            },
            "CAM": {
                "primary": [
                    self.attributes.technical.Passing,
                    self.attributes.technical.Finishing,
                    self.attributes.mental.Vision,
                ],
                "secondary": [
                    self.attributes.mental.Flair,
                    self.attributes.technical.Dribbling,
                    self.attributes.technical.FirstTouch,
                ],
            },
            "W": {
                "primary": [
                    self.attributes.technical.Crossing,
                    self.attributes.technical.Dribbling,
                    self.attributes.physical.Pace,
                ],
                "secondary": [
                    self.attributes.mental.Positioning,
                    self.attributes.mental.Flair,
                    self.attributes.technical.Passing,
                ],
            },
            "ST": {
                "primary": [
                    self.attributes.technical.Finishing,
                    self.attributes.technical.FirstTouch,
                    self.attributes.mental.Composure,
                ],
                "secondary": [
                    self.attributes.technical.Dribbling,
                    self.attributes.mental.Positioning,
                    self.attributes.physical.Strength,
                ],
            },
        }

        # Calculate tertiary attributes (all remaining)
        for position, attributes in positions.items():
            used_attrs = attributes["primary"] + attributes["secondary"]
            attributes["tertiary"] = [
                attr
                for attr in (all_technical + all_mental + all_physical + all_gk)
                if attr not in used_attrs
            ]

        # Calculate scores for all positions
        scores = {}
        for position, attributes in positions.items():
            if position != "Goalkeeper (GK)":
                primary_score = sum(attributes["primary"]) * 0.6
                secondary_score = sum(attributes["secondary"]) * 0.3
                tertiary_score = sum(attributes["tertiary"]) * 0.1
                scores[position] = primary_score + secondary_score + tertiary_score
            else:
                primary_score = sum(attributes["primary"]) * 0.7
                secondary_score = sum(attributes["secondary"]) * 0.3
                scores[position] = primary_score + secondary_score
        # Get the position with the highest score
        best_position = max(scores, key=scores.get)
        return best_position, scores[best_position]

    def initialize_stats(self, season_id):
        """
        Initialize stats for the player
        """
        self.stats = []
        self.stats.append(
            {
                f"season {season_id}": {
                    "appearances": 0,
                    "goals": 0,
                    "assists": 0,
                    "yellow_cards": 0,
                    "red_cards": 0,
                    "motm": 0,
                    "avg_rating": 0,
                }
            }
        )

    def to_dict(self):
        """Convert player to dictionary"""
        return {
            "uid": self.uid,
            "name": self.name,
            "age": self.age,
            "nationalities": self.nationalities,
            "attributes": self.attributes.model_dump_json(),
            "position": self.position,
            "current_ability": self.current_ability,
            "team": self.team.to_dict() if self.team else "",
            "price": self.price,
            "stats": self.stats,
            "form": self.form,
        }
