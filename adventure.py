import random
# Enable ANSI colors on Windows
# ANSI Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Player data dictionary
player = {
    "health": 100,
    "max_health": 100,
    "gold": 20,
    "inventory": [],
    "location": "clearing"
}

# Items database dictionary
items_db = {
    "Health Potion": {"type": "consumable", "heal": 50, "cost": 15},
    "Ancient Sword": {"type": "weapon", "damage_bonus": 10},
    "Magic Amulet": {"type": "special", "effect": "breaks_shield"},
    "Bear Pelt Armor": {"type": "armor", "damage_reduction": 5}
}

# Game flags dictionary
game_flags = {
    "bear_defeated": False,
    "witch_defeated": False,
    "cave_searched": False,
    "enemies_defeated": 0
}


def pause():
    # Wait for user input before continuing.
    input("\nPress Enter to continue...")


def display_status():
    # Display player's current status.
    inv_display = format_inventory_short()
    print("=" * 40)
    health_color = GREEN if player['health'] > 50 else YELLOW if player['health'] > 25 else RED
    print(
        f"Health: {health_color}{player['health']}/{player['max_health']}{RESET} | Gold: {YELLOW}{player['gold']}{RESET}")
    print(f"Inventory: {CYAN}{inv_display}{RESET}")
    print("=" * 40)


def format_inventory_short():
    # Format inventory for status display.
    if not player["inventory"]:
        return "Empty"

    # Count items using linear search algorithm
    item_counts = {}
    for item in player["inventory"]:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    formatted = []
    for item, count in item_counts.items():
        if count > 1:
            formatted.append(f"{item} x{count}")
        else:
            formatted.append(item)

    return ", ".join(formatted)


def get_valid_input(prompt, valid_choices):
    # Get valid input from user.
    # Uses linear search to validate input against valid choices.
    # Time Complexity: O(n) where n is number of valid choices
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")


def add_to_inventory(item_name):
    # Add item to player inventory.
    player["inventory"].append(item_name)
    print(f"{GREEN}You obtained: {item_name}!{RESET}")


def remove_from_inventory(item_name):
    # Remove item from inventory using linear search.
    # Time Complexity: O(n) where n is inventory size
    for i, item in enumerate(player["inventory"]):
        if item == item_name:
            player["inventory"].pop(i)
            return True
    return False


def has_item(item_name):
    # Check if player has item using linear search.
    # Time Complexity: O(n) where n is inventory size
    for item in player["inventory"]:
        if item == item_name:
            return True
    return False


def use_item(item_name):
    """Use a consumable item."""
    if not has_item(item_name):
        print(f"{RED}You don't have that item!{RESET}")
        return False

    if item_name == "Health Potion":
        heal_amount = min(items_db["Health Potion"]["heal"],
                          player["max_health"] - player["health"])
        player["health"] += heal_amount
        remove_from_inventory("Health Potion")
        print(f"{GREEN}You used a Health Potion and restored {heal_amount} HP!{RESET}")
        return True

    return False


# INVENTORY SYSTEM

def check_inventory():
    # Display detailed inventory.
    print(f"{BOLD}{CYAN}=== INVENTORY ==={RESET}")

    if not player["inventory"]:
        print(f"{DIM}Your inventory is empty.{RESET}")
    else:
        # Count and display items
        item_counts = {}
        for item in player["inventory"]:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

        for item, count in item_counts.items():
            print(f"  - {CYAN}{item}{RESET} x{count}")

    print(f"\nGold: {YELLOW}{player['gold']}{RESET}")
    pause()

# COMBAT SYSTEM

