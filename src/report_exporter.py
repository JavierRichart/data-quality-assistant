import json
from pathlib import Path

from src.analyzer import AnalysisReport


def report_to_dict(report: AnalysisReport) -> dict:
    return {
        "summary": {
            "total_rows": report.total_rows,
            "total_columns": report.total_columns,
            "is_valid": report.is_valid,
            "error_count": report.error_count,
            "quality_score": report.quality_score,
            "quality_level": report.quality_level,
        },
        "validation_results": [
            {
                "name": result.name,
                "passed": result.passed,
                "details": result.details,
            }
            for result in report.validation_results
        ],
    }


def export_report_to_json(
    report: AnalysisReport,
    output_path: str | Path,
) -> Path:
    output_path = Path(output_path)

    report_data = report_to_dict(report)

    with output_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report_data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    return output_path