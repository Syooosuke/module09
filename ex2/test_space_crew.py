import json
from pathlib import Path
import pytest
from pydantic import ValidationError

from space_crew import SpaceMission

DATA_DIR = Path(__file__).resolve().parent.parent / "generated_data"


def get_data(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# ネストされた構造（ミッションの中のクルーメンバー）の自動バリデーションテスト
@pytest.mark.parametrize("data", get_data("space_missions.json"))
def test_valid_space_mission(data):
    mission = SpaceMission(**data)
    assert mission.mission_id.startswith("M")
    # クルーが最低1人以上、12人以下で格納されているか
    assert 1 <= len(mission.crew) <= 12