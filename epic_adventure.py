import random
import os

MAX_HEALTH = 100
PLAYER_BASE_ATTACK = 15
PLAYER_BASE_DEFENSE = 5


def clear_screen():
    """Clear the terminal screen"""
    print('\n' * 50)


class Player:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        
        # Adjust stats based on difficulty
        if difficulty == "easy":
            self.health = MAX_HEALTH + 30  # 130 health
            self.attack = PLAYER_BASE_ATTACK + 5  # 20 attack
            self.defense = PLAYER_BASE_DEFENSE + 3  # 8 defense
        elif difficulty == "medium":
            self.health = MAX_HEALTH  # 100 health
            self.attack = PLAYER_BASE_ATTACK  # 15 attack
            self.defense = PLAYER_BASE_DEFENSE  # 5 defense
        else:  # hard
            self.health = MAX_HEALTH - 20  # 80 health
            self.attack = PLAYER_BASE_ATTACK - 3  # 12 attack
            self.defense = PLAYER_BASE_DEFENSE - 2  # 3 defense
        
        self.max_health = self.health
        self.level = 1


class Enemy:
    def __init__(self, name, max_health, attack, defense, aggression, difficulty):
        self.name = name
        
        # Adjust enemy stats based on difficulty
        if difficulty == "easy":
            self.max_health = int(max_health * 0.7)  # 30% weaker
            self.attack = int(attack * 0.75)
            self.defense = int(defense * 0.7)
        elif difficulty == "medium":
            self.max_health = max_health
            self.attack = attack
            self.defense = defense
        else:  # hard
            self.max_health = int(max_health * 1.4)  # 40% stronger
            self.attack = int(attack * 1.3)
            self.defense = int(defense * 1.3)
        
        self.aggression = aggression


def validate_input(prompt, valid_inputs):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_inputs:
            return choice
        print("Invalid input. Please try again.")


