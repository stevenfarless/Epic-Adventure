import random
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple

MAX_HEALTH = 100
PLAYER_BASE_ATTACK = 15
PLAYER_BASE_DEFENSE = 5


DIFFICULTY_SETTINGS: Dict[str, Dict[str, Dict[str, float]]] = {
    "easy": {
        "player": {
            "health": MAX_HEALTH + 30,
            "attack": PLAYER_BASE_ATTACK + 5,
            "defense": PLAYER_BASE_DEFENSE + 3,
        },
        "enemy": {
            "health_multiplier": 0.7,
            "attack_multiplier": 0.75,
            "defense_multiplier": 0.7,
        },
        "rewards": {"health": 25, "attack": 3},
    },
    "medium": {
        "player": {
            "health": MAX_HEALTH,
            "attack": PLAYER_BASE_ATTACK,
            "defense": PLAYER_BASE_DEFENSE,
        },
        "enemy": {
            "health_multiplier": 1.0,
            "attack_multiplier": 1.0,
            "defense_multiplier": 1.0,
        },
        "rewards": {"health": 15, "attack": 2},
    },
    "hard": {
        "player": {
            "health": MAX_HEALTH - 20,
            "attack": PLAYER_BASE_ATTACK - 3,
            "defense": PLAYER_BASE_DEFENSE - 2,
        },
        "enemy": {
            "health_multiplier": 1.4,
            "attack_multiplier": 1.3,
            "defense_multiplier": 1.3,
        },
        "rewards": {"health": 10, "attack": 1},
    },
}


Action = Literal["attack", "defend"]
EncounterMap = Dict[str, "EncounterConfig"]
CombatLog = List[str]


def clear_screen() -> None:
    """Clear the terminal screen by printing blank lines."""
    print("\n" * 50)


@dataclass(frozen=True)
class EncounterConfig:
    name: str
    base_health: int
    base_attack: int
    base_defense: int
    aggression: int
    crossroad_description: str
    intro_text: str
    victory_text: str
    defeat_text: str
    defeat_followup_prompt: Optional[str] = None
    defeat_followup_text: Optional[str] = None


@dataclass
class Player:
    name: str
    difficulty: str
    health: int = field(init=False)
    attack: int = field(init=False)
    defense: int = field(init=False)
    max_health: int = field(init=False)
    level: int = field(default=1)

    def __post_init__(self) -> None:
        player_stats = DIFFICULTY_SETTINGS[self.difficulty]["player"]
        self.health = int(player_stats["health"])
        self.attack = int(player_stats["attack"])
        self.defense = int(player_stats["defense"])
        self.max_health = self.health


@dataclass
class Enemy:
    name: str
    max_health: int
    attack: int
    defense: int
    aggression: int

    @classmethod
    def from_config(cls, config: EncounterConfig, difficulty: str) -> "Enemy":
        multipliers = DIFFICULTY_SETTINGS[difficulty]["enemy"]
        return cls(
            name=config.name,
            max_health=int(config.base_health * multipliers["health_multiplier"]),
            attack=int(config.base_attack * multipliers["attack_multiplier"]),
            defense=int(config.base_defense * multipliers["defense_multiplier"]),
            aggression=config.aggression,
        )