def combat(enemy_name, enemy_hp, enemy_max_hp, enemy_attack_min, enemy_attack_max,
           rewards, has_shield=False, shield_reduction=0):
    current_enemy_hp = enemy_hp
    defending = False
    turn_count = 0
    shield_active = has_shield
    
    # Check if player has Magic Amulet to break shield at start
    if shield_active and has_item("Magic Amulet"):
        print(f"\n{PURPLE}Your Magic Amulet glows and shatters the enemy's shield!{RESET}")
        shield_active = False

    while current_enemy_hp > 0 and player["health"] > 0:
        turn_count += 1

        # Display combat status
        print(f"\n{'=' * 40}")
        print(f"  {BOLD}{RED}COMBAT: {enemy_name.upper()}{RESET}")
        print("=" * 40)
        enemy_health_color = GREEN if current_enemy_hp > enemy_max_hp * \
            0.5 else YELLOW if current_enemy_hp > enemy_max_hp * 0.25 else RED
        print(
            f"{enemy_name} Health: {enemy_health_color}{current_enemy_hp}/{enemy_max_hp}{RESET}")
        if has_shield:
            status = f"{PURPLE}ACTIVE{RESET}" if shield_active else f"{DIM}BROKEN{RESET}"
            print(
                f"Shield: {status}" + (f" (Reduces damage by {shield_reduction})" if shield_active else ""))
        health_color = GREEN if player['health'] > 50 else YELLOW if player['health'] > 25 else RED
        print(
            f"Your Health: {health_color}{player['health']}/{player['max_health']}{RESET}")
        print("=" * 40)

        # Player turn menu
        print("\nYour Turn:")
        print("1. Attack")
        print("2. Defend (Block 50% of next attack)")
        print("3. Use Item")
        print("4. Attempt to Flee (30% chance)")
        valid = ["1", "2", "3", "4"]
        flee_chance = 30

        choice = get_valid_input("\nChoice: ", valid)

        # Process player action
        if choice == "1":  # Attack
            # Calculate damage based on weapon
            if has_item("Ancient Sword"):
                damage = random.randint(15, 25)
            else:
                damage = random.randint(10, 15)

            # Apply shield reduction
            actual_damage = damage
            if shield_active:
                actual_damage = max(0, damage - shield_reduction)
                print(
                    f"\n{RED}You attack for {damage} damage, but the shield absorbs {shield_reduction}!{RESET}")
                print(f"Actual damage: {RED}{actual_damage}{RESET}")
            else:
                print(f"\n{RED}You attack for {damage} damage!{RESET}")

            current_enemy_hp -= actual_damage
            defending = False

        elif choice == "2":  # Defend
            print(f"\n{BLUE}You brace yourself for the next attack...{RESET}")
            defending = True

        elif choice == "3":  # Use Item
            potions = [i for i, item in enumerate(
                player["inventory"]) if item == "Health Potion"]
            if not potions:
                print(f"\n{YELLOW}You have no usable items!{RESET}")
                defending = False
            else:
                print("\nInventory:")
                inv_items = []
                for i, item in enumerate(player["inventory"]):
                    if item == "Health Potion":
                        inv_items.append((i, item))
                        print(f"{len(inv_items)}. {item}")

                print("0. Cancel")
                item_choice = get_valid_input("Choose item: ",
                                              [str(i) for i in range(len(inv_items) + 1)])

                if item_choice != "0":
                    use_item("Health Potion")
                else:
                    # Cancelled - don't consume turn, let player choose again
                    continue
                defending = False

        else:  # Flee (choice 4)
            flee_roll = random.randint(1, 100)
            if flee_roll <= flee_chance:
                print(f"\n{GREEN}You successfully fled!{RESET}")
                gold_dropped = min(10, player["gold"])
                player["gold"] = max(0, player["gold"] - 10)
                if gold_dropped > 0:
                    print(f"{YELLOW}You dropped {gold_dropped} gold while running!{RESET}")
                pause()
                return False
            else:
                print(f"\n{RED}Failed to escape!{RESET}")
                defending = False

        # Check if enemy defeated
        if current_enemy_hp <= 0:
            break

        # Enemy turn
        print(f"\n{enemy_name}'s Turn:")

        # Calculate armor reduction
        armor_reduction = 0
        if has_item("Bear Pelt Armor"):
            armor_reduction = items_db["Bear Pelt Armor"]["damage_reduction"]

        # Special witch mechanics
        if enemy_name == "Witch":
            # Curse every 3rd turn
            if turn_count % 3 == 0:
                curse_damage = 10
                if defending:
                    curse_damage = curse_damage // 2
                curse_damage = max(0, curse_damage - armor_reduction)
                if defending:
                    print(
                        f"{PURPLE}Dark energy wraps around you, sapping your strength!{RESET}")
                    print(
                        f"Your defense reduces the damage! You take {RED}{curse_damage}{RESET} damage!")
                else:
                    print(f"{PURPLE}The witch curses you with dark magic!{RESET}")
                    if armor_reduction > 0:
                        print(
                            f"{BLUE}Your armor absorbs {armor_reduction} damage!{RESET}")
                    print(f"You take {RED}{curse_damage}{RESET} damage!")
                player["health"] -= curse_damage
            else:
                # Regular attack with rage bonus when low HP
                enemy_damage = random.randint(
                    enemy_attack_min, enemy_attack_max)
                if current_enemy_hp < 20:
                    enemy_damage += 5
                    print(f"{RED}The witch's eyes glow with fury!{RESET}")

                if defending:
                    enemy_damage = enemy_damage // 2
                enemy_damage = max(0, enemy_damage - armor_reduction)

                if defending:
                    print(
                        f"{PURPLE}The witch hurls a bolt of purple energy at you!{RESET}")
                    print(
                        f"You block some of it! You take {RED}{enemy_damage}{RESET} damage!")
                else:
                    print(
                        f"{PURPLE}The witch hurls a bolt of purple energy at you!{RESET}")
                    if armor_reduction > 0:
                        print(
                            f"{BLUE}Your armor absorbs {armor_reduction} damage!{RESET}")
                    print(f"You take {RED}{enemy_damage}{RESET} damage!")

                player["health"] -= enemy_damage
        else:
            # Regular enemy attack
            enemy_damage = random.randint(enemy_attack_min, enemy_attack_max)

            if defending:
                enemy_damage = enemy_damage // 2
            enemy_damage = max(0, enemy_damage - armor_reduction)

            if defending:
                print(f"The {enemy_name} attacks!")
                print(
                    f"You block some damage! You take {RED}{enemy_damage}{RESET} damage!")
            else:
                print(
                    f"The {enemy_name} attacks for {RED}{enemy_damage}{RESET} damage!")
                if armor_reduction > 0:
                    print(
                        f"{BLUE}Your armor absorbed {armor_reduction} damage!{RESET}")

            player["health"] -= enemy_damage

        defending = False

        # Check player defeat
        if player["health"] <= 0:
            print(f"\n{RED}You have been defeated...{RESET}")
            pause()
            return False

        pause()

    # Victory
    print(f"\n{GREEN}{BOLD}Victory! You defeated the {enemy_name}!{RESET}")
    print(f"\n{YELLOW}You gained {rewards['gold']} gold!{RESET}")
    player["gold"] += rewards["gold"]

    for item in rewards.get("items", []):
        add_to_inventory(item)

    game_flags["enemies_defeated"] += 1
    pause()
    return True

