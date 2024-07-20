import random

MAX_HEALTH = 100
MIN_DAMAGE = 5
HEALTH_GAIN = 10

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
        choice = input(prompt).strip().lower()
        if choice in valid_inputs:
            return choice
        print("Invalid input. Please try again.")

def fight_enemy(enemy, player):
    enemy_health = enemy.max_health
    while enemy_health > 0 and player.health > 0:
        print(f"\n{player.name}'s health:\t{player.health}\n{enemy.name}'s"
              f"health:\t{enemy_health}")
        choice = validate_input("1. Attack   2. Defend\n> ", ["1", "2"])
        
        if choice == "1":
            player_attack = calculate_player_attack(enemy.attack_damage)
            enemy_health -= player_attack
            print(f"\n{player.name} attacked the {enemy.name} and dealt"
                  f" {player_attack} damage!")
            
            if enemy_health <= 0:
                print(f"The {enemy.name} has been defeated! You rest and gain "
                      f"{HEALTH_GAIN} health!\n")
                input("[Continue]")
                player.health = min(player.health + HEALTH_GAIN, MAX_HEALTH)
                return "victory"
            
            enemy_attack = calculate_enemy_attack(
                MIN_DAMAGE, enemy.attack_damage)
            player.health -= enemy_attack
            print(f"The {enemy.name} attacked {player.name} and dealt"
                  f" {enemy_attack} damage!")
        
        elif choice == "2":
            player.health -= calculate_defend_damage(
                MIN_DAMAGE, enemy.attack_damage)
        
        # Ensure player health doesn't drop below zero unexpectedly
        if player.health <= 0:
            return "game_over"
    
    return None

def calculate_player_attack(max_damage):
    return random.randint(max_damage // 2, max_damage)

def calculate_enemy_attack(min_damage, max_damage):
    return random.randint(min_damage, max_damage // 2)

def calculate_defend_damage(min_damage, max_damage):
    return max(0, random.randint(min_damage, max_damage // 2) - 
               random.randint(MIN_DAMAGE, max_damage // 3))

def scenario(player, enemy, scenario_text):
    print(scenario_text)
    input("[Continue]")
    result = fight_enemy(enemy, player)
    
    print("")
    if result == "victory":
        if enemy.name == "Dragon":
            print("Filled with adrenaline from defeating the dragon, you"
                  " continue your journey.\n")
        elif enemy.name == "Cave Troll":
            print("The defeated troll slumps to the ground, allowing you to"
                  " proceed deeper into the cave.\n")
        elif enemy.name == "Bear":
            print("Feeling triumphant after defeating the bear, you continue"
                  " your journey.\n")
        elif enemy.name == "Bandit Leader":
            print("With the bandit leader defeated, the villagers thank you"
                  " and you continue your journey.\n")
        return "victory"
    else:
        if enemy.name == "Dragon":
            print("The dragon's fire leaves you badly burned. You retreat from"
                  " the mountain to die in peace.\n")
        elif enemy.name == "Cave Troll":
            print("The troll's brute strength overwhelms you.\nYou attempt to"
                  " retreat from the cave to die in peace, but you are trapped"
                  ".\nYour bones join the pile of hundreds of other stupid.."
                  ".\nI mean...\nbrave...\nadventurers.")
        elif enemy.name == "Bear":
            print("The bear's attack overwhelms you.\nYou hear the bear say a"
                  " prayer, thanking his bear deity for this delicious feast"
                  ".\n")
            input("[Press ENTER to say 'Amen' with the bear]")
            print("You can't talk. The bear ripped your throat out."
                  "\n\tBummer.")
        elif enemy.name == "Bandit Leader":
            print("The bandit leader lands his final blow. The bandits fight"
                  " over who gets to keep your sweet loot.\nYou try to get up"
                  " and retreat, but the bandits stole your feet.")
        input("[Continue]")
        return "game_over"

def main():
    print("""
    ***************************************************************************
    ***************************************************************************
    ********************* Welcome to the Epic Adventure! **********************
    ***************************************************************************
    ***************************************************************************
    """)
    input("Press Enter to continue...")
    
    player = Player(input("\nWhat is your name?\n> ").strip())
    
    print(f"\nHello {player.name}.\n\nYou find yourself suddenly teleported to"
          " an unfamiliar crossroad surrounded by four different paths.\n")
    print("To the North:\tYou see a dense forest stretching as far as the"
          " eye can see.")
    print("To the East:\tYou see smoke rising from a distant village.")
    print("To the South:\tYou see a mysterious cave entrance beckoning with"
          " an eerie glow.")
    print("To the West:\tYou see a narrow path leading up a steep mountain.\n")
    # input("[Continue]")
    
    enemies = {
        "north": Enemy("Bear", 50, 20),
        "east": Enemy("Bandit Leader", 65, 30),
        "south": Enemy("Cave Troll", 85, 40),
        "west": Enemy("Dragon", 200, 75)
    }
    scenarios = {
        "north": "\n\tYou enter the dense forest.\nThe air is thick with the"
        " scent of pine and damp earth.\nAs you walk deeper, you hear rustling"
        " in the bushes.\nYou try to ignore it and decide to keep walking."
        " \nBefore you can take another step, out lunges a wild bear!\nIt's"
        " hungry as heck and you look delicious!\n",
        "east": "\n\tAs you head towards the distant village,\nfollowing the"
        " trail of smoke, you notice something alarming:\nthe village is under"
        " attack by a group of bandits!\n\tTheir leader gestures to his gang,"
        " and they quickly encircle you both.\nTheir chants of 'FIGHT! FIGHT!"
        " FIGHT!' echo through the air.",
        "south": "\n\tYou enter the mysterious cave.\nThe air is cool and"
        " damp, with faint echoes bouncing off the walls.\nAs you venture"
        " deeper, you notice glowing crystals illuminating the path.\nYou"
        " start to feel uneasy, so you turn around to leave.\nYou turn and"
        " find yourself face to face with a troll!\n\t'Your bones will make a"
        " great addition to my collection!'",
        "west": "\n\tYou start your ascent up the steep mountain path.\nThe"
        " higher you climb, the more breathtaking the view becomes.\nAfter a"
        " challenging climb, you reach a serene mountaintop lake.\n\tThe air"
        " grows suddenly cold.\nThe wind picks up, carrying a bone-chilling"
        " roar that echoes through the peaks.\nYour heart pounds as a colossal"
        " shadow blots out the sun.\nWith a thunderous crash,"
        " a dragon descends from the swirling clouds,\nits scales gleaming"
        " ominously. Its piercing eyes lock onto you,\nand its wings cast a"
        " dark shadow over the lake.\nThe ground trembles beneath its massive"
        " claws as it emits a low, rumbling growl.\n\nYou ready your weapon",
    }
    defeated_enemies = []
    while True:
        if len(defeated_enemies) == len(enemies):
            print(f"\nCongratulations {player.name}!!! You have defeated all"
                  " the enemies and completed the epic adventure!\n")
            input("Press ENTER to end game and get back to your life, loser.")
            break
        direction = validate_input("Which direction will you choose? "
                                   "(North / East / South / West)\n> ", 
                                   enemies.keys())
        if direction not in defeated_enemies:
            result = scenario(player, enemies[direction], scenarios[direction])
            if result == "victory":
                defeated_enemies.append(direction)
            elif result == "game_over":
                print("\nUnfortunately, your adventure has come to an end.\n")
                input("Press ENTER to die.")
                print("\nx_x You died.\n")
                input("Exit")
                break

if __name__ == "__main__":
    main()