BASE_ENCOUNTERS: Dict[str, EncounterConfig] = {
    "north": EncounterConfig(
        name="Bear",
        base_health=50,
        base_attack=15,
        base_defense=3,
        aggression=75,
        crossroad_description=(
            "To the North:\tYou see a dense forest stretching as far as the eye can see."
        ),
        intro_text=(
            "\n\tYou enter the dense forest.\n"
            "The air is thick with the scent of pine and damp earth.\n"
            "As you walk deeper, you hear rustling in the bushes.\n"
            "You try to ignore it and decide to keep walking. \n"
            "Before you can take another step, out lunges a wild bear!\n"
            "It's hungry as heck and you look delicious!\n"
        ),
        victory_text=(
            "Feeling triumphant after defeating the bear, you continue your journey.\n"
        ),
        defeat_text=(
            "The bear's attack overwhelms you.\n"
            "You hear the bear say a prayer, thanking his bear deity for this delicious feast.\n"
        ),
        defeat_followup_prompt="[Press ENTER to say 'Amen' with the bear]",
        defeat_followup_text=(
            "You can't talk. The bear ripped your throat out.\n\tBummer."
        ),
    ),
    "east": EncounterConfig(
        name="Bandit Leader",
        base_health=70,
        base_attack=18,
        base_defense=5,
        aggression=60,
        crossroad_description=(
            "To the East:\tYou see smoke rising from a distant village."
        ),
        intro_text=(
            "\n\tAs you head towards the distant village,\n"
            "following the trail of smoke, you notice something alarming:\n"
            "the village is under attack by a group of bandits!\n"
            "\tTheir leader gestures to his gang, and they quickly encircle you both.\n"
            "Their chants of 'FIGHT! FIGHT! FIGHT!' echo through the air."
        ),
        victory_text=(
            "With the bandit leader defeated, the villagers thank you and you continue your journey.\n"
        ),
        defeat_text=(
            "The bandit leader lands his final blow. The bandits fight over who gets to keep your sweet loot.\n"
            "You try to get up and retreat, but the bandits stole your feet."
        ),
    ),
    "south": EncounterConfig(
        name="Cave Troll",
        base_health=90,
        base_attack=22,
        base_defense=8,
        aggression=85,
        crossroad_description=(
            "To the South:\tYou see a mysterious cave entrance beckoning with an eerie glow."
        ),
        intro_text=(
            "\n\tYou enter the mysterious cave.\n"
            "The air is cool and damp, with faint echoes bouncing off the walls.\n"
            "As you venture deeper, you notice glowing crystals illuminating the path.\n"
            "You start to feel uneasy, so you turn around to leave.\n"
            "You turn and find yourself face to face with a troll!\n"
            "\t'Your bones will make a great addition to my collection!'"
        ),
        victory_text=(
            "The defeated troll slumps to the ground, allowing you to proceed deeper into the cave.\n"
        ),
        defeat_text=(
            "The troll's brute strength overwhelms you.\n"
            "You attempt to retreat from the cave to die in peace, but you are trapped.\n\n"
            "Your bones join the pile of hundreds of other stupid...\nI mean...\nbrave...\nadventurers."
        ),
    ),
    "west": EncounterConfig(
        name="Dragon",
        base_health=150,
        base_attack=28,
        base_defense=10,
        aggression=50,
        crossroad_description=(
            "To the West:\tYou see a narrow path leading up a steep mountain."
        ),
        intro_text=(
            "\n\tYou start your ascent up the steep mountain path.\n"
            "The higher you climb, the more breathtaking the view becomes.\n"
            "After a challenging climb, you reach a serene mountaintop lake.\n"
            "\tThe air grows suddenly cold.\n"
            "The wind picks up, carrying a bone-chilling roar that echoes through the peaks.\n"
            "Your heart pounds as a colossal shadow blots out the sun.\n"
            "With a thunderous crash, a dragon descends from the swirling clouds,\n"
            "its scales gleaming ominously. Its piercing eyes lock onto you,\n"
            "and its wings cast a dark shadow over the lake.\n"
            "The ground trembles beneath its massive claws as it emits a low, rumbling growl.\n\n"
            "You ready your weapon"
        ),
        victory_text=(
            "Filled with adrenaline from defeating the dragon, you continue your journey.\n"
        ),
        defeat_text=(
            "The dragon's fire leaves you badly burned. You retreat from the mountain to die in peace.\n"
        ),
    ),
}


