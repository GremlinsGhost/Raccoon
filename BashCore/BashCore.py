def get_process_table():
    return {
        "type": "table",
        "columns": ["PID", "NAME", "CPU"],
        "rows": [
            ["101", "bash", "0.3"],
            ["202", "python", "12.4"],
            ["303", "raccoon", "99.9"]
        ]
    }
