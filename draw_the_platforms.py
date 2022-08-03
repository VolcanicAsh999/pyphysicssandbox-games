from pyphysicssandbox import *
import random
import time

pending=False
cord1=(-100,-100)
cord2=(-100,-100)

level=0

start_ball=[]
start_ball_moving=[]

lines_needed=0
lines_done=0

targets_needed=0
targets_done=0

timedelay=time.time()

ramps=[]

blink=[]

total_score=0

bounces=[]

color=[]

target=[]

colorkey=[[Color('green'),Color('blue')],[Color('red'),Color('orange')],[Color('black'),Color('gray')],[Color('light gray'),Color('yellow')],[Color('purple'),Color(255,0,255,0)]]

width=1000
height=600
window('Draw The Platforms!',width,height)

current_type='n'

hover_text=[None,None]

CANUSERIGHTPLATFORM = list(range(2, 21))
CANUSELEFTPLATFORM = list(range(5, 21))
CANUSEINVISIBLEPLATFORM = list(range(11, 21))
CANUSEBLUEPLATFORM = list(range(14, 21))
CANUSEORANGEPLATFORM = list(range(14, 21))
CANUSEGREYPLATFORM = list(range(16, 21))
CANUSEYELLOWPLATFORM = list(range(19, 21))
CANUSEPINKPLATFORM = list(range(19, 21))

class YouWonError(Exception):
    pass

