import random

MAX_HEALTH = 100
PLAYER_BASE_ATTACK = 15
PLAYER_BASE_DEFENSE = 5


class Player:
    def __init__(self, name):
        self.name = name
        self.health = MAX_HEALTH
        self.attack = PLAYER_BASE_ATTACK
        self.defense = PLAYER_BASE_DEFENSE
        self.level = 1


class Enemy:
    def __init__(self, name, max_health, attack, defense, aggression):
        self.name = name
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.aggression = aggression  # how aggressive the enemy is (0-100)


def validate_input(prompt, valid_inputs):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_inputs:
            return choice
        print("Invalid input. Please try again.")


def calculate_damage(attacker_power, defender_defense):
    # Calculate base damage with defender's defense reducing it
    base_damage = attacker_power - (defender_defense // 2)
    # Add some randomness so damage isn't the same every time
    variance = random.randint(
        int(base_damage * 0.85), 
        int(base_damage * 1.15)
    )
    # Ensure player always does at least some damage
    if variance < 3:
        variance = 3
    return variance


def enemy_choose_action(enemy, enemy_health):
    # Figure out what the enemy wants to do based on how much 
    # health they have left
    health_percent = (enemy_health / enemy.max_health) * 100
    
    # Healthy enemies fight more aggressively
    if health_percent > 60:
        attack_chance = enemy.aggression
        defend_chance = 100 - enemy.aggression
    # Wounded enemies are more cautious
    elif health_percent > 30:
        attack_chance = enemy.aggression * 0.7
        defend_chance = 100 - attack_chance
    # Low health makes enemies either desperate or defensive
    else:
        if enemy.aggression > 70:
            # Aggressive enemies go all in when desperate
            attack_chance = 90
            defend_chance = 10
        else:
            # Cautious enemies defend more
            attack_chance = 30
            defend_chance = 70
    
    action = random.choices(
        ["attack", "defend"], 
        weights=[attack_chance, defend_chance]
    )[0]
    return action


def fight_enemy(enemy, player):
    enemy_health = enemy.max_health
    # Calculate spacing for health display
    name_width = (max(len(player.name), len(enemy.name)) + 
                  len("'s health: "))
    health_width = 3

    while enemy_health > 0 and player.health > 0:
        total_width = name_width + health_width
        
        # Show current health for both
        player_spacing = (total_width - len(player.name) - 
                         len('s health: '))
        enemy_spacing = (total_width - len(enemy.name) - 
                        len('s health: '))
        
        print(f"\n{player.name}'s health: "
              f"{player.health:>{player_spacing}}")
        print(f"{enemy.name}'s health: "
              f"{enemy_health:>{enemy_spacing}}")

        # Get player choice
        choice = validate_input("1. Attack   2. Defend\n> ", 
                               ["1", "2"])
        # Enemy makes their own choice
        enemy_action = enemy_choose_action(enemy, enemy_health)

        # Handle when both sides attack
        if choice == "1" and enemy_action == "attack":
            player_damage = calculate_damage(player.attack, 
                                            enemy.defense)
            enemy_damage = calculate_damage(enemy.attack, 
                                           player.defense)
            
            enemy_health -= player_damage
            print(f"\n{player.name} attacked and dealt "
                  f"{player_damage} damage!")
            
            # Check if enemy died
            if enemy_health <= 0:
                print(f"The {enemy.name} has been defeated! "
                      f"You gain experience and rest!\n")
                player.health = min(player.health + 15, MAX_HEALTH)
                player.attack += 2
                player.level += 1
                input("[Continue]")
                return "victory"
            
            player.health -= enemy_damage
            print(f"The {enemy.name} attacked back and dealt "
                  f"{enemy_damage} damage!")

        # Player attacks but enemy blocks
        elif choice == "1" and enemy_action == "defend":
            player_damage = calculate_damage(player.attack, 
                                            enemy.defense)
            reduced_damage = player_damage // 2
            counter_damage = enemy.attack // 3
            
            enemy_health -= reduced_damage
            player.health -= counter_damage
            
            print(f"\n{player.name} attacked for "
                  f"{player_damage} damage!")
            print(f"The {enemy.name} raised its guard and blocked "
                  f"most of it! Only took {reduced_damage} damage.")
            print(f"Its counterattack dealt {counter_damage} "
                  f"damage to you!")
            
            if enemy_health <= 0:
                print(f"The {enemy.name} has been defeated! "
                      f"You gain experience and rest!\n")
                player.health = min(player.health + 15, MAX_HEALTH)
                player.attack += 2
                player.level += 1
                input("[Continue]")
                return "victory"

        # Player blocks, enemy attacks
        elif choice == "2" and enemy_action == "attack":
            enemy_damage = calculate_damage(enemy.attack, 
                                           player.defense)
            reduced_damage = enemy_damage // 2
            counter_damage = player.attack // 3
            
            player.health -= reduced_damage
            enemy_health -= counter_damage
            
            print(f"\n{player.name} raised their guard!")
            print(f"The {enemy.name} attacked for {enemy_damage} "
                  f"damage, but you blocked most of it!")
            print(f"You took {reduced_damage} damage and countered "
                  f"for {counter_damage} damage!")

        # Both defend
        else:
            print(f"\n{player.name} and the {enemy.name} both brace "
                  f"for impact!")
            print(f"You circle each other warily. Both take 2 damage "
                  f"from exhaustion.")
            player.health -= 2
            enemy_health -= 2

        # Check if player died
        if player.health <= 0:
            return "game_over"

    return None


def scenario(player, enemy, scenario_text):
    print(scenario_text)
    input("[Continue]")
    result = fight_enemy(enemy, player)

    print("")
    if result == "victory":
        if enemy.name == "Dragon":
            print("Filled with adrenaline from defeating the dragon, "
                  "you continue your journey.\n")
        elif enemy.name == "Cave Troll":
            print("The defeated troll slumps to the ground, allowing "
                  "you to proceed deeper into the cave.\n")
        elif enemy.name == "Bear":
            print("Feeling triumphant after defeating the bear, "
                  "you continue your journey.\n")
        elif enemy.name == "Bandit Leader":
            print("With the bandit leader defeated, the villagers "
                  "thank you and you continue your journey.\n")
        return "victory"
    else:
        if enemy.name == "Dragon":
            print("The dragon's fire leaves you badly burned. "
                  "You retreat from the mountain to die in peace.\n")
        elif enemy.name == "Cave Troll":
            print("The troll's brute strength overwhelms you.\n"
                  "You attempt to retreat from the cave to die in "
                  "peace, but you are trapped.\n\n"
                  "Your bones join the pile of hundreds of other "
                  "stupid...\nI mean...\nbrave...\nadventurers.")
        elif enemy.name == "Bear":
            print("The bear's attack overwhelms you.\n"
                  "You hear the bear say a prayer, thanking his bear "
                  "deity for this delicious feast.\n")
            input("[Press ENTER to say 'Amen' with the bear]")
            print("You can't talk. The bear ripped your throat out."
                  "\n\tBummer.")
        elif enemy.name == "Bandit Leader":
            print("The bandit leader lands his final blow. The bandits "
                  "fight over who gets to keep your sweet loot.\n"
                  "You try to get up and retreat, but the bandits "
                  "stole your feet.")
        input("[Continue]")
        return "game_over"


def main():
    print("""
    *******************************************
    *******************************************
    ******* Welcome to the Epic Adventure! ***
    *******************************************
    *******************************************
    """)
    input("Press Enter to continue...")

    player = Player(input("\nWhat is your name?\n> ").strip())

    print(f"\nHello {player.name}.\n\n"
          f"You find yourself suddenly teleported to an unfamiliar "
          f"crossroad surrounded by four different paths.\n")
    print("To the North:\tYou see a dense forest stretching as far "
          "as the eye can see.")
    print("To the East:\tYou see smoke rising from a distant village.")
    print("To the South:\tYou see a mysterious cave entrance beckoning "
          "with an eerie glow.")
    print("To the West:\tYou see a narrow path leading up a steep "
          "mountain.\n")

    # Setup the enemies with their stats
    # Stats are: name, health, attack, defense, aggression(0-100)
    enemies = {
        "north": Enemy("Bear", 50, 15, 3, 75),  # Fast but weak
        "east": Enemy("Bandit Leader", 70, 18, 5, 60),  # Balanced
        "south": Enemy("Cave Troll", 90, 22, 8, 85),  # TankY & hits hard
        "west": Enemy("Dragon", 150, 28, 10, 50)  # Boss - plays smart
    }
    
    scenarios = {
        "north": (
            "\n\tYou enter the dense forest.\n"
            "The air is thick with the scent of pine and damp earth.\n"
            "As you walk deeper, you hear rustling in the bushes.\n"
            "You try to ignore it and decide to keep walking. \n"
            "Before you can take another step, out lunges a wild bear!\n"
            "It's hungry as heck and you look delicious!\n"
        ),
        "east": (
            "\n\tAs you head towards the distant village,\n"
            "following the trail of smoke, you notice something "
            "alarming:\n"
            "the village is under attack by a group of bandits!\n"
            "\tTheir leader gestures to his gang, and they quickly "
            "encircle you both.\n"
            "Their chants of 'FIGHT! FIGHT! FIGHT!' echo through "
            "the air."
        ),
        "south": (
            "\n\tYou enter the mysterious cave.\n"
            "The air is cool and damp, with faint echoes bouncing off "
            "the walls.\n"
            "As you venture deeper, you notice glowing crystals "
            "illuminating the path.\n"
            "You start to feel uneasy, so you turn around to leave.\n"
            "You turn and find yourself face to face with a troll!\n"
            "\t'Your bones will make a great addition to my "
            "collection!'"
        ),
        "west": (
            "\n\tYou start your ascent up the steep mountain path.\n"
            "The higher you climb, the more breathtaking the view "
            "becomes.\n"
            "After a challenging climb, you reach a serene mountaintop "
            "lake.\n"
            "\tThe air grows suddenly cold.\n"
            "The wind picks up, carrying a bone-chilling roar that "
            "echoes through the peaks.\n"
            "Your heart pounds as a colossal shadow blots out the sun.\n"
            "With a thunderous crash, a dragon descends from the "
            "swirling clouds,\n"
            "its scales gleaming ominously. Its piercing eyes lock onto "
            "you,\n"
            "and its wings cast a dark shadow over the lake.\n"
            "The ground trembles beneath its massive claws as it emits "
            "a low, rumbling growl.\n\n"
            "You ready your weapon"
        ),
    }
    
    defeated_enemies = []
    
    # Main game loop
    while True:
        # Check if player beat everything
        if len(defeated_enemies) == len(enemies):
            print(f"\nCongratulations {player.name}!!! You have "
                  f"defeated all the enemies and completed the epic "
                  f"adventure!\n")
            input("Press ENTER to end game and get back to your life, "
                  "loser.")
            break
            
        direction = validate_input(
            "Which direction will you choose? "
            "(North / East / South / West)\n> ", 
            enemies.keys()
        )
        
        # Only fight if they haven't beaten this enemy yet
        if direction not in defeated_enemies:
            result = scenario(player, enemies[direction], 
                            scenarios[direction])
            if result == "victory":
                defeated_enemies.append(direction)
            elif result == "game_over":
                print("\nUnfortunately, your adventure has come to "
                      "an end.\n")
                input("Press ENTER to die.")
                print("\nx_x You died.\n")
                input("Exit")
                break


if __name__ == "__main__":
    main()

