import datetime as dt
import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src import reports, utils, views


def test_load_transactions_success(tmp_path, sample_excel_file):
    with patch.dict(os.environ, {"TRANSACTIONS_FILE": sample_excel_file}):
        df = utils.load_transactions()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "col1" in df.columns


def test_load_transactions_error():
    # Тестируем ошибку при чтении файла
    with patch.dict(os.environ, {"TRANSACTIONS_FILE": "nonexistent.xlsx"}):
        with pytest.raises(FileNotFoundError):
            utils.load_transactions()


@pytest.mark.parametrize(
    "date_str,period,expected_start,expected_end",
    [
        ("2024-04-15 10:00:00", "W", dt.datetime(2024, 4, 15), dt.datetime(2024, 4, 15)),
        ("2024-04-15 10:00:00", "M", dt.datetime(2024, 4, 1), dt.datetime(2024, 4, 15)),
        ("2024-04-15 10:00:00", "Y", dt.datetime(2024, 1, 1), dt.datetime(2024, 4, 15)),
        ("2024-04-15 10:00:00", "ALL", dt.datetime(1970, 1, 1), dt.datetime(2024, 4, 15)),
    ],
)
def test_get_date_range(date_str, period, expected_start, expected_end):
    start, end = utils.get_date_range(date_str, period)
    assert start == expected_start
    assert end == expected_end


def test_get_date_range_invalid_period():
    with pytest.raises(ValueError):
        utils.get_date_range("2024-04-15 10:00:00", "INVALID")


@patch("requests.get")
def test_get_currency_rates_from_api_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "rates": {
            "USD": 1.0,
            "EUR": 0.85,
        }
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    result = utils.get_currency_rates_from_api(["USD", "EUR", "JPY"])
    assert isinstance(result, list)
    assert any(d["currency"] == "USD" for d in result)
    assert any(d["currency"] == "EUR" for d in result)
    # Валюта JPY отсутствует, должна быть None
    assert any(d["rate"] is None for d in result if d["currency"] == "JPY")


@patch("requests.get")
def test_get_currency_rates_from_api_failure(mock_get):
    mock_get.side_effect = Exception("API error")
    result = utils.get_currency_rates_from_api(["USD"])
    assert result == []
