from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        is_physical = self.contact_type == ContactType.PHYSICAL
        if is_physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        is_telepanic = self.contact_type == ContactType.TELEPATHIC
        if is_telepanic and self.witness_count < 3:
            raise ValueError("Telepanic contact needs at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            err_msg = "Strong signals (> 7.0) must include a message"
            raise ValueError(err_msg)

        return self


def main() -> None:
    print("Alien Contact Log Validation\n")

    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2026-06-17T23:00:00",
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greeting from Zeta Reticuli",
        )
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'\n")

    except ValidationError as e:
        print(f"Unexpected error: {e}")

    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2026-06-17T23:30:00",
            location="42Tokyo",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=2,
            is_verified=True,
        )
    except ValidationError as e:
        print("Expected validation error:")
        err = e.errors()[0]
        msg = err.get("ctx", {}).get("error", err["msg"])
        print(msg)


if __name__ == "__main__":
    main()
