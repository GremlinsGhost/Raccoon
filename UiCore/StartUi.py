from Raccoon.UiCore.Layout import Layout

def start():
    layout = Layout()
    running = True

    while running:
        screen = layout.render()
        print(screen)

        user_input = input("> ").strip()

        if user_input == "quit":
            running = False

        elif user_input == "dashboard":
            layout.set_view("dashboard")

        elif user_input == "processes":
            layout.set_view("processes")

        elif user_input == "map":
            layout.set_view("map")

        elif user_input == "log":
            layout.set_view("log")
