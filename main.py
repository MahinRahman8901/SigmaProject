import random
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.max_health = 100
        self.health = self.max_health
        self.attack = 15
        self.defense = 10
        self.experience = 0
        self.gold = 0
        self.inventory = {}

    def display_status(self):
        print(f"\n Name: Level {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Experience: {self.experience}/{self.level * 100}")
        print(f"Gold: {self.gold}")
        print("Inventory:", self.inventory)

    def level_up(self):
        if self.experience >= self.level * 100:
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.attack += 5
            self.defense += 3
            print(f"Congratulations! You leveled up to {self.level}.")

    def receive_quest_rewards(self, rewards):
        print("Quest completed! You receive the following rewards:")
        for item, amount in rewards.items():
            print(f"{item}: {amount}")
            if item in self.inventory:
                self.inventory[item] += amount
            else:
                self.inventory[item] = amount

class Enemy:
    def __init__(self, name, level, health, attack, defense, experience_reward, gold_reward):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.experience_reward = experience_reward
        self.gold_reward = gold_reward

    def display_status(self):
        print(f"\n{self.name} (Level {self.level})")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0


class Location:
    def __init__(self, name, description, enemies):
        self.name = name
        self.description = description
        self.enemies = enemies

    def __str__(self):
        return f"{self.name}: {self.description}"

class Quest:
    def __init__(self, name, description, rewards):
        self.name = name
        self.description = description
        self.rewards = rewards
        self.completed = False

    def __str__(self):
        return f"{self.name}: {self.description}"

class RPGGame:
    def __init__(self):
        self.player = None
        self.current_location = None
        self.locations = [
            Location("Village", "Your humble starting point.", []),
            Location("Forest", "A dense forest with hidden dangers.", [
                Enemy("Wolf", 5, 20, 10, 5, 30, 15),
                Enemy("Bandit", 7, 30, 15, 8, 40, 20)
            ]),
            Location("Cave", "A dark and mysterious cave.", [
                Enemy("Goblin", 8, 40, 20, 10, 50, 25),
                Enemy("Troll", 12, 60, 30, 15, 80, 40)
            ]),
            # Add more locations as needed
        ]
        self.quests = [
            Quest("Clear the Forest", "Defeat enemies in the forest.", {"Gold": 50, "Experience": 100}),
            Quest("Explore the Cave", "Delve into the mysterious cave.", {"Potion": 3, "Experience": 150}),
            # Add more quests as needed
        ]

    def start_game(self):
        print("Welcome to the Epic RPG Game!")
        player_name = input("Enter your character's name: ")
        self.player = Player(player_name)
        self.current_location = self.locations[0]
        self.menu()

    def menu(self):
        while True:
            print("\n1. Explore")
            print("2. Display Character Status")
            print("3. Inventory")
            print("4. Quests")
            print("5. Quit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.explore()
            elif choice == "2":
                self.player.display_status()
            elif choice == "3":
                self.display_inventory()
            elif choice == "4":
                self.display_quests()
            elif choice == "5":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Try again.")

    def explore(self):
        print(f"\nYou are in the {self.current_location.name}. {self.current_location.description}")

        # Randomly encounter enemies in the location
        if self.current_location.enemies:
            enemy = random.choice(self.current_location.enemies)
            print(f"You encounter a {enemy.name}!")
            self.battle(enemy)

        # Explore more or return to the main menu
        print("\n1. Move to a new location")
        print("2. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            self.change_location()
        elif choice == "2":
            return

    def change_location(self):
        print("\nAvailable Locations:")
        for i, location in enumerate(self.locations, 1):
            print(f"{i}. {location}")

        selection = int(input("Choose a new location: ")) - 1
        if 0 <= selection < len(self.locations):
            self.current_location = self.locations[selection]
            print(f"You move to the {self.current_location.name}.")
            self.explore()
        else:
            print("Invalid selection. Try again.")

    def battle(self, enemy):
        print(f"\nPrepare for battle! You encounter a {enemy.name}.")
        while self.player.health > 0 and enemy.health > 0:
            print("\n1. Attack")
            print("2. Use Item")
            print("3. Run Away")
            action = input("Choose an action: ")

            if action == "1":
                self.combat(enemy)
            elif action == "2":
                self.use_item()
            elif action == "3":
                print("You run away from the battle.")
                break
            else:
                print("Invalid choice. Try again.")

        if self.player.health <= 0:
            print("Game over. You have been defeated.")
        else:
            print(f"You defeated the {enemy.name}!")

            # Gain experience, gold, and check for level up
            self.player.experience += enemy.experience_reward
            self.player.gold += enemy.gold_reward
            self.player.level_up()

            # Check if there are completed quests in the current location
            self.check_completed_quests()

    def combat(self, enemy):
        # Player attacks enemy
        player_damage = max(0, self.player.attack - enemy.defense)
        enemy.take_damage(player_damage)
        print(f"You attack the {enemy.name} and deal {player_damage} damage.")
        enemy.display_status()

        # Check if the enemy is defeated
        if enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            self.player.receive_quest_rewards({
                "Gold": random.randint(10, 20),
                "Experience": random.randint(20, 30),
            })
            return

        # Enemy attacks player
        enemy_damage = max(0, enemy.attack - self.player.defense)
        self.player.health -= enemy_damage
        print(f"The {enemy.name} attacks you and deals {enemy_damage} damage.")
        self.player.display_status()

    def use_item(self):
        if not self.player.inventory:
            print("Your inventory is empty.")
            return

        print("Inventory:")
        for item, amount in self.player.inventory.items():
            print(f"{item}: {amount}")

        item_to_use = input("Enter the item you want to use: ")

        if item_to_use in self.player.inventory:
            # Use the item (in this example, just healing)
            healing_amount = 20
            self.player.health = min(self.player.max_health, self.player.health + healing_amount)
            print(f"You used {item_to_use} and healed for {healing_amount} health.")
            self.player.inventory[item_to_use] -= 1

            # Remove item if the quantity is zero
            if self.player.inventory[item_to_use] == 0:
                del self.player.inventory[item_to_use]
        else:
            print("Invalid item. Try again.")

    def display_inventory(self):
        print("\nInventory:")
        for item, amount in self.player.inventory.items():
            print(f"{item}: {amount}")

    def display_quests(self):
        print("\nCurrent Quests:")
        for i, quest in enumerate(self.quests, 1):
            status = "Completed" if quest.completed else "Incomplete"
            print(f"{i}. {quest} - {status}")

        choice = input("Enter the number of the quest for details (or press Enter to go back): ")
        if choice.isdigit() and 0 < int(choice) <= len(self.quests):
            self.display_quest_details(int(choice) - 1)

    def display_quest_details(self, quest_index):
        quest = self.quests[quest_index]
        print(f"\n{quest.name} Details:")
        print(quest.description)
        print("Rewards:")
        for item, amount in quest.rewards.items():
            print(f"{item}: {amount}")

        if not quest.completed:
            print("\n1. Accept Quest")
        print("2. Return to Quests")

        choice = input("Choose an option: ")
        if choice == "1" and not quest.completed:
            print(f"You accepted the quest: {quest.name}")
            self.check_completed_quests()
        elif choice == "2":
            return
        else:
            print("Invalid choice. Try again.")

    def check_completed_quests(self):
        for quest in self.quests:
            if not quest.completed and all(item in self.player.inventory and self.player.inventory[item] >= amount
                                           for item, amount in quest.rewards.items()):
                quest.completed = True
                print(f"Quest completed: {quest.name}")
                self.player.receive_quest_rewards(quest.rewards)

if __name__ == "__main__":
    game = RPGGame()
    game.start_game()
