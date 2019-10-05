__author__ = 'Vincent prestianni'

#
class HpPot():
    def __init__(self, level):
        self.restore = level*10
        self.value = 32
        self.string = "Health Potion" + " " + str(level)
        self.id = 13
    def use(self, hero):
        hero.hp += self.restore
        if hero.hp > hero.maxHp:
            hero.hp = hero.maxHp
        self.destroy(hero)
    def destroy(self, hero):
        self.restore = 0
        hero.dropItem(self)

class ManaPot():
    def __init__(self, level):
        self.restore = level*10
        self.value = 54
        self.string = "Mana Potion" + " " + str(level)
        self.id = 12
    def use(self, hero):
        hero.hp += self.restore
        if hero.mana > hero.maxMana:
            hero.mana = hero.maxMana
        self.destroy(hero)
    def destroy(self, hero):
        self.restore = 0
        hero.dropItem(self)

class WoodenSword():
    def __init__(self):
        self.value = 100
        self.damage = 10
        self.id = 11

    def equip(self, hero):
        if hero.sword != None:
            hero.sword.unequip(hero)
        hero.attackEquiped += self.damage
        hero.sword = self

    def unequip(self, hero):
        hero.attackEquiped -= self.damage
        hero.sword = None

class WoodenShield():
    def __init__(self):
        self.value = 100
        self.armour = 10
        self.id = 10

    def equip(self, hero):
        if hero.shield != None:
            hero.sword.unequip(hero)
        hero.defenceEquiped += self.armour
        hero.shield = self

    def unequip(self, hero):
        hero.defenceEquiped -= self.armour
        hero.shield = None

class BloodSword():
    def __init__(self):
        self.value = 1567
        self.damage = 50
        self.id = 9

    def equip(self, hero):
        if hero.sword != None:
            hero.sword.unequip(hero)
        hero.attackEquiped += self.damage
        hero.sword = self
        hero.leech = True

    def unequip(self, hero):
        hero.attackEquiped -= self.damage
        hero.sword = None
        hero.leech = False

class IronSword(WoodenSword):
    def __init__(self):
        WoodenSword.__init__(self)
        self.value = 300
        self.damage = 17
        self.string = "Iron Sword"
        self.id = 8


class IronShield(WoodenShield):
    def __init__(self):
        WoodenShield.__init__(self)
        self.value = 300
        self.armour = 14
        self.id = 7
        self.string = "Iron Shield"


class GoldSword(WoodenSword):
    def __init__(self):
        WoodenSword.__init__(self)
        self.value = 1500
        self.damage = 32
        self.id = 6


class GoldShield(WoodenShield):
    def __init__(self):
        WoodenShield.__init__(self)
        self.value = 1500
        self.armour = 26
        self.id = 5

class DiamondSword(WoodenSword):
    def __init__(self):
        WoodenSword.__init__(self)
        self.value = 3000
        self.damage = 45
        self.id = 4


class DiamondShield(WoodenShield):
    def __init__(self):
        WoodenShield.__init__(self)
        self.value = 3000
        self.armour = 36
        self.id = 3

class LavaSword(WoodenSword):
    def __init__(self):
        WoodenSword.__init__(self)
        self.value = 300000
        self.damage = 65
        self.id = 2
    def equip(self, hero):
        if hero.sword != None:
            hero.sword.unequip(hero)
        hero.attackEquiped += self.damage
        hero.sword = self
        hero.burn = True

    def unequip(self, hero):
        hero.attackEquiped -= self.damage
        hero.sword = None
        hero.burnCheck()

class LavaShield(WoodenShield):
    def __init__(self):
        WoodenShield.__init__(self)
        self.value = 300000
        self.armour = 54
        self.string = "Lava Shield"
        self.id = 1

    def equip(self, hero):
        if hero.shield != None:
            hero.sword.unequip(hero)
        hero.defenceEquiped += self.armour
        hero.shield = self
        hero.burn = True

    def unequip(self, hero):
        hero.attackEquiped -= self.armour
        hero.sword = None
        hero.burnCheck()

class bigDgKey():
    def __init__(self):
        self.used = False
        self.string = "Rusty Key"
        self.id = 0

    def use(self, player, door):
        if door.string == "bigDgDoor":
            self.used = True
            player.dropItem(self)
