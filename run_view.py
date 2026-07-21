from Raccoon.BashCore.BashCore import get_process_table

from Raccoon.ViewCore.ViewObject import ViewObject
from Raccoon.ViewCore.ViewPort import ViewPort
from Raccoon.ViewCore.Layout import Layout
from Raccoon.ViewCore.Canvas import Canvas


def main():
    raw = get_process_table()

    vo = ViewObject(
        raw["type"],
        {
            "columns": raw["columns"],
            "rows": raw["rows"]
        }
    )

    log_data = ViewObject(
        "log",
        {
            "rows": [
                "Starting Raccoon...",
                "Loading modules...",
                "Pipeline OK",
                "Ready."
            ]
        }
    )

    layout = Layout({
        "top": vo,         # prosessitaulukko
        "bottom": log_data
    })

    canvas = Canvas()
    vp = ViewPort()

    result_canvas = layout.render(canvas, vp)
    print(result_canvas.render())

    print(vp.render(log_data))


if __name__ == "__main__":
    main()
