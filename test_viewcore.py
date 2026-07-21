from ViewCore.ViewPort import ViewPort

test_table = {
    "type": "table",
    "columns": ["PID", "NAME", "CPU"],
    "rows": [
        ["101", "bash", "0.3"],
        ["202", "python", "12.4"],
        ["303", "raccoon", "99.9"]
    ]
}

vp = ViewPort()
print(vp.render(test_table))