# LOCATION: DARK CAVE


def bear_encounter():
    if game_flags["bear_defeated"]:
        # Repeat visit - chance for bear respawn or random loot
        respawn_chance = random.randint(1, 100)

        if respawn_chance <= 40:
            # 40% chance - A new bear has moved in!
            print(f"\n{YELLOW}A new bear has made this den its home!{RESET}")
            print("It looks angry at your intrusion...")
            print("\nWhat do you do?")
            print("1. Fight the bear")
            print("2. Run away")

            choice = get_valid_input("\nChoice: ", ["1", "2"])

            if choice == "1":
                # Fight the new bear (weaker, less rewards)
                victory = combat("Bear", 40, 40, 8, 15,
                                 {"gold": 15, "items": ["Health Potion"]})
                if not victory and player["health"] <= 0:
                    return "game_over"
                # Bear doesn't stay defeated on respawns - it can keep respawning
            else:
                print("\nYou quickly retreat from the angry bear!")
            pause()
            return None
        else:
            # 60% chance - Den is empty, but random loot
            print("\nThe bear's den is empty...")
            print("You scavenge through the remains...")

            found_something = False

            # Random gold (60% chance, 1-15 gold)
            if random.randint(1, 100) <= 60:
                gold_found = random.randint(1, 15)
                player["gold"] += gold_found
                print(f"  - {YELLOW}{gold_found} gold{RESET}")
                found_something = True

            # Random Health Potion (25% chance)
            if random.randint(1, 100) <= 25:
                add_to_inventory("Health Potion")
                found_something = True

            if not found_something:
                # Fallback - at least give a few gold
                gold_found = random.randint(1, 5)
                player["gold"] += gold_found
                print(f"  - {YELLOW}{gold_found} gold{RESET}")

            pause()
            return None

    # First encounter - original logic
    print("\nYou find a large bear sleeping in its den!")
    print("You see a shiny sword behind it...")
    print("\nWhat do you do?")
    print("1. Try to sneak past (50% chance)")
    print("2. Fight the bear")
    print("3. Go back")

    choice = get_valid_input("\nChoice: ", ["1", "2", "3"])

    if choice == "1":
        # Sneak attempt - 50% chance
        sneak_roll = random.randint(1, 100)
        if sneak_roll <= 50:
            print("\nYou carefully sneak past the sleeping bear...")
            print("Success! You grab the sword!")
            add_to_inventory("Ancient Sword")
            player["gold"] += 30
            print("You also found 30 gold!")
            game_flags["bear_defeated"] = True
        else:
            print("\n*CRACK!*")
            print("\nYou step on a twig!")
            print("The bear wakes up and roars!")
            pause()
            # Start combat
            victory = combat("Bear", 50, 50, 10, 20,
                             {"gold": 30, "items": ["Ancient Sword", "Bear Pelt Armor"]})
            if victory:
                game_flags["bear_defeated"] = True
            elif player["health"] <= 0:
                return "game_over"

    elif choice == "2":
        # Direct fight
        victory = combat("Bear", 50, 50, 10, 20,
                         {"gold": 30, "items": ["Ancient Sword", "Bear Pelt Armor"]})
        if victory:
            game_flags["bear_defeated"] = True
        elif player["health"] <= 0:
            return "game_over"

    elif choice == "3":
        return None  # Go back
    
    return None


