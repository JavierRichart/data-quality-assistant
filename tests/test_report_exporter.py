import pandas as pd

from src.analyzer import AnalysisReport
from src.report_exporter import (
    export_report_to_json,
    report_to_dict,
)
from src.validation_result import ValidationResult


def test_report_to_dict_returns_expected_structure():
    report = AnalysisReport(
        dataframe=pd.DataFrame(
            {
                "nombre": ["Ana", "Luis"],
                "edad": [30, 40],
            }
        ),
        validation_results=[
            ValidationResult(
                name="required_columns",
                passed=True,
                details=[],
            ),
            ValidationResult(
                name="null_data",
                passed=False,
                details={
                    "nombre": 0,
                    "edad": 1,
                },
            ),
        ],
    )

    result = report_to_dict(report)

    assert result["summary"]["total_rows"] == 2
    assert result["summary"]["total_columns"] == 2
    assert result["summary"]["is_valid"] is False
    assert result["summary"]["error_count"] == 1

    assert result["validation_results"] == [
        {
            "name": "required_columns",
            "passed": True,
            "details": [],
        },
        {
            "name": "null_data",
            "passed": False,
            "details": {
                "nombre": 0,
                "edad": 1,
            },
        },
    ]

import json


def test_export_report_to_json_creates_file(tmp_path):
    report = AnalysisReport(
        dataframe=pd.DataFrame(
            {
                "nombre": ["Ana"],
                "edad": [30],
            }
        ),
        validation_results=[
            ValidationResult(
                name="required_columns",
                passed=True,
                details=[],
            )
        ],
    )

    output_path = tmp_path / "analysis_report.json"

    created_path = export_report_to_json(
        report,
        output_path,
    )

    assert created_path == output_path
    assert output_path.exists()

    with output_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        content = json.load(file)

    assert content["summary"]["total_rows"] == 1
    assert content["summary"]["total_columns"] == 2
    assert content["validation_results"][0]["name"] == "required_columns"