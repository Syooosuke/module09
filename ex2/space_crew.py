from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_million_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        for member in self.crew:
            if not member.is_active:
                err_msg = f"Crew member {member.name} is not active"
                raise ValueError(err_msg)

        has_leader = any(
            m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew
        )
        if not has_leader:
            err_msg = "Mission must have at least one Commander or Captain"
            raise ValueError(err_msg)

        if self.duration_days > 365:
            exp_crew = sum(1 for m in self.crew if m.years_experience >= 5)

            if (exp_crew / len(self.crew)) < 0.5:
                err_msg = "Long missions need 50% experienced crew (5+ years)"
                raise ValueError(err_msg)

        return self


def main() -> None:
    print("Space Mission Crew Validation\n")

    commander = CrewMember(
        member_id="C001",
        name="Sarah Conor",
        rank=Rank.COMMANDER,
        age=45,
        specialization="Mission Command",
        years_experience=15,
    )
    cadet = CrewMember(
        member_id="C002",
        name="John Smith",
        rank=Rank.CADET,
        age=22,
        specialization="Navigation",
        years_experience=1,
    )
    officer = CrewMember(
        member_id="C003",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=22,
        specialization="Engineering",
        years_experience=10,
    )
    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-08-01T00:00:00"),
            duration_days=900,
            crew=[commander, cadet, officer],
            budget_millions=2500.0,
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for m in valid_mission.crew:
            print(f"- {m.name} ({m.rank.value}) : {m.specialization}")
        print()

    except ValidationError as e:
        print(f"Unexpected error: {e}\n")

    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Bae Setup",
            destination="Moon",
            launch_date=datetime.fromisoformat("2026-09-01T00:00:00"),
            duration_days=30,
            crew=[cadet],
            budget_millions=500.0,
        )
    except ValidationError as e:
        print("Expected validation error:")
        err = e.errors()[0]
        msg = err.get("ctx", {}).get("error", err["msg"])
        print(msg)


if __name__ == "__main__":
    main()
