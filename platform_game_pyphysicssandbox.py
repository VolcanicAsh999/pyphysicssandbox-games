from pyphysicssandbox import *
import random
from itertools import cycle
window_width=1000
window_height=600
jump_speed=10000
wall_boost=5
move_speed=100
move_speed_count=0
double_jump=False
shield=False
lava_armor=False
landed=True
checked=True
direction=1
enemy_delay=0
platforms=[]
walls=[]
lava_pools=[]
unsolids=[]
boosters=[]
boosters_de=[]
enemies=[]
targets=[]
players=[]
hidden=[]
tohide=[]
keys=[]
green=[]
lblue=[]
tlist=[]
visible=[]
dlist=[]
dead=[]
complete_dead=[]
checkpoints=[]
trampolines=[]
grav_boost=[]
invisible=[]
flashkeys=[]
inv_lava=[]
searching=False
searching_color=None
wands=[]
key_boxes=[]
pairs=[]
trampoline_boost=2
death_point=(120,window_height-20)
on=True
num=0
default=False
level=1
gravity_direction=1
fdelay=0
boost_symbol='\x0c'
teleport_symbol=bounce_symbol=chr(664)
grav_symbol='^'
level_up_symbol1=won_symbol1=chr(171)
level_up_symbol2=won_symbol2=chr(187)
switch_symbol=chr(166)
checkpoint_symbol='\x0b'
key_symbol=flashkey_symbol=chr(172)
death_symbol=chr(685)
wand_symbol=chr(11064)
all_symbols=[boost_symbol,teleport_symbol,grav_symbol,switch_symbol,wand_symbol,checkpoint_symbol,key_symbol,death_symbol,flashkey_symbol]
def iseven(num):#utility func
    return (num/2==num//2)
def search(player,key,p):
    global searching,wand_symbol,searching_color
    searching=True
    print(wand_symbol+"Teleport available"+wand_symbol)
    deactivate(key)
    searching_color=key.color
    return True
def flash_invis(player,flashkey,p):
    global fdelay,flashkey_symbol
    deactivate(flashkey)
    fdelay=100
    for invis in invisible:
        invis.color=Color('light grey')
    print(flashkey_symbol+"Flashkey activated"+flashkey_symbol)
    return True
def won_game(player,target,p):
    global won_symbol1,won_symbol2
    colors=iter((Color('red'),Color('blue'),Color('green'),Color('yellow'),Color('orange')))
    colorcycle=cycle(colors)
    for i in range(random.randint(random.randint(0,5),random.randint(5,10))+random.randint(random.randint(0,5),random.randint(5,10))):
        message=text_with_font((100+random.randint(0,100),100+random.randint(0,100)),"You Won!","Comic Sans",36)
        message.color=next(colorcycle)
    for target1 in targets:
        deactivate(target1)
    add_collision(player,message,landing)
    print(won_symbol1+"You Won!"+won_symbol2)
    return False
def levelup(player,target,p):
    global level,level_up_symbol1,level_up_symbol2
    if level==10:
        won_game(player,target,p)
    else:
        level+=1
        for i in hidden+tohide:
            if not i.active:
                reactivate(i)
        player=load_level(level)
        print(level_up_symbol1+"Level up!"+level_up_symbol2)
    return False
def reverse_gravity(player,grav_booster,p):
    try:
        deactivate(grav_booster)
        global gravity_direction,grav_symbol
        gravity_direction*=-1
        gravity(0,500*gravity_direction)
        print(grav_symbol+"Gravity reversed"+grav_symbol)
    except AssertionError:
        pass
    return True
def teleport(player,other,p):
    global teleport_symbol
    for i in range(len(tlist)):
        if other==tlist[i]:
            player.position=tlist[i+1]
            print(teleport_symbol+"Teleport"+teleport_symbol)
            return True
    return False
def kill(player,d,p):
    for i in dlist:
        if i[0]==d:
            return False
    dlist.append((d,100))
    return True
def bounce(playe,trampoline,p):
    global landed,trampoline_boost,bounce_symbol,gravity_direction
    player=players[0]
    landed=False
    player.hit((jump_speed*direction,-50000*trampoline_boost*gravity_direction),player.position)
    print(bounce_symbol+"Boing"+bounce_symbol)
    return True
def update_special():
    global num,on,switch_symbol
    num+=1
    if num>=300 and on and visible:
        for i in visible:
            deactivate(i)
        on=False
        print(switch_symbol+"Switch off"+switch_symbol)
        num=0
    elif num>=50 and not on and visible:
        for i in visible:
            reactivate(i)
        on=True
        print(switch_symbol+"Switch on"+switch_symbol)
        num=0
    global mpdelay,mpon,reverse_symbol
    mpon=True
    if not mpon and (mpleft or mpup):
        mpdelay+=1
        if iseven(mpdelay):
            for i in mpleft:
                i.position=(i.position[0]+1,i.position[1])
                add_collision(players[0],i,landing)
            for i in mpup:
                i.position=(i.position[0],i.position[1]+1)
                add_collision(players[0],i,landing)
        if mpdelay>=200:
            mpdelay=200
            mpon=False
            print(reverse_symbol+"Reverse"+reverse_symbol)
            return
    elif not mpon and (mpleft or mpup):
        mpdelay-=1
        if iseven(mpdelay):
            for i in mpleft:
                i.position=(i.position[0]-1,i.position[1])
                add_collision(players[0],i,landing)
            for i in mpup:
                i.position=(i.position[0],i.position[1]-1)
                add_collision(players[0],i,landing)
        if mpdelay<=-200:
            mpdelay=-200
            mpon=True
            print(reverse_symbol+"Reverse"+reverse_symbol)
            return
    global fdelay,flashkey_symbol
    if fdelay>0:
        fdelay-=1
        if fdelay<=0:
            fdelay=0
            print(flashkey_symbol+"Flashkey off"+flashkey_symbol)
            for invis in invisible:
                invis.color=Color('white')
def observer(keys):
    global fdelay
    if visible or fdelay>0:#or mpleft or mpup:
        update_special()
    player=players[0]
    global landed,direction,double_jump,move_speed,move_speed_count,shield,lava_armor,gravity_direction,boost_symbol,searching,wand_symbol,searching_color
    if landed:
        if constants.K_SPACE in keys:# or mouse_clicked():
            landed=False
            player.hit((jump_speed*direction,(-50000*gravity_direction)),player.position)
        if constants.K_a in keys:
            direction=-1
            for platform in platforms:
                platform.surface_velocity=(move_speed*direction,0)
            if not landed:
                player.hit((jump_speed*wall_boost*direction,-50000),player.position)
        if constants.K_d in keys:
            direction=1
            for platform in platforms:
                platform.surface_velocity=(move_speed*direction,0)
            if not landed:
                player.hit((jump_speed*wall_boost*direction,-50000),player.position)
    else:
        if double_jump:
            if mouse_clicked() or constants.K_SPACE in keys:
                landed=False
                player.hit((jump_speed*direction,(-50000*gravity_direction)),player.position)
                double_jump=False
    if mouse_clicked() and searching:
        pos=mouse_point()
        sc=searching_color
        for i in key_boxes:
            if pos[0] in range(int(i.position[0]-15),int(i.position[0])+15) and pos[1] in range(int(i.position[1]-15),int(i.position[1])+15) and i.color==sc:
                player.position=(i.position[0],i.position[1])
                searching=False
                print(wand_symbol+"Teleport used"+wand_symbol)
                searching_color=None
                break
    if constants.K_RETURN in keys:
        if double_jump:
            print(boost_symbol+"Current Booster: Double Jump"+boost_symbol)
            print(boost_symbol+"Enables you to jump a second time when in air"+boost_symbol)
            print(boost_symbol+"Lasts until death or usage"+boost_symbol)
        if move_speed_count>0:
            print(boost_symbol+"Current Booster: x2 Move Speed"+boost_symbol)
            print(boost_symbol+"You move 2x as fast as normal"+boost_symbol)
            print(boost_symbol+"Lasts until death or 5 walls are hit"+boost_symbol)
        if shield:
            print(boost_symbol+"Current Booster: Enemy Shield"+boost_symbol)
            print(boost_symbol+"Will prevent 1 Enemy death [Enemies are blue]"+boost_symbol)
            print(boost_symbol+"Lasts until Lava death or usage"+boost_symbol)
        if lava_armor:
            print(boost_symbol+"Current Booster: Lava Armor"+boost_symbol)
            print(boost_symbol+"Will prevent 1 Lava Pool death [Lava Pools are red]"+boost_symbol)
            print(boost_symbol+"Lasts until Enemy death or usage"+boost_symbol)
    if constants.K_q in keys:
        double_jump=True
        return
        while True:
            i=input(">")
            if i=="double jump":
                double_jump=True
            elif i=="move boost":
                move_speed=200
                move_speed_count=5
                for platform in platforms:
                    platform.surface_velocity=(move_speed*direction,0)
            elif i=="shield":
                shield=True
            elif i=="armor":
                lava_armor=True
            elif i=="win":
                won_game(player,targets[0],(1,1))
            elif i=="kill":
                reset()
            elif i=="exit":
                break
            elif i=="level up":
                levelup(player,targets[0],(1,1))
            elif i=="all":
                shield=True
                lava_armor=True
                double_jump=True
                move_speed=200
                move_speed_count=5
                for platform in platforms:
                    platform.surface_velocity=(move_speed*direction,0)
            elif i=="use key":
                if keys:
                    keyuse(players[0],None,(1,1))
            elif i=="quit game":
                print("Quitting game...")
                import time
                time.sleep(1)
                print("Succesfully quit.")
                raise RuntimeError("You quit the game.")
    if constants.K_l in keys:
        levelup(player,targets[0],(1,1))
    if constants.K_j in keys and constants.K_d in keys:
        double_jump=True
        return
def landing(player,other,p):
    global landed
    landed=True
    return True
def reverse_direction(player,other,p):
    global direction,move_speed_count,move_speed,checked,gravity_direction
    direction*=-1
    for platform in platforms:
        platform.surface_velocity=(move_speed*direction,0)
    if not landed:
        player.hit((jump_speed*wall_boost*direction,(-50000*gravity_direction)),player.position)
    if move_speed_count>0:
        move_speed_count-=1
        checked=False
    if move_speed_count==0 and not checked:
        checked=True
        move_speed=100
    return True
def reset():
    global double_jump,move_speed,move_speed_count,shield,checked,death_point,death_symbol,gravity_direction,fdelay,searching
    searching=False
    double_jump=False
    move_speed=100
    move_speed_count=0
    checked=True
    shield=False
    fdelay=0
    for booster in boosters:
        if not booster.active:
            reactivate(booster)
    for key in keys:
        if not key.active:
            reactivate(key)
    for grav in grav_boost:
        if not grav.active:
            reactivate(grav)
    for dea in dlist:
        dlist.remove(dea)
    for disappear in complete_dead:
        if disappear not in dead:
            dead.append(disappear)
        if not disappear.active:
            reactivate(disappear)
    for flashkey in flashkeys:
        if not flashkey.active:
            reactivate(flashkey)
    for wand in wands:
        if not wand.active:
            reactivate(wand)
    for platform in platforms:
        platform.surface_velocity=(move_speed*direction,0)
    players[0].position=death_point
    gravity_direction=1
    gravity(0,gravity_direction*500)
    print(death_symbol+"You died!"+death_symbol)
def set_death_point(player,checkpoint,p):
    global death_point,checkpoint_symbol
    death_point=tuple(checkpoint.position)
    print(checkpoint_symbol+f"Checkpoint: {tuple(checkpoint.position)}"+checkpoint_symbol)
    deactivate(checkpoint)
    return True
def lava_death(player,other,p):
    global lava_armor,boost_symbol
    if not lava_armor:
        reset()
    else:
        lava_armor=False
        lava_pools.remove(other)
        deactivate(other)
        print(boost_symbol+"Lava Armor used"+boost_symbol)
    return True
def inv_lava_death(player,lava,p):
    global lava_armor
    lava_armor=False
    return lava_death(player,lava,p)
def enemy_death(player,other,p):
    global shield,boost_symbol
    if not shield:
        reset()
    else:
        shield=False
        enemies.remove(other)
        deactivate(other)
        print(boost_symbol+"Enemy Shield used"+boost_symbol)
    return True
def keyuse(player,key,p):
    global key_symbol
    print(key_symbol+"Key activated"+key_symbol)
    if key is not None:
        deactivate(key)
    for i in hidden+tohide:
        if i.active:
            deactivate(i)
        elif not i.active:
            reactivate(i)
    return True
def boost(player,other,p):
    global double_jump,move_speed,move_speed_count,shield,lava_armor,boost_symbol
    deactivate(other)
    r=random.randint(1,4)
    if r==1:
        double_jump=True
        print(boost_symbol+"Booster: Double Jump"+boost_symbol)
    elif r==2:
        move_speed=200
        move_speed_count=5
        for platform in platforms:
            platform.surface_velocity=(move_speed*direction,0)
        print(boost_symbol+"Booster: x2 Move Speed"+boost_symbol)
    elif r==3:
        shield=True
        print(boost_symbol+"Booster: Enemy Shield"+boost_symbol)
    elif r==4:
        lava_armor=True
        print(boost_symbol+"Booster: Lava Armor"+boost_symbol)
    return True
def load_level(level):
    global death_point,mpdelay,mpon
    if level!=1:
        mpdelay=-200
        mpon=True
        death_point=(120,window_height-20)
        for i in visible+checkpoints+grav_boost+flashkeys+wands:
            if not i.active:
                reactivate(i)
        for i in walls+platforms+boosters+enemies+unsolids+lava_pools+keys+hidden+tohide+green+lblue+visible+trampolines+checkpoints+grav_boost+invisible+inv_lava+flashkeys+wands+key_boxes:
            deactivate(i)
            if i in walls:
                walls.remove(i)
            elif i in platforms:
                platforms.remove(i)
            elif i in boosters:
                boosters.remove(i)
            elif i in enemies:
                enemies.remove(i)
            elif i in unsolids:
                unsolids.remove(i)
            elif i in lava_pools:
                lava_pools.remove(i)
            elif i in keys:
                keys.remove(i)
            if i in hidden:
                hidden.remove(i)
            if i in tohide:
                tohide.remove(i)
            elif i in green:
                green.remove(i)
            elif i in lblue:
                lblue.remove(i)
            elif i in visible:
                visible.remove(i)
            elif i in trampolines:
                trampolines.remove(i)
            elif i in checkpoints:
                checkpoints.remove(i)
            elif i in grav_boost:
                grav_boost.remove(i)
            elif i in invisible:
                invisible.remove(i)
            elif i in flashkeys:
                flashkeys.remove(i)
            elif i in inv_lava:
                inv_lava.remove(i)
            elif i in wands:
                wands.remove(i)
            elif i in key_boxes:
                key_boxes.remove(i)
        global searching
        searching=False
        for i in tlist:
            tlist.remove(i)
        for pair in pairs:
            pairs.remove(pair)
        for i in complete_dead:
            if i.active:
                deactivate(i)
            complete_dead.remove(i)
            if i in dead:
                dead.remove(i)
        for i in dlist:
            dlist.remove(i)
        for target in targets:
            deactivate(target)
            targets.remove(target)
        for player in players:
            deactivate(player)
            players.remove(player)
        for i in boosters_de+boosters:
            if i in boosters_de:
                boosters_de.remove(i)
            elif i in boosters:
                boosters.remove(i)
    global death_symbol
    if level==1:
        global boost_symbol,level_up_symbol1,level_up_symbol2
        print("Key:")
        print("Platforms: black")
        print("    You can jump on platforms - symbol: none")
        print("Enemies: blue")
        print("    Touching an Enemy will kill you - symbol: "+death_symbol)
        print("Boosters: yellow")
        print("    Boosters will give you a booster - symbol: "+boost_symbol)
        print("Lava: red")
        print("    Lava will kill you if you touch it - symbol: "+death_symbol)
        print("The goal: green")
        print("    You pass the level by touching the goal - symbol: "+level_up_symbol1+" and "+level_up_symbol2)
        floor=static_box((0,window_height),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        middle_wall=static_box((100,window_height-150),5,150)
        walls.append(middle_wall)
        wall=static_box((window_width-400,window_height-500),5,300)
        walls.append(wall)
        wall=static_box((window_width-450,window_height-450),5,300)
        walls.append(wall)
        wall=static_box((60,window_height-550),5,300)
        walls.append(wall)
        platform=static_box((window_width-100,window_height-50),100,5)
        platforms.append(platform)
        platform=static_box((window_width-100,window_height-50),100,5)
        platforms.append(platform)
        platform=static_box((window_width-250,window_height-100),100,5)
        platforms.append(platform)
        platform=static_box((window_width-500,window_height-150),200,5)
        platforms.append(platform)
        platform=static_box((window_width-600,window_height-500),100,5)
        platforms.append(platform)
        platform=static_box((window_width-500,window_height-590),150,5)
        platforms.append(platform)
        platform=static_box((100,window_height-150),100,5)
        platforms.append(platform)
        platform=static_box((5,window_height-200),45,5)
        platforms.append(platform)
        platform=static_box((60,window_height-550),100,5)
        platforms.append(platform)
        platform=static_box((0,0),100,5)
        platforms.append(platform)
        lava=static_box((5,window_height-5),95,5)
        lava_pools.append(lava)
        unsolid=cosmetic_box((window_width-800,window_height-300),100,5)
        unsolids.append(unsolid)
        unsolid=cosmetic_box((5,window_height-150),100,5)
        unsolids.append(unsolid)
        booster=static_box((window_width-50,window_height-10),10,10)
        boosters.append(booster)
        booster=static_box((20,window_height-210),10,10)
        boosters.append(booster)
        booster=static_box((window_width-450,0),10,10)
        boosters.append(booster)
        enemy=static_box((window_width-30,window_height-10),10,10)
        enemies.append(enemy)
        enemy=static_box((window_width-30,window_height-60),10,10)
        enemies.append(enemy)
        enemy=static_box((window_width-500,window_height-300),10,10)
        enemies.append(enemy)
        target=static_box((180,30),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==2:
        global key_symbol
        print("New Item: Key")
        print("Key: orange")
        print("    The key switches on and off orange platforms - symbol: "+key_symbol)
        floor=static_box((0,window_height),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        wall=static_box((150,window_height-50),5,50)
        walls.append(wall)
        wall=static_box((270,window_height-100),5,100)
        walls.append(wall)
        wall=static_box((245,window_height-170),5,100)
        walls.append(wall)
        wall=static_box((200,window_height-230),5,100)
        walls.append(wall)
        wall=static_box((550,window_height-450),5,200)
        walls.append(wall)
        wall=static_box((450,0),5,150)
        walls.append(wall)
        platform=static_box((0,window_height-30),60,5)
        platforms.append(platform)
        platform=static_box((140,window_height-70),110,5)
        platforms.append(platform)
        platform=static_box((260,window_height-200),90,5)
        platforms.append(platform)
        platform=static_box((450,window_height-450),100,5)
        platforms.append(platform)
        thide=static_box((window_width-50,window_height-50),5,50)
        tohide.append(thide)
        walls.append(thide)
        thide=static_box((window_width-50,window_height-55),50,5)
        tohide.append(thide)
        platforms.append(thide)
        thide=static_box((200,window_height-200),100,5)
        tohide.append(thide)
        platforms.append(thide)
        thide=static_box((775,window_height-50),100,5)
        tohide.append(thide)
        platforms.append(thide)
        key=static_box((170,window_height-150),10,10)
        keys.append(key)
        key=static_box((500,window_height-460),10,10)
        keys.append(key)
        key=static_box((window_width-30,window_height-70),10,10)
        keys.append(key)
        hide=static_box((window_width-90,window_height-30),5,30)
        hidden.append(hide)
        walls.append(hide)
        hide=static_box((window_width-90,window_height-35),35,5)
        hidden.append(hide)
        platforms.append(hide)
        hide=static_box((window_width-60,window_height-30),5,30)
        hidden.append(hide)
        walls.append(hide)
        hide=static_box((400,window_height-250),50,5)
        hidden.append(hide)
        platforms.append(hide)
        hide=static_box((500,window_height-200),100,5)
        hidden.append(hide)
        platforms.append(hide)
        hide=static_box((600,100),5,300)
        hidden.append(hide)
        walls.append(hide)
        booster=static_box((170,window_height-80),10,10)
        boosters.append(booster)
        booster=static_box((530,window_height-460),10,10)
        boosters.append(booster)
        enemy=static_box((window_width-80,window_height-20),10,10)
        enemies.append(enemy)
        lava=static_box((275,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((375,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((475,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((575,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((675,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((775,window_height-5),100,5)
        lava_pools.append(lava)
        target=static_box((window_width-30,window_height-30),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==3:
        global teleport_symbol
        print("New Item: Teleport boxes")
        print("Teleport boxes: blue/green")
        print("    When you touch a green box, teleport to the corresponding blue box - symbol: "+teleport_symbol)
        floor=static_box((0,window_height),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        platform=static_box((200,window_height-100),150,5)
        platforms.append(platform)
        platform=static_box((0,window_height-100),100,5)
        platforms.append(platform)
        platform=static_box((230,window_height-200),100,5)
        platforms.append(platform)
        platform=static_box((530,window_height-330),100,5)
        platforms.append(platform)
        platform=static_box((window_width-300,window_height-300),100,5)
        platforms.append(platform)
        platform=static_box((window_width-400,60),300,5)
        platforms.append(platform)
        platform=static_box((window_width-600,100),200,5)
        platforms.append(platform)
        hide=static_box((window_width-200,window_height-135),100,5)
        hidden.append(hide)
        platforms.append(hide)
        hide=static_box((window_width-500,150),400,5)
        hidden.append(hide)
        platforms.append(hide)
        thide=static_box((50,100),50,5)
        tohide.append(thide)
        platforms.append(thide)
        key=static_box((window_width-15,window_height-115),10,10)
        keys.append(key)
        key=static_box((window_width-600,90),10,10)
        keys.append(key)
        booster=static_box((window_width-350,window_height-170),10,10)
        boosters.append(booster)
        booster=static_box((window_width-300,140),10,10)
        boosters.append(booster)
        enemy=static_box((window_width-500,90),10,10)
        enemies.append(enemy)
        enemy=static_box((150,window_height-200),10,10)
        enemies.append(enemy)
        enemy=static_box((5,window_height-15),10,10)
        enemies.append(enemy)
        ramp=static_line((window_width-300,window_height-50),(window_width-500,window_height+5),5)
        platforms.append(ramp)
        ramp=static_line((window_width-5,window_height-100),(window_width-300,window_height-50),5)
        platforms.append(ramp)
        ramp=static_line((window_width-200,window_height-130),(window_width-500,window_height-180),5)
        platforms.append(ramp)
        ramp=static_line((50,window_height-150),(200,window_height-200),5)
        platforms.append(ramp)
        ramp=static_line((330,window_height-200),(530,window_height-330),5)
        platforms.append(ramp)
        ramp=static_line((window_width-150,window_height-300),(window_width-5,window_height-400),5)
        platforms.append(ramp)
        gree=static_box((window_width-120,40),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((50,50),20,20)
        lblue.append(blue)
        tlist.append((60,60))
        target=static_box((100,60),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==4:
        global switch_symbol
        print("New Item: Blink boxes")
        print("Blink boxes: pink")
        print("    Blink boxes have timed delays for turning on and off - symbol: "+switch_symbol)
        floor=static_box((0,window_height),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        visibl=static_box((0,window_height-50),400,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((600,window_height-300),5,180)
        visible.append(visibl)
        walls.append(visibl)
        visibl=static_box((700,window_height-320),5,180)
        visible.append(visibl)
        walls.append(visibl)
        visibl=static_box((800,window_height-340),5,180)
        visible.append(visibl)
        walls.append(visibl)
        visibl=static_box((900,window_height-360),5,180)
        visible.append(visibl)
        walls.append(visibl)
        platform=static_box((500,window_height-360),400,5)
        platforms.append(platform)
        platform=static_box((200,window_height-100),300,5)
        platforms.append(platform)
        ramp=static_line((500,window_height-100),(window_width,window_height-200),5)
        platforms.append(ramp)
        ramp=static_line((0,window_height-390),(50,window_height-380),5)
        platforms.append(ramp)
        visibl=static_box((300,window_height-360),150,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((100,window_height-380),150,5)
        visible.append(visibl)
        platforms.append(visibl)
        booster=static_box((300,window_height-110),10,10)
        boosters.append(booster)
        booster=static_box((650,window_height-260),10,10)
        boosters.append(booster)
        enemy=static_box((10,window_height-60),10,10)
        enemies.append(enemy)
        target=static_box((100,60),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==5:
        global checkpoint_symbol
        print("New Item: Checkpoint")
        print("Checkpoint: brown")
        print("    Checkpoints will reset where you go when you die - symbol: "+checkpoint_symbol)
        floor=static_box((0,window_height),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        wall=static_box((140,window_height-400),5,400)
        walls.append(wall)
        visibl=static_box((60,window_height-100),80,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((0,window_height-180),80,5)
        platforms.append(visibl)
        visible.append(visibl)
        visibl=static_box((60,window_height-260),80,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-200,window_height-40),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-350,window_height-70),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-500,window_height-100),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((200,window_height-160),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((140,window_height-200),40,5)
        visible.append(visibl)
        platforms.append(visibl)
        vramp=static_line((290,window_height-295),(490,window_height-330),5)
        visible.append(vramp)
        platforms.append(vramp)
        vramp=static_line((500,window_height-300),(window_width-200,window_height-400),5)
        visible.append(vramp)
        platforms.append(vramp)
        vramp=static_line((window_width-180,window_height-430),(window_width-580,window_height-550),5)
        visible.append(vramp)
        platforms.append(vramp)
        platform=static_box((350,window_height-130),100,5)
        platforms.append(platform)
        platform=static_box((190,window_height-300),100,5)
        platforms.append(platform)
        platform=static_box((window_width-180,window_height-400),180,5)
        platforms.append(platform)
        platform=static_box((0,window_height-340),80,5)
        platforms.append(platform)
        lava=static_box((window_width-150,window_height-5),50,5)
        lava_pools.append(lava)
        lava=static_box((window_width-250,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-350,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-450,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((450,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((350,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((250,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((145,window_height-5),105,5)
        lava_pools.append(lava)
        enemy=static_box((350,window_height-140),10,10)
        enemies.append(enemy)
        enemy=static_box((window_width-380,window_height-500),10,10)
        enemies.append(enemy)
        enemy=static_box((window_width-350,window_height-80),10,10)
        enemies.append(enemy)
        booster=static_box((390,window_height-327),10,10)
        boosters.append(booster)
        booster=static_box((window_width-450,window_height-110),10,10)
        boosters.append(booster)
        gree=static_box((window_width-600,window_height-570),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((110,window_height-30),20,20)
        lblue.append(blue)
        tlist.append((120,window_height-20))
        death_point=(window_width-25,window_height-60)
        checkpoint=static_box((400,window_height-140),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((40,window_height-350),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-90,window_height-410),10,10)
        checkpoints.append(checkpoint)
        target=static_box((100,60),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==6:
        global bounce_symbol
        print("New Item: Trampolines")
        print("Trampolines: purple")
        print("    Trampolines will bounce you high in the air - symbol: "+bounce_symbol)
        floor=static_box((0,window_height-5),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        wall=static_box((130,window_height-50),5,50)
        walls.append(wall)
        t=static_box((100,window_height-5),20,5)
        trampolines.append(t)
        t=static_box((230,window_height-180),20,5)
        trampolines.append(t)
        t=static_box((220,window_height-20),20,5)
        trampolines.append(t)
        t=static_box((180,window_height-240),20,5)
        trampolines.append(t)
        visibl=static_box((window_width-300,window_height-150),120,5)
        visible.append(visibl)
        platforms.append(visibl)
        platform=static_box((500,window_height-80),80,5)
        platforms.append(platform)
        visibl=static_box((window_width-400,window_height-115),80,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((250,window_height-30),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((100,window_height-240),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-100,window_height-430),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        platform=static_box((0,window_height-130),130,5)
        platforms.append(platform)
        platform=static_box((window_width-120,window_height-180),120,5)
        platforms.append(platform)
        platform=static_box((300,window_height-350),100,5)
        platforms.append(platform)
        platform=static_box((5,window_height-370),100,5)
        platforms.append(platform)
        ramp=static_line((500,window_height-370),(window_width-200,window_height-400),5)
        platforms.append(ramp)
        checkpoint=static_box((window_width-60,window_height-190),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((150,window_height-250),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((50,window_height-380),10,10)
        checkpoints.append(checkpoint)
        lava=static_box((window_width-100,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-200,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-300,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-400,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-500,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((400,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((300,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((200,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((120,window_height-5),80,5)
        lava_pools.append(lava)
        gree=static_box((window_width-50,20),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((5,window_height-400),20,20)
        lblue.append(blue)
        tlist.append((15,window_height-390))
        death_point=(7,death_point[1]-5)
        target=static_box((100,60),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==7:
        global grav_symbol
        print("New Item: Gravity reversers")
        print("Gravity reversers: dark grey")
        print("    Gravity will flip when you hit a Gravity reverser - symbol: "+grav_symbol)
        floor=static_box((0,window_height-5),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        ceiling=static_box((0,-10),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-20),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-30),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-40),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-50),window_width,10)
        lava_pools.append(ceiling)
        wall=static_box((400,window_height-100),5,50)
        walls.append(wall)
        platform=static_box((0,window_height-50),400,5)
        platforms.append(platform)
        platform=static_box((400,window_height-100),200,5)
        platforms.append(platform)
        platform=static_box((window_width-250,window_height-80),200,5)
        platforms.append(platform)
        platform=static_box((400,window_height-400),100,5)
        platforms.append(platform)
        platform=static_box((450,window_height-350),200,5)
        platforms.append(platform)
        grav=static_box((490,window_height-395),10,10)
        grav_boost.append(grav)
        grav=static_box((200,window_height-15),10,10)
        grav_boost.append(grav)
        grav=static_box((window_width-30,window_height-100),10,10)
        grav_boost.append(grav)
        grav=static_box((5,window_height-130),10,10)
        grav_boost.append(grav)
        t=static_box((window_width-320,window_height-100),20,5)
        trampolines.append(t)
        t=static_box((400,window_height-100),20,5)
        trampolines.append(t)
        visibl=static_box((0,window_height-120),150,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((0,window_height-200),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((150,window_height-160),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((250,window_height-440),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((100,window_height-480),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        lava=static_box((450,window_height-345),200,5)
        lava_pools.append(lava)
        lava=static_box((250,window_height-435),100,5)
        lava_pools.append(lava)
        lava=static_box((100,window_height-475),100,5)
        lava_pools.append(lava)
        lava=static_box((300,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((400,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((500,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-400,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-300,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-200,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((0,window_height-55),100,5)
        lava_pools.append(lava)
        lava=static_box((100,window_height-55),100,5)
        lava_pools.append(lava)
        lava=static_box((200,window_height-55),100,5)
        lava_pools.append(lava)
        lava=static_box((300,window_height-55),100,5)
        lava_pools.append(lava)
        checkpoint=static_box((window_width-450,window_height-360),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((500,window_height-110),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-150,window_height-90),10,10)
        checkpoints.append(checkpoint)
        target=static_box((100,60),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==8:
        print("New Item: Invisible platforms")
        print("Invisible platforms: ?")
        print("    Invisible platforms are, well, invisible - symbol: none")
        print("New Item: Flashkey")
        print("Flashkey: light grey")
        print("    Flashkeys will briefly flash the invisible platforms' locations - symbol: "+flashkey_symbol)
        floor=static_box((0,window_height-5),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        ceiling=static_box((0,-10),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-20),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-30),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-40),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-50),window_width,10)
        lava_pools.append(ceiling)
        invis=static_box((window_width-100,window_height-210),5,204)
        invisible.append(invis)
        walls.append(invis)
        invis=static_box((300,window_height-460),5,200)
        invisible.append(invis)
        walls.append(invis)
        invis=static_box((350,window_height-460),5,175)
        invisible.append(invis)
        walls.append(invis)
        invis=static_box((200,window_height-30),100,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((350,window_height-60),100,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((500,window_height-90),100,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((450,window_height-230),100,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((300,window_height-260),100,5)
        invisible.append(invis)
        platforms.append(invis)
        visibl=static_box((100,100),150,5)
        visible.append(visibl)
        platforms.append(visibl)
        platform=static_box((window_width-350,window_height-120),100,5)
        platforms.append(platform)
        platform=static_box((window_width-500,window_height-200),100,5)
        platforms.append(platform)
        lava=static_box((150,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((250,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((350,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((450,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-450,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-350,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-250,window_height-5),100,5)
        lava_pools.append(lava)
        checkpoint=static_box((window_width-300,window_height-130),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-450,window_height-210),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-40,window_height-170),10,10)
        checkpoints.append(checkpoint)
        grav=static_box((window_width-240,window_height-20),10,10)
        grav_boost.append(grav)
        grav=static_box((540,window_height-225),10,10)
        grav_boost.append(grav)
        flashkey=static_box((5,window_height-15),10,10)
        flashkeys.append(flashkey)
        flashkey=static_box((500,window_height-240),10,10)
        flashkeys.append(flashkey)
        gree=static_box((100,60),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((window_width-95,window_height-25),20,20)
        lblue.append(blue)
        tlist.append((window_width-85,window_height-25))
        visibl=static_box((window_width-100,window_height-40),60,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-60,window_height-80),55,5)
        visible.append(visibl)
        platforms.append(visibl)
        invis=static_box((window_width-100,window_height-120),60,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-60,window_height-160),55,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-100,window_height-200),60,5)
        invisible.append(invis)
        platforms.append(invis)
        flashkey=static_box((window_width-40,window_height-90),10,10)
        flashkeys.append(flashkey)
        target=static_box((window_width-130,window_height-250),20,20)
        target.color=Color("green")
        targets.append(target)
        death_point=(death_point[0]-70,death_point[1])
    elif level==9:
        global wand_symbol
        print("New Item: Invulnerable lava")
        print("Invulnerable lava: red")
        print("    Invulnerable lava is not affected by Lava Armor - symbol: "+death_symbol)
        print("New Item: Wands")
        print("Wands: matches color of Teleport box [special]")
        print("    Hit a wand, then click the corresponding Teleport box [special] to teleport there - symbol: "+wand_symbol)
        print("New Item: Teleport box [special]")
        print("Teleport box [special]: matches color of Wand")
        print("    When you're under the affect of a Wand, click the corresponding Teleport box [special] to teleport there - symbol: "+wand_symbol)
        floor=static_box((0,window_height-5),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        ceiling=static_box((0,-10),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-20),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-30),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-40),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-50),window_width,10)
        lava_pools.append(ceiling)
        invlava=static_box((300,window_height-5),700,5)
        inv_lava.append(invlava)
        invlava=static_box((5,200),655,5)
        inv_lava.append(invlava)
        invlava=static_box((300,window_height-340),700,5)
        inv_lava.append(invlava)
        wand=static_box((5,window_height-15),10,10)
        wands.append(wand)
        key_box=cosmetic_box((100,20),20,20)
        key_boxes.append(key_box)
        pairs.append((wand,key_box))
        wand=static_box((window_width-440,window_height-370),10,10)
        wands.append(wand)
        key_box=cosmetic_box((300,window_height-100),20,20)
        key_boxes.append(key_box)
        pairs.append((wand,key_box))
        visibl=static_box((5,120),200,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((250,180),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((400,140),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-340,5),5,200)
        visible.append(visibl)
        walls.append(visibl)
        visibl=static_box((300,window_height-80),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((450,window_height-110),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-250,window_height-180),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        platform=static_box((window_width-400,window_height-140),100,5)
        platforms.append(platform)
        platform=static_box((window_width-440,window_height-360),120,5)
        platforms.append(platform)
        platform=static_box((window_width-35,window_height-50),35,5)
        platforms.append(platform)
        platform=static_box((window_width-35,window_height-50),5,50)
        platforms.append(platform)
        gree=static_box((window_width-100,window_height-240),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((window_width-30,window_height-45),20,20)
        lblue.append(blue)
        tlist.append((window_width-20,window_height-25))
        invis=static_box((window_width-450,100),100,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-340,60),140,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-150,150),145,5)
        invisible.append(invis)
        platforms.append(invis)
        t=static_box((window_width-150,150),20,5)
        trampolines.append(t)
        checkpoint=static_box((window_width-350,window_height-150),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-250,50),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-380,window_height-370),10,10)
        checkpoints.append(checkpoint)
        target=static_box((window_width-25,window_height-25),20,20)
        target.color=Color("green")
        targets.append(target)
    elif level==10:
        print("New Item: none")
        print("It uses all items from previous levels, basically just a hard level though")
        print("    Good luck, you'll need it ;)")
        floor=static_box((0,window_height-5),window_width,50)
        platforms.append(floor)
        left_wall=static_box((0,0),5,window_height)
        walls.append(left_wall)
        right_wall=static_box((window_width-5,0),5,window_height)
        walls.append(right_wall)
        ceiling=static_box((0,-10),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-20),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-30),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-40),window_width,10)
        lava_pools.append(ceiling)
        ceiling=static_box((0,-50),window_width,10)
        lava_pools.append(ceiling)
        lava=static_box((5,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((105,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((205,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((305,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((405,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((505,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((605,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((705,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((805,window_height-270),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-300,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-200,window_height-5),100,5)
        lava_pools.append(lava)
        lava=static_box((window_width-100,window_height-5),100,5)
        lava_pools.append(lava)
        wall=static_box((40,window_height-200),5,190)
        walls.append(wall)
        wall=static_box((160,window_height-200),5,190)
        walls.append(wall)
        wall=static_box((400,window_height-200),5,190)
        walls.append(wall)
        wall=static_box((window_width-480,window_height-200),5,190)
        walls.append(wall)
        wall=static_box((window_width-320,window_height-200),5,160)
        walls.append(wall)
        wall=static_box((window_width-320,window_height-20),5,5)
        walls.append(wall)
        wall=static_box((window_width-200,100),5,200)
        walls.append(wall)
        wall=static_box((window_width-400,100),5,200)
        walls.append(wall)
        wall=static_box((480,100),5,200)
        walls.append(wall)
        wall=static_box((405,100),5,195)
        walls.append(wall)
        wall=static_box((200,100),5,200)
        walls.append(wall)
        platform=static_box((350,100),100,5)
        platforms.append(platform)
        platform=static_box((350,window_height-305),100,5)
        platforms.append(platform)
        platform=static_box((200,100),100,5)
        platforms.append(platform)
        platform=static_box((200,190),80,5)
        platforms.append(platform)
        platform=static_box((0,window_height-265),50,5)
        platforms.append(platform)
        platform=static_box((40,window_height-15),100,5)
        platforms.append(platform)
        platform=static_box((160,window_height-15),100,5)
        platforms.append(platform)
        platform=static_box((160,window_height-107),80,5)
        platforms.append(platform)
        platform=static_box((160,window_height-200),100,5)
        platforms.append(platform)
        platform=static_box((400,window_height-15),100,5)
        platforms.append(platform)
        platform=static_box((400,window_height-107),80,5)
        platforms.append(platform)
        platform=static_box((400,window_height-200),100,5)
        platforms.append(platform)
        platform=static_box((window_width-480,window_height-15),100,5)
        platforms.append(platform)
        platform=static_box((window_width-400,window_height-255),120,5)
        platforms.append(platform)
        platform=static_box((window_width-200,window_height-305),100,5)
        platforms.append(platform)
        platform=static_box((window_width-328,window_height-380),56,5)
        platforms.append(platform)
        platform=static_box((window_width-150,window_height-160),100,5)
        platforms.append(platform)
        hide=static_box((window_width-150,window_height-380),50,5)
        hidden.append(hide)
        platforms.append(hide)
        hide=static_box((window_width-150,110),50,5)
        hidden.append(hide)
        platforms.append(hide)
        invis=static_box((110,window_height-170),50,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_line((360,window_height-205),(400,window_height-200),5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-390,window_height-425),70,5)
        invisible.append(invis)
        platforms.append(invis)
        invis=static_box((window_width-290,window_height-465),50,5)
        invisible.append(invis)
        platforms.append(invis)
        enemy=static_box((window_width-335,window_height-435),10,10)
        enemies.append(enemy)
        booster=static_box((window_width-305,window_height-390),10,10)
        boosters.append(booster)
        visibl=static_box((50,80),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-300,window_height-20),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-150,window_height-60),100,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-50,window_height-200),50,5)
        visible.append(visibl)
        platforms.append(visibl)
        visibl=static_box((window_width-50,window_height-340),50,5)
        visible.append(visibl)
        platforms.append(visibl)
        key=static_box((window_width-15,window_height-350),10,10)
        keys.append(key)
        t=static_box((window_width-50,window_height-200),20,5)
        trampolines.append(t)
        wand=static_box((450,window_height-25),10,10)
        wands.append(wand)
        key_box=cosmetic_box((window_width-470,window_height-190),20,20)
        key_boxes.append(key_box)
        pairs.append((wand,key_box))
        grav=static_box((window_width-390,window_height-25),10,10)
        grav_boost.append(grav)
        grav=static_box((window_width-290,window_height-250),10,10)
        grav_boost.append(grav)
        checkpoint=static_box((400,90),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-130,100),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((210,window_height-210),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((450,window_height-117),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-100,window_height-70),10,10)
        checkpoints.append(checkpoint)
        checkpoint=static_box((window_width-100,window_height-170),10,10)
        checkpoints.append(checkpoint)
        ramp=static_line((300,window_height-200),(340,window_height-10),5)
        walls.append(ramp)
        ramp=static_line((340,window_height-10),(380,window_height-200),5)
        walls.append(ramp)
        unsolid=cosmetic_line((window_width-350,window_height-300),(window_width-300,100),5)
        unsolids.append(unsolid)
        ramp=static_line((window_width-300,100),(window_width-250,window_height-300),5)
        walls.append(ramp)
        ramp=static_line((480,100),(window_width-400,window_height-300),5)
        walls.append(ramp)
        gree=static_box((window_width-420,window_height-350),20,20)
        green.append(gree)
        tlist.append(gree)
        blue=cosmetic_box((430,80),20,20)
        lblue.append(blue)
        tlist.append((435,80))
        target=static_box((5,40),20,20)
        target.color=Color("green")
        targets.append(target)
        death_point=(5,window_height-25)
    global gravity_direction
    gravity_direction=1
    gravity(0,gravity_direction*500)
    player=box(death_point,15,15)
    player.elasticity=0.0
    players.append(player)
    if level==1:
        add_observer(observer)
    add_collision(player,target,levelup)
    for wall in walls:
        add_collision(player,wall,reverse_direction)
    for platform in platforms:
        platform.surface_velocity=(move_speed,0)
        add_collision(player,platform,landing)
    for lava_pool in lava_pools:
        add_collision(player,lava_pool,lava_death)
        lava_pool.color=Color("red")
    for booster in boosters:
        booster.color=Color("yellow")
        add_collision(player,booster,boost)
    for enemy in enemies:
        enemy.color=Color("blue")
        add_collision(player,enemy,enemy_death)
    for key in keys:
        key.color=Color("orange")
        add_collision(player,key,keyuse)
    for hide in hidden:
        hide.color=Color("orange")
        deactivate(hide)
    for thide in tohide:
        thide.color=Color("orange")
    for gree in green:
        gree.color=Color('light green')
        add_collision(player,gree,teleport)
    for blue in lblue:
        blue.color=Color('light blue')
    for visibl in visible:
        visibl.color=Color('pink')
    for disappear in dead:
        disappear.color=Color('grey')
        complete_dead.append(disappear)
        add_collision(player,disappear,kill)
    for checkpoint in checkpoints:
        checkpoint.color=Color('brown')
        add_collision(player,checkpoint,set_death_point)
    for trampoline in trampolines:
        trampoline.color=Color('purple')
        add_collision(player,trampoline,bounce)
    for grav_booster in grav_boost:
        grav_booster.color=Color('dark grey')
        add_collision(player,grav_booster,reverse_gravity)
    for invis in invisible:
        invis.color=Color('white')
    for flashkey in flashkeys:
        flashkey.color=Color('light grey')
        add_collision(players[0],flashkey,flash_invis)
    for invlava in inv_lava:
        invlava.color=Color('red')
        add_collision(player,invlava,inv_lava_death)
    for wand in wands:
        add_collision(player,wand,search)
    wandcolors=iter((Color(255,0,255,0),Color(0,255,255,128),Color(255,255,0,255)))
    wandscycle=cycle(wandcolors)
    for pair in pairs:
        current_color=next(wandscycle)
        for i in pair:
            i.color=current_color
    return player
i="n"#input("\x0bPlay default game?\x0b (y/n) > ")
if i.lower()=="y":
    print("\x0bPlaying default game.\x0b")
    for platform in platforms:
        deactivate(platform)
    for wall in walls:
        deactivate(wall)
    for lava_pool in lava_pools:
        deactivate(lava_pool)
    for booster in boosters:
        deactivate(booster)
    for enemy in enemies:
        deactivate(enemy)
    for unsolid in unsolids:
        deactivate(unsolid)
    platforms=[]
    walls=[]
    floor=static_box((0,window_height),window_width,50)
    platforms.append(floor)
    left_wall=static_box((0,0),5,window_height)
    walls.append(left_wall)
    right_wall=static_box((window_width-5,0),5,window_height)
    walls.append(right_wall)
    middle_wall=static_box((100,window_height-150),5,150)
    walls.append(middle_wall)
    wall=static_box((100,window_height-150),5,100)
    walls.append(wall)
    platform=static_box((0,window_height-30),30,5)
    platforms.append(platform)
    platform=static_box((140,window_height-70),110,5)
    platforms.append(platform)
    player=box((120,window_height-20),15,15)
    player.elasticity=0.0
    for wall in walls:
        reactivate(wall)
        add_collision(player,wall,reverse_direction)
    for platform in platforms:
        reactivate(wall)
        platform.surface_velocity=(move_speed,0)
        add_collision(player,platform,landing)
    enemies=[]
    boosters=[]
    lava_pools=[]
    target=static_box((window_width-350,window_height-140),20,20)
    target.color=Color("green")
    targets.append(target)
    window("Simple Platform game",window_width,window_height)
    add_collision(player,target,won_game)
    add_observer(observer)
    level=10000
elif i!="y" and i!="n":
    symbol=random.choice(all_symbols)
    print(symbol+"Unknown response. Playing advanced game."+symbol)
    window("Platform game",window_width,window_height)
elif i=="n":
    symbol=random.choice(all_symbols)
    print(symbol+"Playing advanced game."+symbol)
    window("Platform game",window_width,window_height)
player=load_level(level)

run()
