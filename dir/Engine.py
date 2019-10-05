__author__ = 'Vincent prestianni'
import Minions
import os
import pygame
import pytmx
import Player
import Objects

#set up game dir
game_dir = os.path.dirname(__file__)
picture_dir = os.path.join(game_dir, "pictures")
map_dir = os.path.join(game_dir, "maps")
#center game on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("RPG Quest by Vincent Prestianni")
        self.clock = pygame.time.Clock()
        self.windowX = 600
        self.windowY = 600
        self.screen=pygame.display.set_mode([self.windowX,self.windowY])
        self.background = (os.path.join(map_dir, "bigdung.tmx"))
        self.tmx_data = pytmx.load_pygame(self.background)
        self.player = Player.Hero()
        self.Objects = Objects.GameObjects(self.tmx_data).getInstance()
        self.Objects.parseObjectString()
        self.playerPosX = 0
        self.playerPosY = 0
        self.render_tiles_to_screen(self.background)
        for object in self.tmx_data.objects:
            if "spawnPoint" in object.properties:
                self.playerPosX = object.x /2
                self.playerPosY = object.y  /2
        self.movePlayer("up")
        self.loop()

    def spawnMonster(self, danger):
        """
        TODO implment this feature
        hash danger level to array of possible monsters that spawn at that level
        randomly pick a monster from that array and call self.player.battle(mosnter)
        """
        pass

    def changeMap(self, map):
        #TODO: fix this
        self.background = map
        for object in self.tmx_data.objects:
            if "spawnPoint" in object.properties:
                self.movePlayer(self.player.state)
        self.render_tiles_to_screen(self.background)

    def getPlayer(self):
        return self.player

    def getObjects(self):
        return self.Objects

    def render_tiles_to_screen(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        if self.tmx_data.background_color:
            self.screen.fill(pygame.Color(self.tmx_data.background_color))
        for layer in self.tmx_data.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x , y, image in layer.tiles():
                        tileX = (x * self.tmx_data.tilewidth) - self.playerPosX
                        tileY = (y * self.tmx_data.tileheight) - self.playerPosY
                        self.screen.blit(image, (tileX,  tileY))
        self.movePlayer(self.player.state)

    def movePlayer(self, state):
        if not self.blocked():
            if state == 0:
                self.screen.blit(self.player.up, (self.playerPosX, self.playerPosY))
            elif state == 1:
                self.screen.blit(self.player.down,  (self.playerPosX, self.playerPosY))
            elif state == 2:
                self.screen.blit(self.player.left, (self.playerPosX, self.playerPosY))
            elif state == 3:
                self.screen.blit(self.player.right, (self.playerPosX, self.playerPosY))

    def blocked(self): #deals with collison of objects that cant be passed through.
        if self.player.godMode:
            return False
        for object in self.tmx_data.objects:
            if "blocked" in object.properties:
                if "door" in object.properties:
                    if not self.Objects.gameObjs[object.string].shut:
                        return False
                if self.checkRange(object):
                    if self.player.state == 0:
                        self.playerPosY += self.player.speed
                    elif self.player.state == 1:
                        self.playerPosY -= self.player.speed
                    elif self.player.state == 2:
                        self.playerPosX += self.player.speed
                    elif self.player.state == 3:
                        self.playerPosX -= self.player.speed
                    return True

    def onScreen(self, x, y):  # this can be used to control how much the player can see. commented out for now
            return True
        # not((x > self.camX or  y > self.camY) or (x < self.camX - self.visability) or y < self.camY - self.visability)

    def checkObjs(self, player): # deals with objects that are meant to trigger when a player is near them
        for object in self.tmx_data.objects:
            if "useable" in object.properties:
                if self.checkRange(object):
                    self.Objects.gameObjs[object.string].use(self.player)
                    if "mapChange" in object.properties:
                        if self.Objects.gameObjs[object.string].changeFlag:
                            self.changeMap(self.Objects.gameObjs[object.string].map)
                elif "door" in self.tmx_data.properties:
                    if self.checkRange(object):
                        if self.Objects.gameObjs[object.string].shut:
                            self.blocked()


    def checkRange(self, object):
        object.x /= 2
        object.y /= 2
        if self.playerPosX >= object.x and self.playerPosX <= object.x + 10 and self.playerPosY >= object.y \
                and self.playerPosY <= object.y + 10:
            return True
        else:
            return False

    def loop(self):
        running = True

        while running:
            self.render_tiles_to_screen(self.background)
            for k in pygame.event.get():
                if k.type == pygame.QUIT:
                    running = False
                if k.type == pygame.KEYDOWN:
                    if k.key == pygame.K_ESCAPE:
                        running = False
                        exit(0)
                    elif k.key == pygame.K_RIGHT:
                        self.playerPosX += self.player.speed
                        self.player.state = 3
                    elif k.key == pygame.K_LEFT:
                        self.playerPosX -= self.player.speed
                        self.player.state = 2
                    elif k.key == pygame.K_UP:
                        self.playerPosY -= self.player.speed
                        self.player.state = 0
                    elif k.key == pygame.K_DOWN:
                        self.playerPosY += self.player.speed
                        self.player.state = 1
                    elif k.key == pygame.K_i:
                        self.player.printInvo()
                    elif k.key == pygame.K_g:
                        self.player.godMode = not self.player.godMode
                        self.player.speed = 7
                        print("entered dev mode: no blocking, increased speed")
                    elif k.key == pygame.K_e:
                        self.checkObjs(self.player)
            pygame.display.flip()
            self.clock.tick(30)


Game().loop()
