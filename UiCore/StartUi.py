def start():
    print("Raccoon UI ready.")
    while True:
        user_input = input("> ")
        yield user_input
