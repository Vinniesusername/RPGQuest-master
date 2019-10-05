__author__ = 'Vincent prestianni'
import random
import Items


class Blob:
    def __init__(self):
        self.expGained = 12
        self.goldGained = 17
        self.hp = 12
        self.attack = 10
        self.defence = 1
        self.sprite = None
        self.defenceEquiped = 0
        self.attackEquiped = 0

    def hit(self, hero):
        hero.takeDamage(self)

    def death(self, hero):
        hero.gainEXP(self.expGained)
        hero.gainGold(self.goldGained)

    def battleTurn(self, player):
        self.hit(player)

    def getInstance(self):
        return Blob


class Ghost:  # ghost will be the class from which all minions inherit because of its drop feature that blob doesnt have
    def __init__(self):
        self.expGained = 43
        self.goldGained = 54
        self.hp = 43
        self.attack = 32
        self.defence = 3
        self.items = [Items.HpPot(1), Items.ManaPot(1), None]
        self.spirte = None
        self.defenceEquiped = 0
        self.attackEquiped = 0

    def hit(self, hero):
        hero.takeDamage(self)

    def death(self, hero):
        roll = random.randint(0, 3)
        hero.addItem(self.items[roll])
        hero.gainEXP(self.expGained)
        hero.gainGold(self.goldGained)

    def isAlive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def battleTurn(self, player):
        self.hit(player)

    def getInstance(self):
        return Ghost()


class ForestGolem(Ghost):
    def __init__(self):
        Ghost.__init__(self)
        self.items = [None, Items.HpPot(3), Items.GoldShield()]  # shield is rare
        self. expGained = 154
        self.goldGained = 132
        self.hp = 89
        self.attack = 35
        self.defence = 55

    def death(self, hero):
        roll = random.randint(0, 2)
        if roll == 2:
            newroll = random.randint(0, 12)
            if newroll != 10:
                roll = random.randint(0, 1)
        hero.addItem(self.items[roll])
        hero.gainEXP(self.expGained)
        hero.gainGold(self.goldGained)


class MoutainGolem(ForestGolem):  # only difference here will be their art
    def __init__(self):
        ForestGolem.__init__(self)


class LavaGolem(Ghost):  # end game def mob. strongest other than boss. drops rare shield
    def __init__(self):
        Ghost.__init__(self)
        self.items = [None, Items.HpPot(3), Items.LavaShield()] # only way to get lava shield
        self.expGained = 2300
        self.goldGained = 1200
        self.hp = 450
        self.attack = 120
        self.defence = 170

    def death(self, hero):
        roll = random.randint(0, 3)
        if roll == 3:
            newroll = random.randint(0, 100)
            if newroll != 72:
                roll = random.randint(0, 2)
        hero.addItem(self.items[roll])
        hero.gainEXP(self.expGained)
        hero.gainGold(self.goldGained)


class Demon(Ghost):  # low level mob that spawns in graveyard or dgs
    def __init__(self):
        Ghost.__init__(self)
        self.items = [Items.IronSword(), Items.HpPot(1), Items.ManaPot(1)]
        self.expGained = 108
        self.goldGained = 105
        self.hp = 45
        self.attack = 23
        self.defence = 0


class LavaDemon(Ghost): # end game offense mob #TODO: add burn effect for lava mobs? unsure of balence effects
        def __init__(self):
            Ghost.__init__(self)
            self.items = [Items.LavaSword(), Items.HpPot(3), Items.ManaPot(3)] #only way to get lava sword
            self.expGained = 2100
            self.goldGained = 1500
            self.hp = 250
            self.attack = 180
            self.defence = 90

        def death(self, hero):
            roll = random.randint(0, 2)
            if roll == 0:
                newroll = random.randint(0, 100)
                if newroll != 72:
                    roll = random.randint(1, 2)
            hero.addItem(self.items[roll])
            hero.gainEXP(self.expGained)
            hero.gainGold(self.goldGained)