def calculate_damage(attacker_power, defender_defense):
    base_damage = attacker_power - (defender_defense // 2)
    variance = random.randint(
        int(base_damage * 0.85), 
        int(base_damage * 1.15)
    )
    if variance < 3:
        variance = 3
    return variance


def enemy_choose_action(enemy, enemy_health):
    # Special case for the rock - it never attacks!
    if enemy.name == "Rock":
        return "defend"
    
    health_percent = (enemy_health / enemy.max_health) * 100
    
    if health_percent > 60:
        attack_chance = enemy.aggression
        defend_chance = 100 - enemy.aggression
    elif health_percent > 30:
        attack_chance = enemy.aggression * 0.7
        defend_chance = 100 - attack_chance
    else:
        if enemy.aggression > 70:
            attack_chance = 90
            defend_chance = 10
        else:
            attack_chance = 30
            defend_chance = 70
    
    action = random.choices(
        ["attack", "defend"], 
        weights=[attack_chance, defend_chance]
    )[0]
    return action


def fight_enemy(enemy, player):
    enemy_health = enemy.max_health
    name_width = (max(len(player.name), len(enemy.name)) + 
                  len("'s health: "))
    health_width = 3

    while enemy_health > 0 and player.health > 0:
        clear_screen()
        
        total_width = name_width + health_width
        
        player_spacing = (total_width - len(player.name) - 
                         len('s health: '))
        enemy_spacing = (total_width - len(enemy.name) - 
                        len('s health: '))
        
        print(f"\n{player.name}'s health: "
              f"{player.health:>{player_spacing}}")
        print(f"{enemy.name}'s health: "
              f"{enemy_health:>{enemy_spacing}}")

        choice = validate_input("1. Attack   2. Defend\n> ", 
                               ["1", "2"])
        
        clear_screen()
        
        print(f"\n{player.name}'s health: "
              f"{player.health:>{player_spacing}}")
        print(f"{enemy.name}'s health: "
              f"{enemy_health:>{enemy_spacing}}\n")
        
        enemy_action = enemy_choose_action(enemy, enemy_health)

        if choice == "1" and enemy_action == "attack":
            player_damage = calculate_damage(player.attack, 
                                            enemy.defense)
            enemy_damage = calculate_damage(enemy.attack, 
                                           player.defense)
            
            enemy_health -= player_damage
            print(f"{player.name} attacked and dealt "
                  f"{player_damage} damage!")
            
            if enemy_health <= 0:
                print(f"The {enemy.name} has been defeated! "
                      f"You gain experience and rest!\n")
                
                # Difficulty affects health recovery
                if player.difficulty == "easy":
                    health_recovery = 25
                    attack_gain = 3
                elif player.difficulty == "medium":
                    health_recovery = 15
                    attack_gain = 2
                else:  # hard
                    health_recovery = 10
                    attack_gain = 1
                
                player.health = min(player.health + health_recovery, 
                                   player.max_health)
                player.attack += attack_gain
                player.level += 1
                input("[Continue]")
                return "victory"
            
            player.health -= enemy_damage
            print(f"The {enemy.name} attacked back and dealt "
                  f"{enemy_damage} damage!")

        elif choice == "1" and enemy_action == "defend":
            player_damage = calculate_damage(player.attack, 
                                            enemy.defense)
            reduced_damage = player_damage // 2
            counter_damage = enemy.attack // 3
            
            enemy_health -= reduced_damage
            player.health -= counter_damage
            
            print(f"{player.name} attacked for "
                  f"{player_damage} damage!")
            print(f"The {enemy.name} raised its guard and blocked "
                  f"most of it! Only took {reduced_damage} damage.")
            print(f"Its counterattack dealt {counter_damage} "
                  f"damage to you!")
            
            if enemy_health <= 0:
                print(f"The {enemy.name} has been defeated! "
                      f"You gain experience and rest!\n")
                
                if player.difficulty == "easy":
                    health_recovery = 25
                    attack_gain = 3
                elif player.difficulty == "medium":
                    health_recovery = 15
                    attack_gain = 2
                else:
                    health_recovery = 10
                    attack_gain = 1
                
                player.health = min(player.health + health_recovery, 
                                   player.max_health)
                player.attack += attack_gain
                player.level += 1
                input("[Continue]")
                return "victory"

        elif choice == "2" and enemy_action == "attack":
            enemy_damage = calculate_damage(enemy.attack, 
                                           player.defense)
            reduced_damage = enemy_damage // 2
            counter_damage = player.attack // 3
            
            player.health -= reduced_damage
            enemy_health -= counter_damage
            
            print(f"{player.name} raised their guard!")
            print(f"The {enemy.name} attacked for {enemy_damage} "
                  f"damage, but you blocked most of it!")
            print(f"You took {reduced_damage} damage and countered "
                  f"for {counter_damage} damage!")

        else:
            print(f"{player.name} and the {enemy.name} both brace "
                  f"for impact!")
            print(f"You circle each other warily. Both take 2 damage "
                  f"from exhaustion.")
            player.health -= 2
            enemy_health -= 2

        if player.health <= 0:
            input("[Continue]")
            return "game_over"
        
        input("[Continue]")

    return None


def scenario(player, enemy, scenario_text):
    clear_screen()
    print(scenario_text)
    input("[Continue]")
    result = fight_enemy(enemy, player)

    clear_screen()
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
        elif enemy.name == "Rock":
            print("The rock crumbles into dust.\n"
                  "Robert looks at you with concern.\n"
                  "'You okay, buddy?' he asks.\n"
                  "You feel strangely satisfied.\n")
        input("[Continue]")
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
        elif enemy.name == "Rock":
            print("You somehow died fighting a rock.\n"
                  "A ROCK.\n"
                  "Robert will never let you live this down.\n"
                  "...Oh wait, you're dead.\n")
        input("[Continue]")
        return "game_over"


def main():
    clear_screen()
    print("""
    *******************************************
    *******************************************
    ******* Welcome to the Epic Adventure! ***
    *******************************************
    *******************************************
    """)
    input("Press Enter to continue...")

    # Difficulty selection
    clear_screen()
    print("\n" + "="*50)
    print("SELECT YOUR DIFFICULTY:")
    print("="*50)
 
   
    difficulty = validate_input(
        "\nChoose your difficulty (Easy / Medium / Hard)\n> ",
        ["easy", "medium", "hard"]
    )
    
    print(f"  Difficulty set to: {difficulty.upper()}")

    player = Player(input("\nWhat is your name?\n> ").strip(), difficulty)

    clear_screen()
    
    # Check if player name is Marcus (case insensitive)
    is_marcus = player.name.lower() == "marcus"
    
    # Setup the enemies with their stats
    # Stats are: name, health, attack, defense, aggression(0-100), difficulty
    enemies = {
        "north": Enemy("Bear", 50, 15, 3, 75, difficulty),
        "east": Enemy("Bandit Leader", 70, 18, 5, 60, difficulty),
        "south": Enemy("Cave Troll", 90, 22, 8, 85, difficulty),
        "west": Enemy("Dragon", 150, 28, 10, 50, difficulty)
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
    
    # Add Campfire easter egg if player name is Marcus
    if is_marcus:
        enemies["campfire"] = Enemy("Rock", 500, 0, 0, 0, difficulty)
        scenarios["campfire"] = (
            "\n\tYou are sitting around a campfire, just living your best wormy "
            "acetomenotistic life with your best friend Robert. You notice something "
            "is off but you can't put your freakishly long finger on it. After a brief "
            "moment of hypervigilance, something catches your big ol' eye. There's "
            "something about that rock. That rock right there. It's... It's... "
            "IT'S PISSING YOU OFF! You tell Robert but he is of little help. You are "
            "left with no other choice than to give that stupid smug little stupid smug "
            "rock a piece of your mind.\n"
        )
    
    # Build the valid direction inputs
    valid_directions = list(enemies.keys())
    
    # Display initial crossroad
    print(f"\nHello {player.name}.\n\n"
          f"You find yourself suddenly teleported to an unfamiliar "
          f"crossroad surrounded by {'five' if is_marcus else 'four'} different paths.\n")
    print("To the North:\tYou see a dense forest stretching as far "
          "as the eye can see.")
    print("To the East:\tYou see smoke rising from a distant village.")
    print("To the South:\tYou see a mysterious cave entrance beckoning "
          "with an eerie glow.")
    print("To the West:\tYou see a narrow path leading up a steep "
          "mountain.\n")
    
    if is_marcus:
        print("To the Campfire:\tYou see a cozy campfire with your best friend Robert.\n")
    
    defeated_enemies = []
    
    # Main game loop
    while True:
        if len(defeated_enemies) == len(enemies):
            clear_screen()
            print(f"\nCongratulations {player.name}!!! You have "
                  f"defeated all the enemies and completed the epic "
                  f"adventure on {difficulty.upper()} mode!\n")
            input("Press ENTER to end game and get back to your life, "
                  "loser.")
            break
        
        clear_screen()
        print(f"\nHello {player.name}.\n\n"
              f"You find yourself at the crossroad surrounded by {'five' if is_marcus else 'four'} different paths.\n")
        print("To the North:\tYou see a dense forest stretching as far "
              "as the eye can see.")
        print("To the East:\tYou see smoke rising from a distant village.")
        print("To the South:\tYou see a mysterious cave entrance beckoning "
              "with an eerie glow.")
        print("To the West:\tYou see a narrow path leading up a steep "
              "mountain.\n")
        
        if is_marcus:
            print("To the Campfire:\tYou see a cozy campfire with your best friend Robert.\n")
        
        if defeated_enemies:
            print(f"Defeated enemies: {', '.join(defeated_enemies)}\n")
        
        # Build prompt based on available directions
        direction_prompt = "Which direction will you choose? "
        if is_marcus:
            direction_prompt += "(North / East / South / West / Campfire)\n> "
        else:
            direction_prompt += "(North / East / South / West)\n> "
            
        direction = validate_input(direction_prompt, valid_directions)
        
        if direction not in defeated_enemies:
            result = scenario(player, enemies[direction], 
                            scenarios[direction])
            if result == "victory":
                defeated_enemies.append(direction)
            elif result == "game_over":
                clear_screen()
                print("\nUnfortunately, your adventure has come to "
                      "an end.\n")
                input("Press ENTER to die.")
                print("\nx_x You died.\n")
                input("Exit")
                break


if __name__ == "__main__":
    main()