def search_treasure():
    print("\nYou search the dark corners of the cave...")

    if not game_flags["cave_searched"]:
        # First time searching - guaranteed good loot
        print("\nYou found:")
        print(f"  - {GREEN}Health Potion{RESET}")
        print(f"  - {GREEN}Health Potion{RESET}")
        print(f"  - {YELLOW}20 gold{RESET}")

        add_to_inventory("Health Potion")
        add_to_inventory("Health Potion")
        player["gold"] += 20
        game_flags["cave_searched"] = True
    else:
        # Repeat visits - random smaller rewards
        # 70% chance to find something, 30% chance to find nothing
        find_chance = random.randint(1, 100)

        if find_chance <= 70:
            found_something = False
            print("\nYou scavenge through the cave again...")

            # Random gold (50% chance, 1-10 gold)
            if random.randint(1, 100) <= 50:
                gold_found = random.randint(1, 10)
                player["gold"] += gold_found
                print(f"  - {YELLOW}{gold_found} gold{RESET}")
                found_something = True

            # Random Health Potion (20% chance)
            if random.randint(1, 100) <= 20:
                add_to_inventory("Health Potion")
                found_something = True

            if not found_something:
                # Fallback - at least give a few gold
                gold_found = random.randint(1, 5)
                player["gold"] += gold_found
                print(f"  - {YELLOW}{gold_found} gold{RESET}")
        else:
            print(
                f"\n{DIM}You search carefully but find nothing useful this time.{RESET}")

    pause()


def dark_cave():
    while True:
        print("\n" + "=" * 40)
        print(f"  {BOLD}{CYAN}DARK CAVE{RESET}")
        print("=" * 40)
        print("\nYou enter a dark, damp cave.")
        print("The air is cold and you hear water dripping in the distance.")

        display_status()

        print("\nWhat do you want to do?")
        print("1. Explore Deeper")
        print("2. Search for Treasure")
        print("3. Return to Clearing")

        choice = get_valid_input("\nChoice: ", ["1", "2", "3"])

        if choice == "1":
            result = bear_encounter()
            if result == "game_over":
                return "game_over"
        elif choice == "2":
            search_treasure()
        elif choice == "3":
            return "clearing"


