

def select_option(cap):
    r = input("Select the option: ")
    try:
        if int(r) > cap:
            print("Invalid option")
            return 0
        return int(r)
    except ValueError as error:
        print(error)
        return 0

def select_open_option(options):
    for i, opt in enumerate(options):
        print(f"{str(i)}: {opt}")
    # r = input("Select the option: ")
    r = select_option(len(options))
    return options[r]

def read_players(filename):
    players = []
    with open(f"players/{filename}", "r") as file:
        for line in file:
            players.append(line.strip("\n"))
    return players
