def show_output(title: str, content: str):
    print(f"[Raccoon] {title}")


    longest = max(len(line) for line in content.splitlines())
    print("-" * longest)

    print(content)