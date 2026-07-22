import json

from src.analyzer import AnalysisReport
from src.report_exporter import report_to_dict


SYSTEM_INSTRUCTIONS = """
Eres un especialista en calidad de datos.

Tu tarea es analizar un informe de validación y:

1. Resumir el estado general de los datos.
2. Explicar los errores encontrados de forma sencilla.
3. Ordenar los problemas por prioridad.
4. Proponer acciones concretas para corregirlos.

No inventes errores que no aparezcan en el informe.
No modifiques ni valides directamente los datos.
Responde en español.
""".strip()


def build_analysis_prompt(report: AnalysisReport) -> str:
    report_data = report_to_dict(report)

    report_json = json.dumps(
        report_data,
        ensure_ascii=False,
        indent=2,
    )

    return f"""
Analiza el siguiente informe de calidad de datos:

{report_json}

Genera una respuesta con estas secciones:

- Resumen general
- Problemas encontrados
- Prioridad de corrección
- Acciones recomendadas
""".strip()