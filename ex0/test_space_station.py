import json
from pathlib import Path
import pytest
from pydantic import ValidationError

# 本番コードからクラスをインポート（同じex0フォルダ内なので直接書ける）
from space_station import SpaceStation

# ルートディレクトリにある generated_data へのパスを作成
DATA_DIR = Path(__file__).resolve().parent.parent / "generated_data"


def get_data(filename: str):
    """JSONファイルからデータを読み込むヘルパー関数"""
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# 1. 正常なステーションの自動生成データ（10件等）を一斉にテスト
@pytest.mark.parametrize("data", get_data("space_stations.json"))
def test_valid_space_station(data):
    station = SpaceStation(**data)
    assert station.station_id == data["station_id"]
    assert station.is_operational == data["is_operational"]


# 2. わざとエラーになる異常データが、正しくバリデーションで弾かれるかテスト
@pytest.mark.parametrize("data", get_data("invalid_stations.json"))
def test_invalid_space_station_must_fail(data):
    # 「この中に書いた処理で、ちゃんと ValidationError が起これば合格！」という意味
    with pytest.raises(ValidationError):
        SpaceStation(**data)