MARCUS_ROCK_ENCOUNTER = EncounterConfig(
    name="Rock",
    base_health=500,
    base_attack=0,
    base_defense=0,
    aggression=0,
    crossroad_description=(
        "To the Campfire:\tYou see a cozy campfire with your best friend Robert."
    ),
    intro_text=(
        "\n\tYou are sitting around a campfire, just living your best wormy life with your best friend Robert. "
        "You notice something is off but you can't put your freakishly long finger on it. After a brief moment of hypervigilance, "
        "something catches your big ol' eye. There's something about that rock. That rock right there. It's... It's... IT'S PISSING YOU OFF! "
        "You tell Robert but he is of little help. You are left with no other choice than to give that stupid smug little stupid smug rock a piece of your mind.\n"
    ),
    victory_text=(
        "The rock crumbles into dust.\nRobert looks at you with concern.\n'You okay, buddy?' he asks.\nYou feel strangely satisfied.\n"
    ),
    defeat_text=(
        "You somehow died fighting a rock.\nA ROCK.\nRobert will never let you live this down.\n...Oh wait, you're dead.\n"
    ),
)



ROBERT_CAMPFIRE_ENCOUNTER = EncounterConfig(
    name="Marcus's Sanity",
    base_health=1,  # Doesn't matter, we'll handle this specially
    base_attack=0,
    base_defense=0,
    aggression=0,
    crossroad_description=(
        "To the Campfire:\tYou see a cozy campfire with your best friend Marcus."
    ),
    intro_text=(
        "\n\tYou're relaxing by a warm campfire with your best friend Marcus, roasting marshmallows and enjoying the peaceful evening. "
        "The stars twinkle overhead, the fire crackles gently... it's perfect.\n\n"
        "\tThen Marcus stands up.\n\n"
        "He walks over to a nearby rock. A perfectly innocent rock. Without a word, without warning, "
        "\"Robert...\" Marcus mutters, \"I don't like that rock\"\n\n"
        "he raises his fist and slams it down onto the rock with the fury of a thousand suns.\n\n"
        "\"Take that, you smug little pebble!\" he says calm and monotone.\n\n"
        "You watch in stunned silence as Marcus proceeds to beat the everloving heck out of this poor innocent rock."
        "His fists are a blur. The rock doesn't stand a chance. Chunks of stone fly in every direction.\n\n"
        "\"It's pissing me off.\" Marcus mutters in his trademark sociopathic wormitude.\n\n"
        # "In a blind fit of the calmest, slowest, most uneccessary rage, he dives face first directly into the campfire.\n"
    ),
    victory_text=(
        "Marcus crawls out of the fire, singed but alive. He's coughing up smoke and his eyebrows are gone. Or did he even have any to begin with?\n"
        "\"Thanks... Robert\" he wheezes. \"You saved my life. That rock had it coming though.\"\n"
        "You both agree to never speak of this again. The adventure continues.\n"
    ),
    defeat_text=(
        "You couldn't save him. Marcus remains in the fire, a monument to poor decision-making and rock-related rage.\n"
        "You continue your adventure alone, forever haunted by the memory of your friend's final words: \"It's pissing me off.\"\n"
    ),
)

def validate_input(prompt: str, valid_inputs: List[str]) -> str:
    """Prompt the user until they supply a value contained in ``valid_inputs``."""

    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_inputs:
            return choice
        print("Invalid input. Please try again.")


