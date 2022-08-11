from py_struct_query import __version__

import py_struct_query.py_struct_query as pyql


def test_version():
    assert __version__ == '0.1.0'


def test_db():
    data = {
        "brand": [
            {"name": "Specialized", "country": "USA"},
            {"name": "All City", "country": "USA"},
        ],
        "model": [
            ["name", "brand_name", "type"],
            ["Langster", "Specialized", "track"],
            ["Thunderdome", "All City", "track"],
            ["Space Horse", "All City", "touring"],
        ],
    }
    with pyql.db(**data) as db:
        rows = db.fetchall(f"""
        SELECT
          b.name AS brand_name,
          m.name AS model_name,
          m.type AS model_type,
          b.country AS brand_country
        FROM brand AS b
        JOIN model AS m
        ON b.name = m.brand_name
        ORDER BY m.name
        """)
        results = []
        for row in rows:
            brand_name, model_name, model_type, brand_country = row
            results.append(
                {
                    "brand_name": brand_name,
                    "model_name": model_name,
                    "model_type": model_type,
                    "brand_country": brand_country,
                },
            )

        assert results == [
            {"brand_name": "Specialized", "model_name": "Langster", "model_type": "track", "brand_country": "USA"},
            {"brand_name": "All City", "model_name": "Space Horse", "model_type": "touring", "brand_country": "USA"},
            {"brand_name": "All City", "model_name": "Thunderdome", "model_type": "track", "brand_country": "USA"},
        ]