# LOCATION: WITCH'S HUT

def talk_to_witch():
    print(f'\n{PURPLE}Witch: "I sense you seek adventure..."{RESET}')
    print(f'{PURPLE}Witch: "But are you strong enough to defeat me?"{RESET}')
    print(f'{PURPLE}Witch: "I think not! Hehehehe..."{RESET}')
    print("\n1. Continue talking")
    print("2. Back")

    choice = get_valid_input("\nChoice: ", ["1", "2"])

    if choice == "1":
        print(f'\n{PURPLE}Witch: "You amuse me, mortal..."{RESET}')
        print(f'{PURPLE}Witch: "Perhaps I shall let you live... for now."{RESET}')
        print(f'{PURPLE}Witch: "But if you seek to challenge me, bring something to break my shield!"{RESET}')
        pause()


def witch_hut():
    if game_flags["witch_defeated"]:
        print("\nThe witch's hut stands empty, a reminder of your victory.")
        print("There is nothing more for you here.")
        pause()
        return "clearing"

    while True:
        print("\n" + "=" * 40)
        print(f"  {BOLD}{PURPLE}WITCH'S HUT{RESET}")
        print("=" * 40)
        print("\nYou approach a crooked hut with purple smoke rising from the chimney.")
        print("You sense powerful magic emanating from within.")
        print(
            f"\nAn old witch stands before you, eyes glowing with {PURPLE}power{RESET}.")
        print(f'\n{PURPLE}Witch: "What brings you to my home, traveler?"{RESET}')

        display_status()

        print("\nWhat do you do?")
        print("1. Talk to Witch")
        print(f"2. {RED}FIGHT THE WITCH (Final Boss!){RESET}")
        print("3. Leave")

        choice = get_valid_input("\nChoice: ", ["1", "2", "3"])

        if choice == "1":
            talk_to_witch()
        elif choice == "2":
            print(f'\n{PURPLE}Witch: "You DARE attack me?! Foolish mortal!"{RESET}')
            print(f'{PURPLE}Witch: "I\'ll teach you respect!"{RESET}')
            pause()

            # Witch combat with shield mechanic
            victory = combat("Witch", 100, 100, 15, 25,
                             {"gold": 100, "items": [
                                 "Magic Amulet", "Health Potion", "Health Potion"]},
                             has_shield=True, shield_reduction=10)

            if victory:
                game_flags["witch_defeated"] = True
                return good_ending()
            else:
                return "game_over"
        elif choice == "3":
            return "clearing"


# LOCATION: FOREST CLEARING

