import random

# Initial player health
PLAYER_HEALTH = 100

class Player:
    def __init__(self, name):
        self.name = name
        self.health = PLAYER_HEALTH

def intro():
    """Introduction and player name input"""
    print("""
    ********************************************************************************
    ********************************************************************************
    ************************ Welcome to the Epic Adventure! ************************
    ********************************************************************************
    ********************************************************************************
    """)
    input("Press Enter to continue...")
    player_name = input("What is your name? ")

    print(f"\nHello, {player_name}. You find yourself at a crossroads.\n")
    input("[Continue]")
    print("""To the NORTH:
    You see a dense forest stretching as far as the eye can see.""")
    input("[Continue]")
    print("""To the EAST:
    You see a narrow path leading up a steep mountain.""")
    input("[Continue]")
    print("""To the SOUTH:
    You see smoke rising from a distant village.""")
    input("[Continue]")
    print("""To the WEST:
    You see a mysterious cave entrance beckoning with an eerie glow.""")
    input("[Continue]")
    return Player(player_name)

def fight_enemy(enemy_name, max_health, attack_damage, player):
    """Simulates a fight between the player and an enemy"""
    enemy_health = max_health

    while enemy_health > 0 and player.health > 0:
        print(f"\nYour health: {player.health}   {enemy_name}'s health: {enemy_health}")
        choice = input("1. Attack   2. Defend\n")
        
        if choice == "1":
            player_attack = random.randint(attack_damage // 2, attack_damage)
            enemy_health -= player_attack
            print(f"\nYou attack the {enemy_name} and deal {player_attack} damage!")
            
            if enemy_health <= 0:
                print(f"\nThe {enemy_name} has been defeated!\n")
                player.health += 10  # Increase player health by 10
                if player.health > PLAYER_HEALTH:  # Ensure player health does not exceed max
                    player.health = PLAYER_HEALTH
                return "victory"
            
            enemy_attack = random.randint(1, attack_damage // 2)
            player.health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")
            
        elif choice == "2":
            player_defense = random.randint(1, attack_damage // 3)
            enemy_attack = random.randint(1, attack_damage // 2)
            damage_taken = max(0, enemy_attack - player_defense)
            player.health -= damage_taken
            print(f"\nYou defend against the {enemy_name}'s attack and take {damage_taken} damage.")
            
        else:
            print("Invalid choice. The enemy takes advantage of your hesitation.")
            enemy_attack = random.randint(1, attack_damage // 2)
            player.health -= enemy_attack
            print(f"The {enemy_name} attacks you and deals {enemy_attack} damage!")

    if player.health <= 0:
        print("\nYou have been defeated.")
        return "game_over"  # Signal game over

def forest(player):
    """Handles the forest scenario and fight"""
    print("\nYou enter the dense forest.")
    input("[Continue]")
    print("The air is thick with the scent of pine and damp earth.")
    input("[Continue]")
    print("As you walk deeper, you hear rustling in the bushes.")
    input("[Continue]")
    return fight_enemy("Bear", 50, 20, player)

def mountain(player):
    """Handles the mountain scenario and fight"""
    print("You start your ascent up the steep mountain path.")
    input("[Continue]")
    print("The higher you climb, the more breathtaking the view becomes.")
    input("[Continue]")
    print("After a challenging climb, you reach a serene mountaintop lake.")
    input("[Continue]")
    return fight_enemy("Dragon", 80, 30, player)

def village(player):
    """Handles the village scenario and fight"""
    print("You head towards the distant village, following the smoke.")
    input("[Continue]")
    print("As you approach, you notice the village is under attack by bandits!")
    input("[Continue]")
    return fight_enemy("Bandit Leader", 60, 25, player)

def cave(player):
    """Handles the cave scenario and fight"""
    print("\nYou enter the mysterious cave.")
    input("[Continue]")
    print("The air is cool and damp, with faint echoes bouncing off the walls.")
    input("[Continue]")
    print("As you venture deeper, you notice glowing crystals illuminating the path.")
    input("[Continue]")
    return fight_enemy("Cave Troll", 100, 35, player)

def main():
    """Main function to drive the game"""
    player = intro()
    print("\nYou set off on your epic adventure!\n")
    input("[Continue]")
    
    directions = {
        "north": ("Bear", forest),
        "east": ("Dragon", mountain),
        "south": ("Bandit Leader", village),
        "west": ("Cave Troll", cave)
    }
    
    defeated_enemies = []

    while True:
        if len(defeated_enemies) == 4:
            input("Press ENTER to continue")
            print("\n" * 3)
            print("*" * 68)
            print("*" * 68)
            print("*" * 68)
            print(f"**************** Congratulations {player.name}!!! *******************")
            print("You have defeated all the enemies and completed the epic adventure!")
            print("*" * 68)
            print("*" * 68)
            print("*" * 68)
            input("Press ENTER to end the game.")
            break
        
        direction = input("Which direction will you choose? (North / East / South / West)\n").lower()
        
        if direction in directions:
            enemy_name, location_function = directions[direction]
            
            if direction in defeated_enemies:
                print(f"\nYou have already defeated the {enemy_name}.\n")
                input("[Continue]")
                print("Choose another direction.")
                continue
            else:
                result = location_function(player)
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
