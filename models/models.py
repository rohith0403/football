from pydantic import BaseModel, Field


class Technical(BaseModel):
    Corners: int = Field(..., ge=1, le=20)
    Crossing: int = Field(..., ge=1, le=20)
    Dribbling: int = Field(..., ge=1, le=20)
    Finishing: int = Field(..., ge=1, le=20)
    FirstTouch: int = Field(..., ge=1, le=20)
    FreeKickTaking: int = Field(..., ge=1, le=20)
    Heading: int = Field(..., ge=1, le=20)
    Long_Shots: int = Field(..., ge=1, le=20)
    Long_Throws: int = Field(..., ge=1, le=20)
    Marking: int = Field(..., ge=1, le=20)
    Passing: int = Field(..., ge=1, le=20)
    Penalty_Taking: int = Field(..., ge=1, le=20)
    Tackling: int = Field(..., ge=1, le=20)
    Technique: int = Field(..., ge=1, le=20)


class Mental(BaseModel):
    Aggression: int = Field(..., ge=1, le=20)
    Anticipation: int = Field(..., ge=1, le=20)
    Bravery: int = Field(..., ge=1, le=20)
    Composure: int = Field(..., ge=1, le=20)
    Concentration: int = Field(..., ge=1, le=20)
    Decisions: int = Field(..., ge=1, le=20)
    Determination: int = Field(..., ge=1, le=20)
    Flair: int = Field(..., ge=1, le=20)
    Leadership: int = Field(..., ge=1, le=20)
    OffTheBall: int = Field(..., ge=1, le=20)
    Positioning: int = Field(..., ge=1, le=20)
    Teamwork: int = Field(..., ge=1, le=20)
    Vision: int = Field(..., ge=1, le=20)
    WorkRate: int = Field(..., ge=1, le=20)


class Physical(BaseModel):
    Acceleration: int = Field(..., ge=1, le=20)
    Agility: int = Field(..., ge=1, le=20)
    Balance: int = Field(..., ge=1, le=20)
    JumpingReach: int = Field(..., ge=1, le=20)
    NaturalFitness: int = Field(..., ge=1, le=20)
    Pace: int = Field(..., ge=1, le=20)
    Stamina: int = Field(..., ge=1, le=20)
    Strength: int = Field(..., ge=1, le=20)


class GK(BaseModel):
    GKDiving: int = Field(..., ge=1, le=20)
    GKHandling: int = Field(..., ge=1, le=20)
    GKKicking: int = Field(..., ge=1, le=20)
    GKPositioning: int = Field(..., ge=1, le=20)
    GKReflexes: int = Field(..., ge=1, le=20)


class Intrinsic(BaseModel):
    Confidence: int = Field(..., ge=1, le=20)  # Ability to get out of a slump
    Consistency: int = Field(..., ge=1, le=20)  # Ability to continue good form
    Proffesionalism: int = Field(..., ge=1, le=20)  # Ability to be proffessional
    BigGamePlayer: int = Field(..., ge=1, le=20)  # Ability to perform in big games
    Loyalty: int = Field(..., ge=1, le=20)  # Loyalty to club or nation
    CareerAmbition: int = Field(..., ge=1, le=20)  # Lust for Trophy
    MoneyAmbition: int = Field(..., ge=1, le=20)  # Lust for money


class Attributes(BaseModel):
    technical: Technical
    mental: Mental
    physical: Physical
    gk: GK
    intrinsic: Intrinsic
