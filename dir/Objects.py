__author__ = 'Vinnent prestianni'
import os
import Items
import Minions
#
game_dir = os.path.dirname(__file__)
picture_dir = os.path.join(game_dir, "pictures")
map_dir = os.path.join(game_dir, "maps")


class GameObjects:
    def __init__(self, tmx_data):
        self.rewardKey = Items.bigDgKey()
        self.rewardDoor = bigDgDoor(self.rewardKey)
        self.boss = Minions.Ghost()
        self.bossSpawn = bossSpawn(self.boss)
        self.totalObjs = [bigDgKeyChest(self.rewardDoor),self.rewardDoor, bigDgRewardChest(), keySpot(self.rewardDoor),
                          bigDgChestOne(),bigDgChestTwo() , self.bossSpawn, bigDgEscape()]
        self.gameObjs = {} #this dict holds all objects on the map that are usable
        self.tmx_data = tmx_data

    def getInstance(self):
        return self

    def parseObjectString(self):
        for object in self.tmx_data:
            if "useable" in object.properties or "render" in object.properties:
                for x in self.totalObjs:
                    if x.string == object.properties["string"]:
                        self.gameObjs[object.properties["string"]] = x
                        print(x)


class bigDgKeyChest:
    def __init__(self, door):
        self.opened = False
        self.string = "bigDgKeyChest"
        self.loot = [door.key, Items.HpPot(2)]


    def use(self, player):
        tempTaken = []
        for item in self.loot:
            if player.addItem(item):
                tempTaken.append(item)
        if tempTaken == self.loot:
            self.loot = []
            self.opened = True
        else:
            self.loot = (item for item in self.loot if item not in tempTaken)



class bigDgRewardChest:
    def __init__(self):
        self.loot = [Items.HpPot(3), Items.HpPot(3), Items.LavaShield()]
        self.string = "bigDgRewardChest"
        self.opend = False
        self.goldValue = 500
        self.EXPValue = 2000
    def use(self, player):
        tempTaken = []
        for item in self.loot:
            if player.addItem(item):
                tempTaken.append(item)
        if tempTaken == self.loot:
            self.loot = []
            self.opened = True
        else:
            self.loot = (item for x in self.loot if item not in tempTaken)
        if self.opened:
            self.giveXpandGold(player)

    def giveXpandGold(self, player):
        player.gainGold(self.goldValue)
        player.gainEXP(self.EXPValue)

class bigDgChestOne(bigDgRewardChest):
    def __init__(self):
        bigDgRewardChest.__init__(self)
        self.loot = [Items.HpPot(2), Items.ManaPot(3)]
        self.string = "bigDgChestOne"
        self.goldValue = 43
        self.EXPValue = 0

class bigDgChestTwo(bigDgRewardChest):
        def __init__(self):
            bigDgRewardChest.__init__(self)
            self.loot = [Items.HpPot(2), Items.HpPot(3), Items.IronShield()]
            self.string = "bigDgChestTwo"
            self.goldValue = 76
            self.EXPValue = 0

class bossSpawn:
    def __init__(self, boss):
        self.string = "bossSpawn"
        self.boss = boss

    def use(self, player):
        player.battle(self.boss)



class bigDgDoor:
    def __init__(self, key):
        self.shut = True
        self.string = "bigDgDoor"
        self.key = key

    def use(self, player):
        if self.key in player.invo:
            self.shut = False
            print("door open")

class keySpot:
    def __init__(self, door):
        self.string = "keySpot"
        self.door = door

    def use(self, player):
        self.door.use(player)

class bigDgEscape:
    def __init__(self):
        self.string = "bigDgEscape"
        self.map = os.path.join(map_dir, "gamemap.tmx")
        self.changeFlag = False

    def use(self, player):
        self.changeFlag = True
        print("used")