def calculate_damage(attacker_power: int, defender_defense: int) -> int:
    """Return a randomized damage value that respects attacker power and defense."""

    base_damage = max(attacker_power - (defender_defense // 2), 1)
    minimum = max(int(base_damage * 0.85), 1)
    maximum = max(int(base_damage * 1.15), minimum)
    damage = random.randint(minimum, maximum)
    return max(damage, 3)


def calculate_status_width(player: Player, enemy: Enemy) -> int:
    """Determine the width required to display the combat status block."""

    label_padding = len("'s health: ")
    name_width = max(len(player.name), len(enemy.name)) + label_padding
    health_width = max(len(str(player.max_health)), len(str(enemy.max_health)))
    return name_width + health_width


def print_health_status(
    player: Player,
    enemy_name: str,
    enemy_health: int,
    status_width: int,
) -> None:
    """Render the combatants' health values in an aligned format."""

    label_suffix = "'s health: "
    player_padding = status_width - len(player.name) - len(label_suffix)
    enemy_padding = status_width - len(enemy_name) - len(label_suffix)
    print(
        f"\n{player.name}{label_suffix}"
        f"{player.health:>{player_padding}}"
    )
    print(
        f"{enemy_name}{label_suffix}"
        f"{enemy_health:>{enemy_padding}}"
    )


def apply_victory_rewards(player: Player) -> None:
    """Apply the configured post-battle rewards for the player's difficulty."""

    rewards = DIFFICULTY_SETTINGS[player.difficulty]["rewards"]
    player.health = min(player.health + int(rewards["health"]), player.max_health)
    player.attack += int(rewards["attack"])
    player.level += 1


def handle_enemy_defeat(player: Player, enemy_name: str) -> None:
    """Celebrate the enemy's defeat and grant the associated rewards."""

    print(f"The {enemy_name} has been defeated! You gain experience and rest!\n")
    apply_victory_rewards(player)
    input("[Continue]")


def describe_crossroad(
    player: Player,
    encounters: EncounterMap,
    defeated_enemies: List[str],
    intro_template: str,
) -> None:
    """Display the available paths and any previously defeated enemies."""

    path_count = "five" if "campfire" in encounters else "four"
    print(f"\nHello {player.name}.\n")
    print(intro_template.format(path_count=path_count))
    for direction in encounters:
        print(encounters[direction].crossroad_description)
    print()
    if defeated_enemies:
        print(f"Defeated enemies: {', '.join(defeated_enemies)}\n")


def build_direction_prompt(encounters: EncounterMap) -> str:
    """Build the input prompt listing available encounter directions."""

    options = " / ".join(direction.title() for direction in encounters)
    return f"Which direction will you choose? ({options})\n> "


def enemy_choose_action(enemy: Enemy, enemy_health: int) -> Action:
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
        weights=[attack_chance, defend_chance],
    )[0]
    return action


def player_attack_round(
    player: Player,
    enemy: Enemy,
    enemy_health: int,
    enemy_action: Action,
) -> Tuple[int, bool, CombatLog]:
    """Resolve the events for a player attack turn."""

    messages: CombatLog = []
    player_damage = calculate_damage(player.attack, enemy.defense)

    if enemy_action == "attack":
        enemy_health -= player_damage
        messages.append(f"{player.name} attacked and dealt {player_damage} damage!")

        if enemy_health <= 0:
            return enemy_health, True, messages

        enemy_damage = calculate_damage(enemy.attack, player.defense)
        player.health -= enemy_damage
        messages.append(
            f"The {enemy.name} attacked back and dealt {enemy_damage} damage!"
        )
        return enemy_health, False, messages

    reduced_damage = player_damage // 2
    counter_damage = enemy.attack // 3
    enemy_health -= reduced_damage
    player.health -= counter_damage

    messages.append(f"{player.name} attacked for {player_damage} damage!")
    messages.append(
        f"The {enemy.name} raised its guard and blocked most of it! "
        f"Only took {reduced_damage} damage."
    )
    messages.append(f"Its counterattack dealt {counter_damage} damage to you!")

    return enemy_health, enemy_health <= 0, messages


def player_defend_round(
    player: Player,
    enemy: Enemy,
    enemy_health: int,
    enemy_action: Action,
) -> Tuple[int, CombatLog]:
    """Resolve the events for a player defend turn."""

    messages: CombatLog = []

    if enemy_action == "attack":
        enemy_damage = calculate_damage(enemy.attack, player.defense)
        reduced_damage = enemy_damage // 2
        counter_damage = player.attack // 3

        player.health -= reduced_damage
        enemy_health -= counter_damage

        messages.append(f"{player.name} raised their guard!")
        messages.append(
            f"The {enemy.name} attacked for {enemy_damage} damage, but you blocked most of it!"
        )
        messages.append(
            f"You took {reduced_damage} damage and countered for {counter_damage} damage!"
        )
        return enemy_health, messages

    player.health -= 2
    enemy_health -= 2

    messages.append(f"{player.name} and the {enemy.name} both brace for impact!")
    messages.append("You circle each other warily. Both take 2 damage from exhaustion.")
    return enemy_health, messages



def robert_watch_marcus_fight(player: Player) -> Optional[str]:
    """Special encounter where Robert watches Marcus fight a rock and throw himself in a fire."""
    help_attempts = 0
    marcus_phrases = [
        "\"Help me... Robert...\"",
        "\"Robert... This hurts worse than getting shanked in the leg by Big Badinky Bones at Panera Bread.\"",
        "\"Robert... Why did you allow me to yeet myself into this fire?\"",
        "\"Robert... This fire is pissing me off.\""
    ]

    # Phase 1: Watch Marcus beat up the rock
    clear_screen()
    print("\nMarcus is absolutely destroying this rock. Pebbles everywhere.\n")
    print("His knuckles are bleeding. The rock is 50% dust now. He's not stopping.\n")
    input("[Continue]")

    clear_screen()
    print("\nThe rock is now gravel. Marcus raises his arms in triumph.\n")
    print('\"Victory...\" he says calmly and monotone to the heavens.\n')
    print("\nThen... he looks at the campfire.\n")
    input("[Continue]")

    clear_screen()
    print("\n\"The rock... it made me do terrible things,\" Marcus says.\n")
    print('\"There\'s only one way to cleanse this guilt...\"\n')
    print("\nBefore you can stop him, in a blind fit of the calmest, slowest, most uneccessary rage, he dives face first directly into the campfire.\n")
    input("[Continue]")

    # Phase 2: The rescue attempts
    while help_attempts < 3:
        clear_screen()
        if help_attempts == 0:
            print("\nMarcus is rolling around in the fire, screaming for help.\n")
            print("The flames are everywhere. This is a disaster.\n")
        elif help_attempts == 1:
            print("\nMarcus is still in the fire. He's doing this weird flailing thing.\n")
            print("Is he... is he swimming in the fire? That's not helping, Marcus.\n")
        else:
            print("\nMarcus has given up flailing. He's just lying there dramatically.\n")
            print("But he's still saying Robert. So at least he's alive.\n")

        print(f"\nMarcus: {marcus_phrases[help_attempts]}\n")

        choice = validate_input("1. Help Marcus\n2. Tell him to get out\n> ", ["1", "2"])

        clear_screen()

        if choice == "1":
            help_attempts += 1
            if help_attempts < 3:
                print("\nYou reach toward the fire to help Marcus!\n")
                print("\nBut the heat is too intense! You pull back, singed.\n")
                print("Marcus continues writhing in the flames.\n")
                # print('\"I CAN SEE MY ANCESTORS! THEY\'RE DISAPPOINTED!\" Marcus wails.\n')
                input("[Continue]")
            else:
                # Success!
                print("\nWith a heroic burst of determination, you grab a nearby branch!\n")
                print("You extend it to Marcus. He grabs hold!\n")
                print("\nWith a mighty heave, you YANK Marcus out of the fire!\n")
                print("He tumbles onto the ground, smoking and coughing.\n")
                input("[Continue]")

                clear_screen()
                print('\nMarcus looks up at you with tears in his eyes.\n')
                print('\"That rock... it was so smug, Robert. So smug.\"\n')
                print("\nYou help him to his feet. His hair is mostly gone.\n")
                print('\"We don\'t talk about this,\" you say firmly.\n')
                print('\"Agreed,\" Marcus nods. \"What rock?\"\n')
                input("[Continue]")

                return "victory"
        else:  # choice == "2"
            print("\n\"Marcus, just GET OUT!\" you yell.\n")
            print("\nMarcus looks at you from the flames.\n")
            print(f"\nMarcus: {marcus_phrases[min(help_attempts, len(marcus_phrases)-1)]}\n")
            print("\nYeah, that's not working.\n")
            input("[Continue]")

    return "victory"


def fight_enemy(enemy: Enemy, player: Player) -> Optional[str]:
    enemy_health = enemy.max_health
    status_width = calculate_status_width(player, enemy)

    while enemy_health > 0 and player.health > 0:
        clear_screen()
        print_health_status(player, enemy.name, enemy_health, status_width)

        choice = validate_input("1. Attack   2. Defend\n> ", ["1", "2"])

        clear_screen()
        print_health_status(player, enemy.name, enemy_health, status_width)
        print()

        enemy_action = enemy_choose_action(enemy, enemy_health)

        if choice == "1":
            enemy_health, enemy_defeated, messages = player_attack_round(
                player, enemy, enemy_health, enemy_action
            )
            for message in messages:
                print(message)

            if enemy_defeated:
                handle_enemy_defeat(player, enemy.name)
                return "victory"

        else:
            enemy_health, messages = player_defend_round(
                player, enemy, enemy_health, enemy_action
            )
            for message in messages:
                print(message)

        if enemy_health <= 0:
            handle_enemy_defeat(player, enemy.name)
            return "victory"

        if player.health <= 0:
            input("[Continue]")
            return "game_over"

        input("[Continue]")

    return None


def scenario(player: Player, encounter: EncounterConfig) -> Optional[str]:
    """Play through a single encounter and return the resulting state."""
    # Special handling for Robert's campfire encounter
    if encounter.name == "Marcus's Sanity":
        clear_screen()
        print(encounter.intro_text)
        input("[Continue]")
        result = robert_watch_marcus_fight(player)
        clear_screen()
        if result == "victory":
            print(encounter.victory_text)
            input("[Continue]")
        return result

    enemy = Enemy.from_config(encounter, player.difficulty)
    clear_screen()
    print(encounter.intro_text)
    input("[Continue]")

    result = fight_enemy(enemy, player)

    clear_screen()
    if result == "victory":
        print(encounter.victory_text)
        input("[Continue]")
        return "victory"

    if result == "game_over":
        print(encounter.defeat_text)
        if encounter.defeat_followup_prompt:
            input(encounter.defeat_followup_prompt)
            if encounter.defeat_followup_text:
                print(encounter.defeat_followup_text)
        input("[Continue]")
        return "game_over"

    return result


def main() -> None:
    """Run the adventure game loop."""

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

    is_marcus = player.name.lower() == "marcus"
    is_robert = player.name.lower() == "robert"

    encounters: EncounterMap = dict(BASE_ENCOUNTERS)
    if is_marcus:
        encounters["campfire"] = MARCUS_ROCK_ENCOUNTER
    if is_robert:
        encounters["campfire"] = ROBERT_CAMPFIRE_ENCOUNTER

    defeated_enemies: List[str] = []
    first_visit = True

    while True:
        if len(defeated_enemies) == len(encounters):
            clear_screen()
            print(
                f"\nCongratulations {player.name}!!! You have defeated all the enemies "
                f"and completed the epic adventure on {difficulty.upper()} mode!\n"
            )
            input("Press ENTER to end game and get back to your life, loser.")
            break

        clear_screen()
        intro_template = (
            "You find yourself suddenly teleported to an unfamiliar crossroad surrounded by {path_count} different paths.\n"
            if first_visit
            else "You find yourself at the crossroad surrounded by {path_count} different paths.\n"
        )
        describe_crossroad(player, encounters, defeated_enemies, intro_template)
        first_visit = False

        direction = validate_input(
            build_direction_prompt(encounters),
            list(encounters.keys()),
        )

        if direction in defeated_enemies:
            print("You have already cleared this path. Try another direction.")
            input("[Continue]")
            continue

        result = scenario(player, encounters[direction])
        if result == "victory":
            defeated_enemies.append(direction)
        elif result == "game_over":
            clear_screen()
            print("\nUnfortunately, your adventure has come to an end.\n")
            input("Press ENTER to die.")
            print("\nx_x You died.\n")
            input("Exit")
            break


if __name__ == "__main__":
    main()
