import json
from pathlib import Path
import pytest
from pydantic import ValidationError

from alien_contact import AlienContact

DATA_DIR = Path(__file__).resolve().parent.parent / "generated_data"


def get_data(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("data", get_data("alien_contacts.json"))
def test_valid_alien_contact(data):
    contact = AlienContact(**data)
    # 独自ルール（IDは必ずACから始まる）が機能しているか再確認
    assert contact.contact_id.startswith("AC")


@pytest.mark.parametrize("data", get_data("invalid_contacts.json"))
def test_invalid_alien_contact_must_fail(data):
    with pytest.raises(ValidationError):
        AlienContact(**data)