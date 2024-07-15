import time
import random

PLAYER_HEALTH = 100

def intro():
    print("""
    Welcome to the Epic Adventure!
    You find yourself at a crossroads...
    To the north, a dense forest stretches as far as the eye can see.
    To the east, there's a narrow path leading up a steep mountain.
    To the south, you can see smoke rising from a distant village.
    To the west, a mysterious cave entrance beckons with an eerie glow.
    """)

def fight_enemy(enemy_name, max_health, attack_damage):
    print(f"A wild {enemy_name} appears!")
    enemy_health = max_health
    player_health = PLAYER_HEALTH

    while enemy_health > 0 and player_health > 0:
        print(f"Your health: {player_health}   {enemy_name}'s health: {enemy_health}")
        choice = input("1. Attack   2. Defend\n")
        
        if choice == "1":
            player_attack = random.randint(attack_damage // 2, attack_damage)
            enemy_health -= player_attack
            print(f"\nYou attack the {enemy_name} and deal {player_attack} damage!")
            
            if enemy_health <= 0:
                print(f"\nThe {enemy_name} has been defeated!\n")
                return "victory"
            
            enemy_attack = random.randint(1, attack_damage // 2)
            player_health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")
            
        elif choice == "2":
            player_defense = random.randint(1, attack_damage // 3)
            enemy_attack = random.randint(1, attack_damage // 2)
            damage_taken = max(0, enemy_attack - player_defense)
            player_health -= damage_taken
            print(f"\nYou defend against the {enemy_name}'s attack and take {damage_taken} damage.")
            
        else:
            print("Invalid choice. The enemy takes advantage of your hesitation...")
            enemy_attack = random.randint(1, attack_damage // 2)
            player_health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")

    if player_health <= 0:
        print("You have been defeated...")
        return "defeat"

def forest():
    print("""
    You enter the dense forest...
    The air is thick with the scent of pine and damp earth.
    As you walk deeper, you hear rustling in the bushes.
    """)
    return fight_enemy("Bear", 50, 20)

def mountain():
    print("""
    You start your ascent up the steep mountain path...
    The higher you climb, the more breathtaking the view becomes.
    After a challenging climb, you reach a serene mountaintop lake.
    """)
    return fight_enemy("Dragon", 80, 30)

def village():
    print("""
    You head towards the distant village, following the smoke...
    As you approach, you notice the village is under attack by bandits!
    """)
    return fight_enemy("Bandit Leader", 60, 25)

def cave():
    print("""
    You enter the mysterious cave...
    The air is cool and damp, with faint echoes bouncing off the walls.
    As you venture deeper, you notice glowing crystals illuminating the path.
    """)
    return fight_enemy("Cave Troll", 100, 35)

def main():
    intro()
    print("You set off on your epic adventure...\n")
    
    directions = {
        "north": ("Bear", forest),
        "east": ("Dragon", mountain),
        "south": ("Bandit Leader", village),
        "west": ("Cave Troll", cave)
    }
    
    defeated_enemies = []

    while True:
        if len(defeated_enemies) == 4:
            print("\n" * 3)
            print("*" * 68)
            print("*" * 68)
            print("*" * 68)
            print("************************ Congratulations!!! ************************")
            print("You have defeated all the enemies and completed the epic adventure!")
            print("*" * 68)
            print("*" * 68)
            print("*" * 68)
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