def forest_clearing():
    while True:
        print("\n" + "=" * 40)
        print(f"  {BOLD}{GREEN}FOREST CLEARING{RESET}")
        print("=" * 40)
        print("\nYou stand in a peaceful forest clearing.")
        print("Sunlight filters through the canopy above.")
        print("You see paths leading in three directions.")

        display_status()

        print("\nWhat do you want to do?")
        print("1. North - Dark Cave")
        print("2. West - Witch's Hut (Final Boss)")
        print("3. Rest (Restore 30 HP)")
        print("4. Check Inventory")
        print("5. Quit Game")

        choice = get_valid_input("\nChoice: ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            result = dark_cave()
            if result == "game_over":
                return "game_over"

        elif choice == "2":
            result = witch_hut()
            if result == "game_over":
                return "game_over"
            elif result == "victory":
                return "victory"

        elif choice == "3":
            heal_amount = min(30, player["max_health"] - player["health"])
            player["health"] += heal_amount
            print(f"\nYou rest under a tree...")
            print(f"{GREEN}Restored {heal_amount} HP!{RESET}")
            print(
                f"Health: {GREEN}{player['health']}/{player['max_health']}{RESET}")
            pause()

        elif choice == "4":
            check_inventory()

        elif choice == "5":
            print("\nThank you for playing!")
            return "quit"


# GAME ENDINGS

def game_over():
    print("\n" + "=" * 40)
    print(f"  {BOLD}{RED}GAME OVER{RESET}")
    print("=" * 40)
    print(f"\n{RED}You have been defeated...{RESET}")
    print("Your adventure ends here.")
    print(f"\n{YELLOW}Final Stats:{RESET}")
    print(f"  - Gold Earned: {YELLOW}{player['gold']}{RESET}")
    print(f"  - Enemies Defeated: {game_flags['enemies_defeated']}")

    print("\n1. Restart from Clearing")
    print("2. Quit Game")

    choice = get_valid_input("\nChoice: ", ["1", "2"])

    if choice == "1":
        # Reset health but keep inventory and gold
        player["health"] = player["max_health"]
        return "restart"
    else:
        print("\nThank you for playing!")
        return "quit"


def good_ending():
    print("\n" + "=" * 40)
    print(f"  {BOLD}{GREEN}VICTORY!{RESET}")
    print("=" * 40)
    print(f"\nThe witch falls to her knees, her magic fading...")
    print(f'{PURPLE}"Impossible... defeated by a mere mortal..."{RESET}')
    print("She vanishes in a puff of purple smoke.")
    print(f"\n{GREEN}The forest around you begins to change...{RESET}")
    print("The curse lifts, and sunlight breaks through the canopy.")
    print("Birds begin to sing again.")
    print(f"\n{BOLD}{GREEN}You have freed the forest from the witch's curse!{RESET}")
    print(f"{GREEN}You are hailed as a hero!{RESET}")

    print(f"\n{YELLOW}Final Stats:{RESET}")
    print(f"  - Total Gold: {YELLOW}{player['gold']}{RESET}")
    print(f"  - Enemies Defeated: {game_flags['enemies_defeated']}")
    print(f"  - Items Collected: {len(player['inventory'])}")

    print("\n" + "=" * 40)
    print(f"  {BOLD}{CYAN}THE END{RESET}")
    print("=" * 40)
    print("\nThank you for playing!")
    pause()
    return "victory"


# MAIN GAME INTRO

def show_intro():
    # Display game introduction.
    print()
    print(f"  {GREEN}███████╗ ██████╗ ██████╗ ███████╗███████╗████████╗{RESET}")
    print(f"  {GREEN}██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝{RESET}")
    print(f"  {GREEN}█████╗  ██║   ██║██████╔╝█████╗  ███████╗   ██║   {RESET}")
    print(f"  {GREEN}██╔══╝  ██║   ██║██╔══██╗██╔══╝  ╚════██║   ██║   {RESET}")
    print(f"  {GREEN}██║     ╚██████╔╝██║  ██║███████╗███████║   ██║   {RESET}")
    print(f"  {GREEN}╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   {RESET}")
    print()
    print(f"  {YELLOW} █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗{RESET}")
    print(f"  {YELLOW}██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝{RESET}")
    print(f"  {YELLOW}███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗  {RESET}")
    print(f"  {YELLOW}██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝  {RESET}")
    print(f"  {YELLOW}██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗{RESET}")
    print(f"  {YELLOW}╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝{RESET}")
    print()
    print("\nYou wake in a mysterious forest...")
    print("You have no memory of how you got here.")
    print(f"\n{YELLOW}Goal: Defeat the witch and escape!{RESET}")
    pause()


def reset_game():
    global player, game_flags

    player["health"] = 100
    player["max_health"] = 100
    player["gold"] = 20
    player["inventory"] = []
    player["location"] = "clearing"

    game_flags["bear_defeated"] = False
    game_flags["witch_defeated"] = False
    game_flags["cave_searched"] = False
    game_flags["enemies_defeated"] = 0


def main():
    reset_game()
    show_intro()

    while True:
        result = forest_clearing()

        if result == "quit":
            break
        elif result == "victory":
            break
        elif result == "game_over":
            go_result = game_over()
            if go_result == "quit":
                break
            elif go_result == "restart":
                continue


if __name__ == "__main__":
    main()