from game import Person, bcolors
from magic import spell
from inventory import items
import random

# creating black magic
fire = spell("Fire", 15, 600, "Black")
thunder = spell("Thunder", 25, 800, "Black")
blizzard = spell("Blizzard", 30, 900, "Black")
meteor = spell("Meteor", 40, 1200, "Black")
quake = spell("Quake", 30, 1040, "Black")

# creating white magic
cure = spell("Cure", 25, 620, "White")
cura = spell("Cura", 32, 1500, "White")
curaga = spell("Curaga", 50, 6000, "White")

#creating some item:
potion = items("Potion", "potion", "heals 50 HP", 50)
hipotion = items("Hi-Potion", "Potion", "heals 100 HP", 100)
superpotion = items("Super Potion", "potion", "heals 500 HP", 1000)
elixer = items("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = items("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
granade = items("Granade", "attack", "deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spell = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item":hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item":elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item":granade, "quantity": 5}]

# Instantiate People
player1 = Person("Gobu: ", 3200, 132, 300, 34, player_spells, player_items, quit)
player2 = Person("Puggu:", 4000, 188, 311, 34, player_spells, player_items, quit)
player3 = Person("Yogi: ", 3120, 174, 288, 34, player_spells, player_items, quit)

# instantiate Enemy
enemy1 = Person("Batli:     ", 1250, 130, 500, 250, enemy_spell, [], [])
enemy2 = Person("Supernova: ", 11200, 701, 525, 300, enemy_spell, [], [])
enemy3 = Person("Sakura:    ", 1200, 130, 500, 250, enemy_spell, [], [])

#creating list containers for future use
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
weapon = [potion, hipotion, superpotion, elixer, hielixer, granade]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=====================")

    print("\n\n")
    print("NAME                 HP                                MP")
    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("     Choose Action")
        index = int(choice) - 1

        while index >= 4:
            print(bcolors.FAIL + " You have Chosen wrong Action." + bcolors.ENDC)
            choice = input("     Choose Action")
            index = int(choice) - 1

        if index == 0:

            dmg = player.generate_damege()
            enemy = player.choose_target(enemies)

            while enemy >= len(enemies):
                print(bcolors.FAIL + "WRONG CHOICE" + bcolors.ENDC)
                enemy = player.choose_target(enemies)

            if enemy < len(enemies):
                player = enemies[enemy].take_damage(dmg)
                print("You Attack " + enemies[enemy].name.replace(" ", "") + "for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died")
                del enemies[enemy]

            if enemy2.get_hp() == 0:
                print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
                running = False
                exit()

            if enemy > len(enemies):
                enemy = player.choose_target(enemies)

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("     Choose Magic:")) - 1
            if magic_choice == -1:
                continue

            while magic_choice > len(player_spells) - 1:
                print(bcolors.FAIL + "WRONG CHOICE" + bcolors.ENDC)
                magic_choice = int(input("     Choose Magic:")) - 1

            if magic_choice < len(player_spells):
                spell = player.magic[magic_choice]

            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            player.heal(magic_dmg)

            if spell.type == "White":
                if player.hp == player.maxhp:
                    print(bcolors.OKBLUE + " Your health is full choose attack spells." + bcolors.ENDC)

                if player.hp < player.maxhp:
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "Black":

                enemy = player.choose_target(enemies)
                magic = len(enemies)

                while enemy >= magic:
                    print(bcolors.FAIL + "WRONG CHOICE" + bcolors.ENDC)
                    enemy = player.choose_target(enemies)

                if enemy < magic:
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to "
                          + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.replace(" ", "") + " has died")
                        del enemies[enemy]

                    if enemy2.get_hp() == 0:
                        print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
                        running = False
                        exit()
        elif index == 2:
            player.choose_item()
            item_choice = int(input("     Choose items: ")) - 1
            atom = len(weapon) - 1
            while item_choice > atom:
                print(bcolors.FAIL + "WRONG CHOICE" + bcolors.ENDC)
                item_choice = int(input("     Choose items: ")) - 1

            if item_choice == -1:
                continue

            if item_choice <= atom:
                items = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None Left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if items.type == "potion":
                player.heal(items.prop)
                print(bcolors.OKGREEN + "\n" + items.name + "heals for ", str(items.prop), "HP" + bcolors.ENDC)
            elif items.type == "elixer":

                if items.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n" + items.name + " fully restores everyone's HP/MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

            elif items.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(items.prop)

                print(bcolors.FAIL + "\n" + items.name + "deals", str(items.prop), "points of damage to   "
                      + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]

                if enemy2.get_hp() == 0:
                    print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
                    running = False
                    exit()

        elif index == 3:
            player.choose_endgame()
            choice_endgame = int(input("     Choose Action: "))
            if choice_endgame == 1:
                print(bcolors.FAIL + " YOU LOSE" + bcolors.ENDC)
                print(bcolors.FAIL + " You quit the game" + bcolors.ENDC)
                exit()
            elif choice_endgame >= 2:
                player.choose_action()
                choice = input("     Choose Action")
                index = int(choice) - 1
                continue

    #check if battle is over
    defi = enemy2
    play = len(players)
    defeated_players = 0
    if enemy2.get_hp() == 0:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False

    if play == 0:
        print(bcolors.FAIL + "You loose idiot now go home" + bcolors.ENDC)
        exit()

    print("\n")
    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, len(players))
        ch = enemy_choice
        #Enemy Choose attack
        if enemy_choice == 0:
            target = ch
            enemy_dmg = enemies[target].generate_damege()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + "for",  enemy_dmg)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + "has died")
                del players[target]

        elif enemy_choice == 1:

            spell = random.randrange(0, len(enemy_spell))
            player = random.randrange(0, len(players))

            if spell == fire or meteor:

                magic_dmg = meteor.generate_damage()
                players[player].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name + "Attack for Meteor for " + str(magic_dmg) + " damage to "
                      + players[player].name + bcolors.ENDC)

            elif spell == curaga:
                enemy.heal(curaga)
                magic_dmg = meteor.generate_damage()
                print(bcolors.OKBLUE + "Curaga heals for " + enemy.name + str(magic_dmg) + bcolors.ENDC)

            if players[player].get_hp() == 0:
                print(players[player].name.replace(" ", "") + "has died")
                del players[player]


            #print("Enemy chose", spell, "damage is", magic_dmg)



