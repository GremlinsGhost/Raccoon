from Raccoon.BashCore.BashCore import get_process_table


from Raccoon.ViewCore.ViewObject import ViewObject
from Raccoon.ViewCore.ViewPort import ViewPort


def main():
    raw = get_process_table()

    vo = ViewObject(
        view_type=raw["type"],
        payload=raw
    )

    vp = ViewPort()
    print(vp.render(vo))

if __name__ == "__main__":
    main()
