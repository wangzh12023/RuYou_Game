import sys
import pygame
from Player import *
from Scene import *
from Settings import *
from PopUpBox import *
from Guide import *                       #Guideboard
from BgmPlayer import BgmPlayer
class GameManager:
    def __init__(self):
        #设置背景音乐播放器并播放初始背景音乐
        self.bgmplayer=BgmPlayer()
        self.bgmplayer.start.play()
        #创建窗口
        self.window=pygame.display.set_mode((WindowSettings.width,WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)
        #创建时钟
        self.clock=pygame.time.Clock()
        #设置初始场景
        self.scene=StartCG(self.window) 
        #创建主人公
        self.player=Player(WindowSettings.width//2,WindowSettings.height//2)  
        #创建提示板
        self.guideboard=Guideboard(self.window)
        #创建对话栏
        self.dialogbox=DialogBox(self.window)
        #创建购物栏
        self.shopbox=ShoppingBox(self.window)
        #初始游戏状态
        self.state=GameState.START_CG
    #设置帧率
    def tick(self, fps):
        self.clock.tick(fps)
    #返回当前游戏进行时间(s)
    def get_time(self):
        return pygame.time.get_ticks()/1000
    #场景切换
    def flush_scene(self, GOTO:SceneType):
        #根据场景切换信息更换场景
        if GOTO==SceneType.MENU:
            self.scene=StartMenu(self.window)
        if GOTO==SceneType.CITY:
            self.scene=CityScene(self.window)
        if GOTO==SceneType.WILD:
            self.scene=WildScene(self.window)
        if GOTO==SceneType.BOSS:
            self.scene=BossScene(self.window)
        #将场景重置
        self.scene_reset()
    #重置场景的函数
    def scene_reset(self):
        self.player.reset_pos(self.state)#主人公回到屏幕中央
        self.player.attacks.empty()#请空子弹
    #总更新函数
    def update(self):
        self.tick(30)
        #处理事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#退出
                pygame.QUIT()
                sys.exit()
            if event.type==GameEvent.EVENT_SWITCH_START_MENU:#进入主菜单
                self.state=GameState.MAIN_MENU
                self.flush_scene(SceneType.MENU) 
            if event.type==GameEvent.EVENT_SWITCH_CITY:#进入城市
                self.bgmplayer.boss.stop()
                self.bgmplayer.city.play(-1)
                self.state=GameState.GAME_PLAY_CITY
                self.flush_scene(SceneType.CITY) 
            if event.type==GameEvent.EVENT_SWITCH_WILD:#进入野外
                self.bgmplayer.city.stop()
                self.bgmplayer.boss.stop()
                self.bgmplayer.wild.play(-1)
                self.state=GameState.GAME_PLAY_WILD
                self.flush_scene(SceneType.WILD) 
            if event.type==GameEvent.EVENT_SWITCH_BOSS:#进入BOSS房
                self.bgmplayer.wild.stop()
                self.bgmplayer.boss.play(-1)
                self.state=GameState.GAME_PLAY_BOSS
                self.flush_scene(SceneType.BOSS) 
            if event.type==GameEvent.EVENT_DIALOG:#开始对话
                self.player.talking=True
                self.dialogbox.set_npc(self.player.collide.collidingObject["npc"])
                self.dialogbox.npc.talking=True
            if event.type==GameEvent.EVENT_END_DIALOG:#结束对话
                self.player.talking=False
                self.dialogbox.npc.talking=False
            if event.type==GameEvent.EVENT_SHOP:#开始购物
                self.player.shopping=True
                self.shopbox.set_npc(self.player.collide.collidingObject["npc"],self.player)
                self.shopbox.npc.shopping=True
            if event.type==GameEvent.EVENT_END_SHOP:#结束购物
                self.player.shopping=False
                self.shopbox.npc.shopping=False
        #更新背景音乐
        self.update_bgmplayer()
        if self.state==GameState.START_CG:
            self.update_start_cg()
        if self.state==GameState.MAIN_MENU:
            self.update_main_menu()
        if self.state==GameState.GAME_PLAY_CITY:
            self.update_city()
        if self.state==GameState.GAME_PLAY_WILD:
            self.update_wild()
        if self.state==GameState.GAME_PLAY_BOSS:
            self.update_boss()
    #更新CG
    def update_start_cg(self):
        keys=pygame.key.get_pressed()
        if  self.get_time()>BGMSettings.Test or keys[pygame.K_q]:#StartBGM_length=22
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_START_MENU))
    #更新背景音乐
    def update_bgmplayer(self):
        if self.state!=GameState.START_CG:
            self.bgmplayer.start.stop()
    #更新主菜单
    def update_main_menu(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:#按下任意键进入游戏
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_CITY))
    #更新城市
    def update_city(self):
        self.update_player()#更新主人公状态
        self.update_attack()#更新子弹状态
        self.update_NPCs()#更新NPC状态
        self.update_guide()#更新提示板状态
        #处理碰撞
        self.manage_collide()
        #更新镜头
        self.scene.update_camera(self.player)
        #更新对话栏
        self.update_dialogbox()
        #更新对话栏
        self.update_shopbox()
    #更新野外
    def update_wild(self):
        self.update_player()#更新主人公状态
        self.update_attack()#更新子弹状态
        self.update_NPCs()#更新NPC状态
        self.update_guide()#更新提示板状态
        #处理碰撞
        self.manage_collide()
        #更新镜头
        self.scene.update_camera(self.player)
    #更新BOSS房
    def update_boss(self):
        self.update_player()#更新主人公状态
        self.update_attack()#更新子弹状态
        self.update_NPCs()#更新NPC状态
        self.update_guide()#更新提示板状态
        #处理碰撞
        self.manage_collide()
        #更新镜头
        self.scene.update_camera(self.player)
    #更新主人公状态
    def update_player(self):
        self.player.update(self.get_time())
    #更新子弹状态
    def update_attack(self):
        for attack in self.player.attacks:
            attack.update()
    #更新NPC
    def update_NPCs(self):
        for npc in self.scene.npcs.sprites():
            npc.update(self.scene.cameraX,self.scene.cameraY)
    #更新提示板
    def update_guide(self):
        self.guideboard.update(self.get_time())
    def update_dialogbox(self):
        if self.dialogbox.open:
            self.dialogbox.update()
    def update_shopbox(self):
        if self.shopbox.state!="Close":
            self.shopbox.update()
    #更新给定对象（包括主人公和子弹）的碰撞
    def update_collide(self,object):
        # object -> Obstacles
        if pygame.sprite.spritecollide(object,self.scene.obstacles,False,pygame.sprite.collide_mask):
            object.collide.collidingWith["obstacle"]=True
            for obstacle in self.scene.obstacles.sprites():
                if pygame.sprite.collide_rect(object,obstacle):
                    object.collide.collidingObject["obstacle"].append(obstacle)
        else:
            object.collide.collidingWith["obstacle"]=False
            object.collide.collidingObject["obstacle"]=[]
        # object -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        if pygame.sprite.spritecollide(object,self.scene.npcs,False,pygame.sprite.collide_mask):
            object.collide.collidingWith["npc"]=True
            for npc in self.scene.npcs.sprites():
                if pygame.sprite.collide_rect(object,npc):
                    object.collide.collidingObject["npc"]=npc
                    break
        else:
            object.collide.collidingWith["npc"]=False
            object.collide.collidingObject["npc"]=None
        # object -> Monsters
        if pygame.sprite.spritecollide(object,self.scene.monsters,False,pygame.sprite.collide_mask):
            object.collide.collidingWith["monster"]=True
            for monster in self.scene.monsters.sprites():
                if pygame.sprite.collide_rect(object,monster):
                    object.collide.collidingObject["monster"]=monster
        else:
            object.collide.collidingWith["monster"]=False
            object.collide.collidingObject["monster"]=None
        # object -> Portals
        if pygame.sprite.spritecollide(object,self.scene.portals,False,pygame.sprite.collide_mask):
            object.collide.collidingWith["portal"]=True
            for portal in self.scene.portals.sprites():
                if pygame.sprite.collide_rect(object,portal):
                    object.collide.collidingObject["portal"]=portal
        else:
            object.collide.collidingWith["portal"]=False
            object.collide.collidingObject["portal"]=None
        # object -> Boss
        pass
    #处理碰撞
    def manage_collide(self):
        self.update_collide(self.player)#更新主人公碰撞
        #处理主人公碰撞
        if self.player.collide.is_colliding():
            if self.player.collide.collidingWith["portal"]:#与传送门碰撞
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.WILD:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_WILD))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.CITY:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_CITY))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.BOSS:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_BOSS))

            if self.player.collide.collidingWith["obstacle"]:#与障碍物碰撞
                self.player.rect=self.player.rect.move(-self.player.dx,-self.player.dy)
            if self.player.collide.collidingWith["npc"]:#与NPC碰撞
                if self.player.collide.collidingObject["npc"].can_talk() and not (self.player.talking or self.player.shopping):
                    if isinstance(self.player.collide.collidingObject["npc"],DialogNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))
                    if isinstance(self.player.collide.collidingObject["npc"],ShopNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))
            if self.player.collide.collidingWith["monster"]:#与怪物碰撞
                self.player.rect=self.player.rect.move(-self.player.dx,-self.player.dy)
        #更新子弹碰撞
        for attack in self.player.attacks:
            self.update_collide(attack)
        #处理子弹碰撞
        for attack in self.player.attacks:
            #如果越过边界或发生碰撞就删除子弹
            if attack.over_range(self.scene.cameraX,self.scene.cameraY) or attack.collide.is_colliding():
                attack.kill()
    #总渲染函数
    def render(self):
        if self.state==GameState.START_CG:
            self.render_start()
        if self.state==GameState.MAIN_MENU:
            self.render_main_menu()
        if self.state==GameState.GAME_PLAY_CITY:
            self.render_city()
        if self.state==GameState.GAME_PLAY_WILD:
            self.render_wild()
        if self.state==GameState.GAME_PLAY_BOSS:
            self.render_boss()
    #渲染开场CG
    def render_start(self):
        self.scene.render(self.get_time())
    #渲染主菜单
    def render_main_menu(self):
        self.scene.render(self.get_time())
    #渲染城市
    def render_city(self):
        self.scene.render(self.player)#渲染场景
        #self.render_guide()
        #如果正在对话,渲染对话栏
        if self.player.talking:
            self.render_dialogbox()
        if self.player.shopping:
            self.render_shopbox()
    #渲染野外
    def render_wild(self):
        self.scene.render(self.player)#渲染场景
        self.render_guide()#渲染提示
    #渲染BOSS房
    def render_boss(self):
        self.scene.render(self.player)#渲染场景
        self.render_guide()#渲染提示
    #渲染提示   
    def render_guide(self):
        self.guideboard.draw()
    #渲染对话栏
    def render_dialogbox(self):
        self.dialogbox.draw()
    def render_shopbox(self):
        self.shopbox.draw()