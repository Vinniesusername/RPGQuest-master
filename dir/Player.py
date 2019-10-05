__author__ = 'Vincent prestianni'

import os
import pygame
import random


game_dir = os.path.dirname(__file__)
picture_dir = os.path.join(game_dir, "pictures")


class Hero:
    def __init__(self):
        self.gold = 0
        self.hp = 30 # TODO: re check all numbers for balence.
        self.maxHp = 30
        self.maxMana = 0
        self.attack = 15
        self.mana = 0
        self. defence = 10
        self.attackEquiped = 0 #stats from swords
        self. defenceEquiped = 0 #stats from shields
        self.invo = [] # holds items
        self.exp = 0
        self.levelChart = [0, 52, 153, 532, 1765, 5402] #diffent exp needed for levels
        self.leveltrack = 0 # used to keep track of where you are in the chart. used in gainEXP function
        self.sword = None
        self.shield = None
        self.leech = False # special effect from blood sword
        self.burn = False # special effect from lava items
        self.battling = False
        self.godMode = False
        self.speed = 4

        ############ sprite stuff here ##################

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.right = pygame.image.load(os.path.join(picture_dir, "playerright.png")).convert()
        self.up = pygame.image.load(os.path.join(picture_dir, "playerup.png")).convert()
        self.down = pygame.image.load(os.path.join(picture_dir, "playerdown.png")).convert()
        self.left = pygame.image.load(os.path.join(picture_dir, "playerleft.png")).convert()
        self.state = 0 # keep track of direction moving
        # 0 = up 1 = down left = 2 right = 3

    def _printStats(self): # testing
        print(self.maxHp, self.attack, self.defence,  self.attackEquiped , self.defenceEquiped, self.exp, self.leveltrack + 1, self.maxMana)

    def fillHP(self):
        self.hp = self.maxHp
        self.mana = self.maxMana

    def printInvo(self):
        invoString = ""
        for item in self.invo:
            invoString = invoString + item.string + " "
        if invoString == "":
            invoString = "Empty"
        print(invoString)

    def hit(self, opp):  #takes in an object that extends BASIC
        damage = (self.attack + ( 0.8 * self.attackEquiped)) - (opp.defence + opp.defenceEquiped)
        opp.hp -= damage
        if self.leech:
            self.hp += damage * .04
            if self.hp > self.maxHp:
                self.hp = self.maxHp
        if opp.hp < 0:
            opp.death(self)

    def takeDamage(self, mininon):
        self.hp -= (mininon.attack - (self.defenceEquiped + self.defence *0.8) )
        if self.hp < 0:
            self.death()

    def battle(self, monster):
        while self.isAlive() and monster.isAlive():
            self.battling = True
            self.battleTurn(monster)
            print(self.hp)
            print(monster.hp)
            monster.battleTurn(self)
            print(self.hp)
            print(monster.hp)

    def battleTurn(self, monster):
        for event in pygame.event.get():
            if event == pygame.KEYDOWN:
                if event == pygame.K_a:
                    self.hit(monster)
                elif event == pygame.K_h:
                    for x in self.invo:
                        if x.string == "health pot":
                            x.use(self)

    def isAlive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def addItem(self, item):  # takes in an item object
        if item == None:
            return False
        if self.invo.__len__() < 20:
            self.invo.append(item)
        else:  # TODO: change print statement in to text prompt in pygame
            n = input("your backpack is full, would you like to discard an item in order to add " + item + "?")
            if n == "Y":
                d = input("what is the name of the item you wish to drop?")
                self.dropItem(d)
                self.addItem(item)
            else:
                return False
        return True

    def dropItem(self, item):  #this can be extended to remove x number of the same items in the same method.
        for x in self.invo:
            if x.id == item.id:
                self.invo.remove(item)

    def sellItem(self, item):
        self.gainGold(item.value)
        self.dropItem(item)

    def death(self): # TODO: add death graphics once pygame is figured out
        # TODO: create save state, and return to last last saved point
        # TODO: then remove some gold and/or items from player for death penaliy.
        pass

    def gainGold(self, amount):
        self.gold += amount

    def gainEXP(self, amount):
        self.exp += amount
        leveling = True
        try:
            while leveling:
                if self.exp > self.levelChart[self.leveltrack + 1]:
                    self.levelUP(self.leveltrack + 1)
                else:
                    leveling = False
        except IndexError:
            pass

    def levelUP(self, level):
        if level >= 3:
            self.maxMana += level * 2 + 8
        self.attack += random.randint(5, 7)
        self.defence += random.randint(5, 7)
        self.maxHp += random.randint(12, 18)
        self.leveltrack += 1
        self.fillHP()

    def drinkPot(self, pot):
        if pot in self.invo:
            pot.drink(self)
        else:
            raise Exception("trying to drink something hero doesnt have")

    def equipItem(self, item):
        if item in self.invo:
            item.equip()
        else:
            raise Exception("dont have the item")

    def unequipItem(self, item):
        item.unequip()

    def burnCheck(self):
        if self.sword == Items.LavaSword() or self.shield == Items.LavaShield():
            self.burn = True
        else:
            self.burn = False

    def getInstance(self):
        return Hero()