def iseven(num):#utility func
    return (num/2==num//2)

def pcolor(ball,platform,p):
    try:
        if ball.color!=platform.color:
            return False
        return True
    except KeyError:
        ball.position=(ball.position[0],ball.position[1]+10)
        return True

def level_up(ball,target,pos):
    global targets_done,targets_needed,lines_done,lines_needed,timedelay,total_score,level
    if level<20:
        temp=targets_done
        for i in colorkey:
            if i[0]==target.color and i[1]==ball.color:
                targets_done+=1
                deactivate(ball)
                start_ball_moving.remove(ball)
        if temp==targets_done:
            return False
        if targets_done>=targets_needed:
            play_level()
            print("Level passed!")
            score1=(lines_needed-lines_done)*1000
            score2=round(time.time()-timedelay)*300
            total_score+=score1+score2
            print(f"Score: {score1+score2}")
    else:
        temp=targets_done
        for i in colorkey:
            if i[0]==target.color and i[1]==ball.color:
                targets_done+=1
                deactivate(ball)
                start_ball_moving.remove(ball)
        if temp==targets_done:
            return False
        if targets_done>=targets_needed:
            print("Level passed!")
            score1=(lines_needed-lines_done)*1000
            score2=round(time.time()-timedelay)*300
            total_score+=score1+score2
            print(f"Score: {score1+score2}")
            time.sleep(1)
            print("You Won!")
            print(f'Total Score: {total_score}')
            raise YouWonError('Your win was so awesome Python stopped working')
    return True

def create_line(cord1,cord2):
    return static_line(cord1,cord2,5)

def switch():
    for i in blink:
        if i.active:
            deactivate(i)
        else:
            reactivate(i)

def observer(keys):
    global pending,cord1,cord2,lines_done,lines_needed,current_type,level
    if pending and mouse_clicked() and lines_done<lines_needed:
        if cord1==(-100,-100):
            cord1=mouse_point()
        elif cord2==(-100,-100):
            cord2=mouse_point()
            if current_type=='n':
                line=create_line(cord1,cord2)
            elif current_type=='r':
                line=create_line(cord1,cord2)
                line.color=Color('brown')
                line.surface_velocity=(250,0)
            elif current_type=='l':
                line=create_line(cord1,cord2)
                line.color=Color('red')
                line.surface_velocity=(-250,0)
            elif current_type=='p1' or current_type=='p2':
                line=create_line(cord1,cord2)
                line.color=Color('pink')
                blink.append(line)
                ramps.append(line)
                if current_type=='p1':
                    deactivate(line)
            elif current_type=='b' or current_type=='o' or current_type=='g' or current_type=='y' or current_type=='p':
                line=create_line(cord1,cord2)
                if current_type=='b':
                    line.color=Color('blue')
                elif current_type=='g':
                    line.color=Color('grey')
                elif current_type=='y':
                    line.color=Color('yellow')
                elif current_type=='p':
                    line.color=Color(255,0,255,0)
                else:
                    line.color=Color('orange')
                color.append(line)
                ramps.append(line)
            ramps.append(line)
            cord1=(-100,-100)
            cord2=cord1
            lines_done+=1
            hover_text[1].text=f'Lines done: {lines_done}'
    else:
        for ball in start_ball_moving:
            pos=ball.position
            if pos[0]<0 or pos[0]>width or pos[1]<0 or pos[1]>height:
                level_failed()
        if constants.K_q in keys:
            level_failed()
    if constants.K_RETURN in keys and lines_done<=lines_needed:
        pending=False
        start_level()
    if constants.K_1 in keys:
        current_type='n'
    if constants.K_2 in keys and level in CANUSERIGHTPLATFORM:
        current_type='r'
    if constants.K_3 in keys and level in CANUSELEFTPLATFORM:
        current_type='l'
    if constants.K_4 in keys and level in CANUSEINVISIBLEPLATFORM:
        current_type='p1'
    if constants.K_5 in keys and level in CANUSEINVISIBLEPLATFORM:
        current_type='p2'
    if constants.K_6 in keys and level in CANUSEBLUEPLATFORM:
        current_type='b'
    if constants.K_7 in keys and level in CANUSEORANGEPLATFORM:
        current_type='o'
    if constants.K_8 in keys and level in CANUSEGREYPLATFORM:
        current_type='g'
    if constants.K_9 in keys and level in CANUSEYELLOWPLATFORM:
        current_type='y'
    if constants.K_0 in keys and level in CANUSEPINKPLATFORM:
        current_type='p'
    if constants.K_l in keys:
        level_failed(bypass=True)
    if constants.K_p in keys and not pending:
        if blink:
            switch()

def create_level(level):
    global pending,lines_done,lines_needed,width,height,targets_needed,targets_done
    targets_done=0
    lines_done=0
    for i in ramps:
        deactivate(i)
    ramps.clear()
    for i in start_ball_moving:
        deactivate(i)
    start_ball_moving.clear()
    for targe in target:
        deactivate(targe)
    target.clear()
    for bal in start_ball:
        deactivate(bal)
    start_ball.clear()
    blink.clear()
    color.clear()
    pending=True
    start_points=[]
    end_points=[]
    start_points2=[]
    end_points2=[]
    start_points3=[]
    end_points3=[]
    start_points4=[]
    end_points4=[]
    start_points5=[]
    end_points5=[]
    if level==1:
        start_points.append((50,50))
        end_points.append((width-50,height-50))
        lines_needed=2
        print("Normal Platforms selected by using [1]")
    elif level==2:
        start_points.append((50,height-50))
        end_points.append((width-50,height-50))
        lines_needed=1
        print("Right Platforms selected by using [2]")
    elif level==3:
        start_points.append((50,50))
        end_points.append((width-50,height-50))
        lines_needed=5
        ramps.append(static_box((width//2,0),5,height-60))
    elif level==4:
        start_points.append((50,50))
        end_points.append((width-50,height-50))
        ramps.append(static_box((width//2,0),5,height//2-50))
        ramps.append(static_box((width//2,height//2+50),5,height//2-50))
        lines_needed=3
    elif level==5:
        start_points.append((width-50,50))
        end_points.append((width-50,height-50))
        ramps.append(static_box((width//2,height//2),width//2,5))
        ramps.append(static_box((width//2,100),5,height-200))
        lines_needed=5
        print("Left Platforms selected by using [3]")
    elif level==6:
        start_points.append((50,50))
        end_points.append((50,height-50))
        ramps.append(static_box((0,height-100),100,5))
        ramps.append(static_box((0,height//2),width-50,5))
        lines_needed=3
    elif level==7:
        start_points.append((50,50))
        start_points.append((width-50,50))
        end_points.append((width//2,height-50))
        lines_needed=2
    elif level==8:
        start_points.append((50,50))
        start_points.append((50,height//2+20))
        start_points.append((width-50,height-50))
        end_points.append((50,height-50))
        ramps.append(static_box((0,height//2),width-50,5))
        ramps.append(static_box((0,height-100),100,5))
        lines_needed=5
    elif level==9:
        start_points.append((50,50))
        start_points.append((width-50,50))
        start_points.append((width//2,50))
        start_points.append((width//4,50))
        start_points.append(((width//4)+(width//2),50))
        end_points.append((width//2,height-50))
        ramps.append(static_box((width//2-50,height-100),100,5))
        line=static_line((30,height//2+50),(width//2+80,height-100),5)
        line.surface_velocity=((250,0))
        line.color=Color('brown')
        ramps.append(line)
        lines_needed=1
    elif level==10:
        j=1
        for i in range(18):
            start_points.append((50*j,50))
            j+=1
        end_points.append((width-50,height-50))
        lines_needed=4
    elif level==11:
        print("Blinking [start-off] Platforms selected by using [4]")
        print("Blinking [start-on] Platforms selected by using [5]")
        start_points.append((50,50))
        start_points2.append((width-50,50))
        end_points.append((width-50,height-50))
        end_points2.append((50,height-50))
        lines_needed=5
    elif level==12:
        j=1
        for i in range(18):
            if j<=9:
                start_points.append((50*j,50))
            else:
                start_points2.append((50*j,50))
            j+=1
        end_points.append((50,height-50))
        end_points2.append((width-50,height-50))
        lines_needed=4
    elif level==13:
        for i in range(18):
            for j in range(8):
                start_points.append((50*(i+1),50*(j+1)))
        end_points.append((width-50,height-50))
        lines_needed=6
    elif level==14:
        print("Blue Platforms selected by using [6]")
        print("Orange Platforms selected by using [7]")
        j=1
        for i in range(18):
            if iseven(j):
                start_points.append((50*j,50))
            else:
                start_points2.append((50*j,50))
            j+=1
        end_points.append((50,height-50))
        end_points2.append((width-50,height-50))
        lines_needed=6
    elif level==15:
        j=1
        for i in range(18):
            start_points.append((50*j,50))
            j+=1
        j=1
        for i in range(18):
            start_points2.append((50*j,100))
            j+=1
        end_points.append((50,height-50))
        end_points2.append((width-50,height-50))
        lines_needed=5
    elif level==16:
        print("Grey Platforms selected by using [8]")
        start_points.append((50,50))
        start_points2.append((width//2,50))
        start_points3.append((width-50,50))
        end_points.append((width//2,height-50))
        end_points2.append((width-50,height-50))
        end_points3.append((50,height-50))
        lines_needed=3
    elif level==17:
        j=1
        for i in range(18):
            start_points.append((50*j,50))
            j+=1
        j=1
        for i in range(18):
            start_points2.append((50*j,100))
            j+=1
        j=1
        for i in range(18):
            start_points3.append((50*j,150))
            j+=1
        end_points.append((width//4,height-50))
        end_points2.append((width//2,height-50))
        end_points3.append(((width//2)+(width//4),height-50))
        lines_needed=6
    elif level==18:
        start_points.append((50,50))
        start_points2.append((50,height//2+20))
        start_points3.append((width-50,height-70))
        end_points.append((50,height-50))
        end_points2.append((width-50,height-50))
        end_points3.append((5,height-50))
        ramps.append(static_box((0,height//2),width-50,5))
        ramps.append(static_box((0,height-100),100,5))
        lines_needed=5
    elif level==19:
        print('Yellow Platforms selected by using [9]')
        print('[Dark] Pink Platforms selected by using [0]')
        start_points.append((50,50))
        start_points2.append((width//4,50))
        start_points3.append((width//2,50))
        start_points4.append(((width//2)+(width//4),50))
        start_points5.append((width-50,50))
        points=[(50,height-50),(width//4,height-50),(width//2,height-50),((width//2)+(width//4),height-50),(width-50,height-50)]
        random.shuffle(points)
        end_points.append(points[0])
        end_points2.append(points[1])
        end_points3.append(points[2])
        end_points4.append(points[3])
        end_points5.append(points[4])
        lines_needed=5
    elif level==20:
        start_points.append((50,50))
        start_points2.append((width-50,50))
        start_points3.append((width-50,height-70))
        start_points4.append((50,height//2+70))
        start_points5.append((50,height//2+10))
        end_points.append((width//2,height//2+10))
        end_points2.append((50,height//2-25))
        end_points3.append((5,height-50))
        end_points4.append((width-50,height-50))
        end_points5.append((50,height-50))
        ramps.append(static_box((0,height//2),width-50,5))
        ramps.append(static_box((0,height-100),100,5))
        lines_needed=7
    else:
        return
    for pos in end_points:
        targe=static_box(pos,20,20)
        targe.color=Color('green')
        target.append(targe)
    for pos in end_points2:
        targe=static_box(pos,20,20)
        targe.color=Color('red')
        target.append(targe)
    for pos in end_points3:
        targe=static_box(pos,20,20)
        targe.color=Color('black')
        target.append(targe)
    for pos in end_points4:
        targe=static_box(pos,20,20)
        targe.color=Color('light gray')
        target.append(targe)
    for pos in end_points5:
        targe=static_box(pos,20,20)
        targe.color=Color('purple')
        target.append(targe)
    hover_text[0]=cosmetic_text_with_font((width-250,50),f'Lines Max: {lines_needed}','Comic Sans',36)
    hover_text[1]=cosmetic_text_with_font((width-250,100),f'Lines Done: 0','Comic Sans',36)
    targets_needed=len(start_points)+len(start_points2)+len(start_points3)+len(start_points4)+len(start_points5)
    for pos in start_points:
        bal=static_ball(pos,7)
        bal.color=Color('blue')
        start_ball.append(bal)
    for pos in start_points2:
        bal=static_ball(pos,7)
        bal.color=Color('orange')
        start_ball.append(bal)
    for pos in start_points3:
        bal=static_ball(pos,7)
        bal.color=Color('grey')
        start_ball.append(bal)
    for pos in start_points4:
        bal=static_ball(pos,7)
        bal.color=Color('yellow')
        start_ball.append(bal)
    for pos in start_points5:
        bal=static_ball(pos,7)
        bal.color=Color(255,0,255,0)
        start_ball.append(bal)
    extra_list=[]
    remove_list=[]
    for i in start_ball:
        if str(i) not in extra_list:
            extra_list.append(str(i))
        elif str(i) in extra_list:
            deactivate(i)
            remove_list.append(i)
    for i in remove_list:
        start_ball.remove(i)
    start_points.clear()
    start_points2.clear()
    start_points3.clear()
    start_points4.clear()
    start_points5.clear()
    end_points.clear()
    end_points2.clear()
    end_points3.clear()
    end_points4.clear()
    end_points5.clear()

def play_level():
    global level
    level+=1
    if level!=1:
        for i in hover_text:
            deactivate(i)
    create_level(level)

def level_failed(bypass=False):
    global level,targets_done,pending
    if bypass:
        pending=True
    targets_done=0
    if not bypass:
        level-=1
        print("Level failed! Retrying...")
    for bal in start_ball_moving:
        deactivate(bal)
    for targe in target:
        deactivate(targe)
    start_ball_moving.clear()
    target.clear()
    for bal in start_ball:
        deactivate(bal)
    start_ball.clear()
    play_level()

def start_level():
    global targets_needed,timedelay
    for bal in start_ball:
        pos=tuple(bal.position)
        deactivate(bal)
        bal2=ball(pos,7)
        bal2.color=bal.color
        for targe in target:
            add_collision(bal2,targe,level_up)
        for colo in color:
            add_collision(bal2,colo,pcolor)
        start_ball_moving.append(bal2)
    targets_needed=len(start_ball_moving)
    start_ball.clear()
    timedelay=time.time()

play_level()

add_observer(observer)

run()
