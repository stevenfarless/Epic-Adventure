import time
import random

def intro():
    """Introduces the game and the available directions."""
    print("Welcome to the Epic Adventure!")
    time.sleep(1)
    print("You find yourself at a crossroads...")
    time.sleep(1)
    print("To the north, a dense forest stretches as far as the eye can see.")
    print("To the east, there's a narrow path leading up a steep mountain.")
    print("To the south, you can see smoke rising from a distant village.")
    print("To the west, a mysterious cave entrance beckons with an eerie glow.")
    print()

def fight_enemy(enemy_name, max_health, attack_damage):
    """
    Simulates a fight with an enemy.

    Parameters:
    - enemy_name: str, the name of the enemy
    - max_health: int, the maximum health of the enemy
    - attack_damage: int, the maximum attack damage the enemy can deal

    Returns:
    - str: "victory" if the player wins, "defeat" if the player loses
    """
    print(f"A wild {enemy_name} appears!")
    enemy_health = max_health
    player_health = 100  # Player starts with 100 health
    
    # Battle loop
    while enemy_health > 0 and player_health > 0:
        print(f"Your health: {player_health}   {enemy_name}'s health: {enemy_health}")
        choice = input("1. Attack   2. Defend\n")
        
        if choice == "1":
            # Player attacks
            player_attack = random.randint(attack_damage // 2, attack_damage)
            enemy_health -= player_attack
            print(" ")
            print(f"You attack the {enemy_name} and deal {player_attack} damage!")
            
            if enemy_health <= 0:
                print (" ")
                print(f"The {enemy_name} has been defeated!")
                print (" ")
                return "victory"
          
            # Enemy counterattacks
            enemy_attack = random.randint(1, attack_damage // 2)
            player_health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")
            
        elif choice == "2":
            # Player defends
            player_defense = random.randint(1, attack_damage // 3)
            enemy_attack = random.randint(1, attack_damage // 2)
            damage_taken = max(0, enemy_attack - player_defense)
            player_health -= damage_taken
            print(" ")
            print(f"You defend against the {enemy_name}'s attack and take {damage_taken} damage.")
            
        else:
            # Invalid choice, enemy attacks
            print("Invalid choice. The enemy takes advantage of your hesitation...")
            enemy_attack = random.randint(1, attack_damage // 2)
            player_health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")
    
    # Check if the player is defeated
    if player_health <= 0:
        print("You have been defeated...")
        return "defeat"

def forest():
    """Handles the events that occur when the player chooses to go north to the forest."""
    print(" ")
    print("You enter the dense forest...")
    time.sleep(1)
    print("The air is thick with the scent of pine and damp earth.")
    time.sleep(1)
    print("As you walk deeper, you hear rustling in the bushes.")
    time.sleep(1)
    
    # Fight a bear in the forest
    result = fight_enemy("Bear", 50, 20)
    if result == "victory":
        print("Feeling triumphant after defeating the bear, you continue your journey.")
        return "victory"
    else:
        print("The bear's attack overwhelms you, and you retreat from the forest...")
        return "game_over"

def mountain():
    """Handles the events that occur when the player chooses to go east to the mountain."""
    print("You start your ascent up the steep mountain path...")
    time.sleep(1)
    print("The higher you climb, the more breathtaking the view becomes.")
    time.sleep(1)
    print("After a challenging climb, you reach a serene mountaintop lake.")
    time.sleep(1)
    
    # Fight a dragon on the mountain
    result = fight_enemy("Dragon", 80, 30)
    if result == "victory":
        print("Filled with adrenaline from defeating the dragon, you continue your journey.")
        return "victory"
    else:
        print("The dragon's fire overwhelms you, and you retreat from the mountain...")
        return "game_over"

def village():
    """Handles the events that occur when the player chooses to go south to the village."""
    print("You head towards the distant village, following the smoke...")
    time.sleep(1)
    print("As you approach, you notice the village is under attack by bandits!")
    time.sleep(1)
    
    # Fight the bandit leader in the village
    result = fight_enemy("Bandit Leader", 60, 25)
    if result == "victory":
        print("With the bandit leader defeated, the villagers thank you and you continue your journey.")
        return "victory"
    else:
        print("Overwhelmed by the bandit leader's forces, you retreat from the village...")
        return "game_over"

def cave():
    """Handles the events that occur when the player chooses to go west to the cave."""
    print("You enter the mysterious cave...")
    time.sleep(1)
    print("The air is cool and damp, with faint echoes bouncing off the walls.")
    time.sleep(1)
    print("As you venture deeper, you notice glowing crystals illuminating the path.")
    time.sleep(1)
    
    # Fight a cave troll in the cave
    result = fight_enemy("Cave Troll", 100, 35)
    if result == "victory":
        print("The defeated troll slumps to the ground, allowing you to proceed deeper into the cave.")
        return "victory"
    else:
        print("The troll's brute strength overwhelms you, and you retreat from the cave...")
        return "game_over"

def main():
    """Main function to run the game."""
    intro()
    time.sleep(1)
    print("You set off on your epic adventure...")
    time.sleep(1)
    
    # Mapping of directions to their respective functions and enemy names
    directions = {
        "north": ("Bear", forest),
        "east": ("Dragon", mountain),
        "south": ("Bandit Leader", village),
        "west": ("Cave Troll", cave)
    }
    
    defeated_enemies = []  # List to keep track of defeated enemies
    
    while True:
        if len(defeated_enemies) == 4:
            time.sleep(1)
            print(" ")
            print(" ")
            print(" ")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("************************ Congratulations!!! ************************")
            print("You have defeated all the enemies and completed the epic adventure!")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            print("********************************************************************")
            break
        
        direction = input("Which direction will you choose? (North / East / South / West)\n").lower()
        
        if direction in directions:
            enemy_name, location_function = directions[direction]
            
            if direction in defeated_enemies:
                print(f"You have already defeated the {enemy_name} in this direction.")
                print("Choose another direction.")
                continue
            else:
                result = location_function()
                if result == "victory":
                    defeated_enemies.append(direction)
                elif result == "game_over":
                    print("Unfortunately, your adventure has come to an end.")
                    print("Better luck next time!")
                    break
        
        else:
            print("Invalid direction. Please choose North, East, South, or West.")

if __name__ == "__main__":
    main()
