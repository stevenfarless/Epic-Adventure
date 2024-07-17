import random

MAX_HEALTH = 100
MIN_DAMAGE = 1

class Player:
    def __init__(self, name):
        self.name = name
        self.health = MAX_HEALTH

class Enemy:
    def __init__(self, name, max_health, attack_damage):
        self.name = name
        self.max_health = max_health
        self.attack_damage = attack_damage

def validate_input(prompt, valid_inputs):
    while True:
        choice = input(prompt).lower()
        if choice in valid_inputs:
            return choice
        print("Invalid input. Please try again.")

def fight_enemy(enemy, player):
    enemy_health = enemy.max_health
    while enemy_health > 0 and player.health > 0:
        print(f"\n{player.name}'s health:\t{player.health}\n{enemy.name}'s health:\t{enemy_health}")
        choice = validate_input("1. Attack   2. Defend\n", ["1", "2"])
        if choice == "1":
            player_attack = random.randint(enemy.attack_damage // 2, enemy.attack_damage)
            enemy_health -= player_attack
            print(f"\nYou attack the {enemy.name} and deal {player_attack} damage!")
            if enemy_health <= 0:
                print(f"\nThe {enemy.name} has been defeated!\n")
                player.health = min(player.health + 10, MAX_HEALTH)
                return "victory"
            player.health -= random.randint(MIN_DAMAGE, enemy.attack_damage // 2)
        elif choice == "2":
            player.health -= max(0, random.randint(MIN_DAMAGE, enemy.attack_damage // 2) - random.randint(MIN_DAMAGE, enemy.attack_damage // 3))
        else:
            player.health -= random.randint(MIN_DAMAGE, enemy.attack_damage // 2)
    return "game_over" if player.health <= 0 else None

def scenario(player, enemy, scenario_text):
    print(scenario_text)
    input("[Continue]")
    return fight_enemy(enemy, player)

def main():
    print("""
    ********************************************************************************
    ********************************************************************************
    ************************ Welcome to the Epic Adventure! ************************
    ********************************************************************************
    ********************************************************************************
    """)
    input("Press Enter to continue...")
    
    player = Player(input("\nWhat is your name? "))
    
    print(f"\nHello {player.name}.\nYou find yourself suddenly teleported to an unfamiliar crossroad surrounded by four different paths.\n")
    input("[Continue]")
    print("""To the North:\tYou see a dense forest stretching as far as the eye can see.""")
    # input("[Continue]")
    print("""To the East:\tYou see smoke rising from a distant village.""")
    # input("[Continue]")
    print("""To the South:\tYou see a mysterious cave entrance beckoning with an eerie glow.""")
    # input("[Continue]")
    print("""To the West:\tYou see a narrow path leading up a steep mountain.\n""")
    input("[Continue]")
    
    enemies = {
        "north": Enemy("Bear", 50, 20),
        "east": Enemy("Bandit Leader", 65, 30),
        "south": Enemy("Cave Troll", 85, 25),
        "west": Enemy("Dragon", 100, 35)
    }
    scenarios = {
        "north": "\nYou enter the dense forest.\nThe air is thick with the scent of pine and damp earth.\nAs you walk deeper, you hear rustling in the bushes.\nYou try to ignore it and decide to keep walking.\nBefore you can take another step, out lunges a wild bear!\nIt's hungry as heck and you look delicious!\n",
        "east": "\nYou head towards the distant village, following the smoke.\nAs you approach, you notice the village is under attack by bandits!\n",
        "south": "\nYou enter the mysterious cave.\nThe air is cool and damp, with faint echoes bouncing off the walls.\nAs you venture deeper, you notice glowing crystals illuminating the path.\n",
        "west": "\nYou start your ascent up the steep mountain path.\nThe higher you climb, the more breathtaking the view becomes.\nAfter a challenging climb, you reach a serene mountaintop lake.\n",
    }
    defeated_enemies = []
    while True:
        if len(defeated_enemies) == len(enemies):
            print(f"\nCongratulations {player.name}!!! You have defeated all the enemies and completed the epic adventure!")
            break
        direction = validate_input("Which direction will you choose? (North / East / South / West)\n", enemies.keys())
        if direction not in defeated_enemies:
            result = scenario(player, enemies[direction], scenarios[direction])
            if result == "victory":
                defeated_enemies.append(direction)
            elif result == "game_over":
                print("Unfortunately, your adventure has come to an end.")
                break

if __name__ == "__main__":
    main()
