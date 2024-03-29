import sys
import pygame
from Player import *
from Scene import *
from Settings import *
from PopUpBox import *
from Guide import *                       
from BgmPlayer import BgmPlayer
class GameManager:
    def __init__(self):
        #设置背景音乐播放器并播放初始背景音乐
        self.bgmPlayer=BgmPlayer()
        self.bgmPlayer.play()
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
        self.guideBoard=GuideBoard(self.window)
        #创建对话栏
        self.dialogBox=DialogBox(self.window)
        #创建购物栏
        self.shopBox=ShoppingBox(self.window)
        #初始游戏状态
        self.state=GameState.START_CG
        #初始化BOSS击杀数量
        self.killedBossNum=0
        self.isKilled=[False,False,False]
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
            self.scene=CityScene(self.window,self.isKilled)
        if GOTO==SceneType.WILD_GRASS:
            self.scene=WildGrassScene(self.window,self.killedBossNum)
        if GOTO==SceneType.WILD_WATER:
            self.scene=WildWaterScene(self.window,self.killedBossNum)
        if GOTO==SceneType.WILD_FIRE:
            self.scene=WildFireScene(self.window,self.killedBossNum)
        if GOTO==SceneType.BOSS_GRASS:
            self.scene=BossGrassScene(self.window,self.killedBossNum)
        if GOTO==SceneType.BOSS_WATER:
            self.scene=BossWaterScene(self.window,self.killedBossNum)
        if GOTO==SceneType.BOSS_FIRE:
            self.scene=BossFireScene(self.window,self.killedBossNum)     
        if GOTO==SceneType.GAME_OVER:
            self.scene=GameOverScene(self.window)  
        if GOTO==SceneType.GAME_CLEAR:
            self.scene=GameClearScene(self.window,self.get_time())  
        #将场景重置
        self.scene_reset()
    #重置场景的函数
    def scene_reset(self):
        self.player.reset_pos(self.state,self.scene.mapType)#主人公回到屏幕中央
        self.player.attacks.empty()#请空子弹
    #总更新函数
    def update(self):
        self.tick(30)
        #处理事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#退出
                pygame.QUIT()
                sys.exit()
            if event.type==GameEvent.GAME_CLEAR:
                self.state=GameState.GAME_CLEAR
                self.flush_scene(SceneType.GAME_CLEAR) 
            if event.type==GameEvent.EVENT_SWITCH_START_MENU:#进入主菜单
                self.state=GameState.MAIN_MENU
                self.flush_scene(SceneType.MENU) 
            if event.type==GameEvent.EVENT_SWITCH_CITY:#进入城市
                self.update_bgmplayer(SceneType.CITY)
                self.bgmPlayer.play()
                self.state=GameState.GAME_PLAY_CITY
                self.flush_scene(SceneType.CITY) 
                if self.killedBossNum==3:
                    pygame.event.post(pygame.event.Event(GameEvent.GAME_CLEAR))
            #进入野外
            if event.type==GameEvent.EVENT_SWITCH_WILD_GRASS:
                self.update_bgmplayer(SceneType.WILD_GRASS)
                self.state=GameState.GAME_PLAY_WILD_GRASS
                self.flush_scene(SceneType.WILD_GRASS) 
            if event.type==GameEvent.EVENT_SWITCH_WILD_WATER:
                self.update_bgmplayer(SceneType.WILD_WATER)
                self.state=GameState.GAME_PLAY_WILD_WATER
                self.flush_scene(SceneType.WILD_WATER) 
            if event.type==GameEvent.EVENT_SWITCH_WILD_FIRE:
                self.update_bgmplayer(SceneType.WILD_FIRE)
                self.state=GameState.GAME_PLAY_WILD_FIRE
                self.flush_scene(SceneType.WILD_FIRE) 
                
            #进入BOSS房
            if event.type==GameEvent.EVENT_SWITCH_BOSS_GRASS:
                self.update_bgmplayer(SceneType.BOSS_GRASS)
                self.state=GameState.GAME_PLAY_BOSS_GRASS
                self.flush_scene(SceneType.BOSS_GRASS) 
            if event.type==GameEvent.EVENT_SWITCH_BOSS_WATER:
                self.update_bgmplayer(SceneType.BOSS_WATER)
                self.state=GameState.GAME_PLAY_BOSS_WATER
                self.flush_scene(SceneType.BOSS_WATER) 
            if event.type==GameEvent.EVENT_SWITCH_BOSS_FIRE:
                self.update_bgmplayer(SceneType.BOSS_FIRE)
                self.state=GameState.GAME_PLAY_BOSS_FIRE
                self.flush_scene(SceneType.BOSS_FIRE) 
            #开始对话
            if event.type==GameEvent.EVENT_DIALOG:
                self.player.talking=True
                self.dialogBox.set_npc(self.player.collide.collidingObject["npc"])
                self.dialogBox.npc.talking=True
            #结束对话
            if event.type==GameEvent.EVENT_END_DIALOG:
                self.player.talking=False
                self.dialogBox.npc.talking=False
                if self.dialogBox.npc.name=="治疗师":
                    self.player.reset_hp()
                if self.dialogBox.npc.name=="宝箱":
                    self.player.attr_update(addMaxHp=self.dialogBox.npc.hp,
                                            addHp=self.dialogBox.npc.hp,
                                            addAttack=self.dialogBox.npc.attack,
                                            addDefence=self.dialogBox.npc.defence,
                                            addCoins=self.dialogBox.npc.money)
                    self.dialogBox.npc.kill()
            #开始购物
            if event.type==GameEvent.EVENT_SHOP:
                self.player.shopping=True
                self.shopBox.set_npc(self.player.collide.collidingObject["npc"],self.player)
                self.shopBox.npc.shopping=True
            #结束购物
            if event.type==GameEvent.EVENT_END_SHOP:
                self.player.shopping=False
                self.shopBox.npc.shopping=False
            if event.type==GameEvent.EVENT_GAME_OVER:
                self.state=GameState.GAME_OVER
                self.flush_scene(SceneType.GAME_OVER) 

        #更新背景音乐
        if self.state==GameState.START_CG:
            self.update_start_cg()
        if self.state==GameState.MAIN_MENU:
            self.update_main_menu()
        if self.state==GameState.GAME_PLAY_CITY:
            self.update_city()
        if self.state==GameState.GAME_PLAY_WILD_GRASS or self.state==GameState.GAME_PLAY_WILD_WATER or self.state==GameState.GAME_PLAY_WILD_FIRE:
            self.update_wild()
        if self.state==GameState.GAME_PLAY_BOSS_GRASS or self.state==GameState.GAME_PLAY_BOSS_WATER or self.state==GameState.GAME_PLAY_BOSS_FIRE:
            self.update_boss()
        if self.state==GameState.GAME_OVER:
            self.update_game_over()
        if self.state==GameState.GAME_CLEAR:
            self.update_game_clear()
    #更新CG
    def update_start_cg(self):
        keys=pygame.key.get_pressed()
        if  self.get_time()>BgmSettings.test or keys[pygame.K_q]:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_START_MENU))
    #更新背景音乐
    def update_bgmplayer(self,GOTO):
        self.bgmPlayer.stop()
        self.bgmPlayer.update(GOTO)
        self.bgmPlayer.play()
    #更新主菜单
    def update_main_menu(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:#按下任意键进入游戏
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_CITY))
    #更新城市
    def update_city(self):
        self.update_player()#更新主人公状态
        self.update_attack()#更新子弹状态
        self.update_npcs()#更新NPC状态
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
        self.update_npcs()#更新NPC状态
        self.update_monsters()
        self.update_guide()#更新提示板状态
        #处理碰撞
        self.manage_collide()
        #更新镜头
        self.scene.update_camera(self.player)
        self.update_dialogbox()

        
    #更新BOSS房
    def update_boss(self):
        self.update_player()#更新主人公状态
        self.update_attack()#更新子弹状态
        self.update_bosses()
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
    def update_npcs(self):
        for npc in self.scene.npcs.sprites():
            npc.update(self.scene.cameraX,self.scene.cameraY)
    def update_monsters(self):
        for monster in self.scene.monsters.sprites():
            monster.update()
    def update_bosses(self):
        if self.scene.boss:
            self.scene.boss.update(self.player.rect.x,self.player.rect.y,self.get_time())
        for attack in self.scene.boss.attacks:
            attack.update(self.get_time())
            
    #更新提示板
    def update_guide(self):
        self.guideBoard.update(self.get_time())
    def update_dialogbox(self):
        if self.dialogBox.open:
            self.dialogBox.update()
    def update_shopbox(self):
        if self.shopBox.state!=ShopType.CLOSE:
            self.shopBox.update()
    
    def update_game_over(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_CITY))
    def update_game_clear(self):
        if self.get_time()-self.scene.startTime>10:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
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
        if pygame.sprite.spritecollide(object,self.scene.bosses,False,pygame.sprite.collide_mask):
            object.collide.collidingWith["boss"]=True
            object.collide.collidingObject["boss"]=self.scene.boss
        else:
            object.collide.collidingWith["boss"]=False
            object.collide.collidingObject["boss"]=None
        if isinstance(object,Player):
            for boss in self.scene.bosses:
                if pygame.sprite.spritecollide(object,boss.attacks,False,pygame.sprite.collide_mask):
                    object.collide.collidingWith["bossAttack"]=True
                    for attack in boss.attacks:
                        if pygame.sprite.collide_rect(object,attack):
                            object.collide.collidingObject["bossAttack"]=attack
                    break
            else:
                object.collide.collidingWith["bossAttack"]=False
                object.collide.collidingObject["bossAttack"]=None
    #处理碰撞
    def manage_collide(self):
        self.update_collide(self.player)#更新主人公碰撞
        #处理主人公碰撞
        if self.player.collide.is_colliding():
            if self.player.collide.collidingWith["portal"]:#与传送门碰撞
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.WILD_GRASS:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_WILD_GRASS))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.WILD_WATER:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_WILD_WATER))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.WILD_FIRE:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_WILD_FIRE))                                   
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.CITY:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_CITY))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.BOSS_GRASS :
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_BOSS_GRASS))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.BOSS_WATER:
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_BOSS_WATER))
                if self.player.collide.collidingObject["portal"].GOTO==SceneType.BOSS_FIRE :
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_BOSS_FIRE))

            if self.player.collide.collidingWith["obstacle"]:#与障碍物碰撞
                self.player.rect=self.player.rect.move(-self.player.dx,-self.player.dy)

            if self.player.collide.collidingWith["npc"]:#与NPC碰撞
                if self.player.collide.collidingObject["npc"].can_talk() and not (self.player.talking or self.player.shopping):
                    if isinstance(self.player.collide.collidingObject["npc"],DialogNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))
                    if isinstance(self.player.collide.collidingObject["npc"],ShopNPC):
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))
        
            if self.player.collide.collidingWith["monster"]:#与怪物碰撞
                if self.player.can_collide():
                    self.player.attr_update(addHp=min(0,self.player.defence
                                            -self.player.collide.collidingObject["monster"].attack))
                    if self.player.hp<=0:
                        self.player.hp=1
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_GAME_OVER))
                    self.player.reset_collide_cd()
            if self.player.collide.collidingWith["boss"]:
                if self.player.can_collide():
                    self.player.attr_update(addHp=min(0,self.player.defence
                                            -self.player.collide.collidingObject["boss"].attack))
                    if self.player.hp<=0:
                        self.player.hp=1
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_GAME_OVER))
                    self.player.reset_collide_cd()
            if self.player.collide.collidingWith["bossAttack"]:
                if self.player.can_collide():
                    self.player.attr_update(addHp=min(0,self.player.defence
                                            -self.player.collide.collidingObject["bossAttack"].attack))
                    if self.player.hp<=0:
                        self.player.hp=1
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_GAME_OVER))
                    self.player.reset_collide_cd()
                    self.player.collide.collidingObject["bossAttack"].kill()
        #更新子弹碰撞
        for attack in self.player.attacks:
            self.update_collide(attack)
        #处理子弹碰撞
        for attack in self.player.attacks.sprites():
            #如果越过边界或发生碰撞就删除子弹
            if attack.collide.collidingWith["monster"]:
                monster=attack.collide.collidingObject["monster"]
                monster.hp-=max(0,self.player.attack-monster.defence)
                if monster.hp<=0:
                    self.player.attr_update(addCoins=monster.money)
                    monster.kill()
            if attack.collide.collidingWith["boss"]:
                boss=attack.collide.collidingObject["boss"]
                boss.hp-=max(0,self.player.attack-boss.defence)
                if boss.hp<=0:
                    self.player.attr_update(addCoins=boss.money)
                    self.killedBossNum+=1
                    self.isKilled[self.scene.bossIndex]=True
                    for portal in self.scene.portals:
                        portal.rect.x=boss.rect.x+100
                        portal.rect.y=boss.rect.y+100
                    boss.kill()
            if attack.over_range(self.scene.cameraX,self.scene.cameraY) or attack.collide.is_colliding():
                attack.kill()
        #处理怪物碰撞
        for monster in self.scene.monsters.sprites():
            if monster.check==False:
                self.scene.monsters.remove(monster)
                self.update_collide(monster)
                self.scene.monsters.add(monster)
                monster.check=True
        for monster in self.scene.monsters.sprites():
            monster.check=False
            monster.fix(self.scene.cameraX,self.scene.cameraY)

    #总渲染函数
    def render(self):
        if self.state==GameState.START_CG:
            self.render_start()
        if self.state==GameState.MAIN_MENU:
            self.render_main_menu()
        if self.state==GameState.GAME_PLAY_CITY:
            self.render_city()
        if self.state==GameState.GAME_PLAY_WILD_GRASS or self.state==GameState.GAME_PLAY_WILD_WATER or self.state==GameState.GAME_PLAY_WILD_FIRE:
            self.render_wild()
        if self.state==GameState.GAME_PLAY_BOSS_WATER or self.state==GameState.GAME_PLAY_BOSS_GRASS or self.state==GameState.GAME_PLAY_BOSS_FIRE:
            self.render_boss()
        if self.state==GameState.GAME_OVER:
            self.render_gameover()
        if self.state==GameState.GAME_CLEAR:
            self.render_gameclear()
  
    #渲染开场CG
    def render_start(self):
        self.scene.render(self.get_time())
    #渲染主菜单
    def render_main_menu(self):
        self.scene.render(self.get_time())
    #渲染城市
    def render_city(self):
        self.scene.render(self.player)#渲染场景
        self.render_guide()
        #如果正在对话,渲染对话栏
        if self.player.talking:
            self.render_dialogbox()
        if self.player.shopping:
            self.render_shopbox()
    #渲染野外
    def render_wild(self):
        self.scene.render(self.player)#渲染场景
        self.render_guide()#渲染提示
        if self.player.talking:
            self.render_dialogbox()
    #渲染BOSS房
    def render_boss(self):
        self.scene.render(self.player)#渲染场景
        self.render_guide()#渲染提示
    #渲染游戏结束
    def render_gameover(self):
        self.scene.render(self.get_time())
    def render_gameclear(self):
        self.scene.render(self.get_time())
    #渲染提示   
    def render_guide(self):
        self.guideBoard.draw()

    #渲染对话栏
    def render_dialogbox(self):
        self.dialogBox.draw()
    def render_shopbox(self):
        self.shopBox.draw()
        