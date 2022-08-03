import random,time
from pyphysicssandbox import *

width=1000
height=600

window('Fruit Chop',width,height)

gravity(0,500)

velocity_key={}

shapes=[]

delay=70
fruit_delay=delay

trail=[]

all_shapes=[]

score=0
score_text=cosmetic_text_with_font((10,10),f'Score: {score}','Comic Sans',36)

lives=5
lives_text=cosmetic_text_with_font((width-310,10),f'Lives Remaining: {lives}','Comic Sans',36)

fruit_pool=['watermelon','watermelon','watermelon',
            'apple','apple',
            'orange',
            'bomb']
max_shape_amount=4

levels_unlocked=[1]

max_length=10

death_delay=0
death_text=cosmetic_text_with_font((width//2-100,height//2-10),'','Comic Sans',100)

def fruit_collide(fruit1,fruit2,pos):
    return False

def fruit_hit_bottom(fruit,bottom,pos):
    global score
    if fruit.color.__str__()!='(0, 0, 0, 255)':
        if score>=1:
            score-=1
            score_text.text=f'Score: {score}'
        deactivate(fruit)
        shapes.remove(fruit)
    else:
        score+=1
        deactivate(fruit)
        shapes.remove(fruit)
        score_text.text=f'Score: {score}'
    return False

def p_hit_bottom(p,bottom,pos):
    deactivate(p)
    all_shapes.remove(p)
    return False

def fruit_explode(fruit):
    for i in range(random.randint(2,5)):
        particle=ball((random.randint(int(fruit.position[0]-10),int(fruit.position[0]+10)),random.randint(int(fruit.position[1]-5),int(fruit.position[1]+5))),3)
        particle.color=fruit.color
        particle.hit((random.randint(-10000,10000),random.randint(-10000,10000)),particle.position)
        for i in all_shapes:
            add_collision(i,particle,fruit_collide)
        add_collision(particle,bottom,p_hit_bottom)
        all_shapes.append(particle)
    for i in range(2):
        if fruit.color.__str__()==Color('red').__str__():
            radius=7.5
        elif fruit.color.__str__()==Color('green').__str__():
            radius=10
        elif fruit.color.__str__()==Color('orange').__str__():
            radius=5
        else:
            radius=10
        half=ball((random.randint(int(fruit.position[0]-10),int(fruit.position[0]+10)),random.randint(int(fruit.position[1]-5),int(fruit.position[1]+5))),radius)
        half.color=fruit.color
        half.hit((random.randint(-20000,20000),random.randint(-20000,20000)),particle.position)
        for i in all_shapes:
            add_collision(i,half,fruit_collide)
        add_collision(half,bottom,p_hit_bottom)
        all_shapes.append(half)

def chop_fruit(chopper,fruit,pos):
    global score,lives,max_length,delay,max_shape_amount,width,height,death_delay
    if fruit.color.__str__()!='(0, 0, 0, 255)':
        score+=1
        deactivate(fruit)
        shapes.remove(fruit)
        all_shapes.remove(fruit)
        print('Fruit chopped!')
        score_text.text=f'Score: {score}'
        fruit_explode(fruit)
    else:
        lives-=1
        deactivate(fruit)
        shapes.remove(fruit)
        all_shapes.remove(fruit)
        print('You chopped a bomb!')
        lives_text.text=f'Lives Remaining: {lives}'
        if lives<=0:
            print('You lose!')
            lives=5
            score=0
            print('Replaying')
            score_text.text='Score: 0'
            lives_text.text='Lives Remaining: 5'
            max_length=10
            max_shape_amount=4
            delay=70
            levels_unlocked.clear()
            levels_unlocked.append(1)
            fruit_pool.clear()
            fruit_pool.extend(('watermelon','watermelon','watermelon',
                               'apple','apple',
                               'orange',
                               'bomb'))
            for shape in all_shapes:
                deactivate(shape)
            all_shapes.clear()
            death_text.text='You Lost!'
            death_delay=150
            for i in trail:
                deactivate(i)
            trail.clear()
    return False

def make_fruit():
    global width,height
    fruit=random.choice(fruit_pool)
    if fruit=='watermelon':
        shape=ball((random.randint(20,width-20),height-20),20)
        shape.color=Color('green')
    elif fruit=='apple':
        shape=ball((random.randint(20,width-20),height-20),15)
        shape.color=Color('red')
    elif fruit=='orange':
        shape=ball((random.randint(20,width-20),height-20),10)
        shape.color=Color('orange')
    elif fruit=='bomb':
        shape=ball((random.randint(20,width-20),height-20),15)
        shape.color=Color(0,0,0,255)
    if fruit=='apple' or fruit=='bomb':
        shape.hit((random.choice([random.randint(-100000,-90000),random.randint(90000,100000)]),random.randint(-500000,-350000)),shape.position)
    elif fruit=='watermelon':
        shape.hit((random.choice([random.randint(-120000,-110000),random.randint(110000,120000)]),random.randint(-900000,-700000)),shape.position)
    elif fruit=='orange':
        shape.hit((random.choice([random.randint(-80000,-70000),random.randint(70000,80000)]),random.randint(-300000,-150000)),shape.position)
    return shape

def make_fruits():
    global max_shape_amount
    for fruit in range(random.randint(1,max_shape_amount)):
        shape=make_fruit()
        for i in all_shapes:
            add_collision(shape,i,fruit_collide)
        shapes.append(shape)
        all_shapes.append(shape)
        add_collision(chopper,shape,chop_fruit)
        add_collision(shape,bottom,fruit_hit_bottom)

def observer(keys):
    global fruit_delay,delay,max_shape_amount,max_length,lives,death_delay
    fruit_delay-=1
    if fruit_delay<=0:
        fruit_delay=delay
        make_fruits()
    if death_delay>0:
        death_delay-=1
        if death_delay<=0:
            death_delay=0
            death_text.text=''
    nex=static_ball(tuple(chopper.position),5)
    nex.color=chopper.color
    chopper.position=mouse_point()
    if len(trail)>=max_length:
        deactivate(trail.pop(0))
    trail.append(nex)
    for shape in shapes:
        add_collision(nex,shape,chop_fruit)
    for shape in all_shapes:
        if shape not in shapes:
            add_collision(nex,shape,fruit_collide)
    if score>=30 and 2 not in levels_unlocked:
        print('Level up! Level 2 unlocked')
        print('New Delay: 1 second')
        delay=50
        levels_unlocked.append(2)
        max_length+=5
        lives=5
        lives_text.text=f'Lives Remaining: {lives}'
    if score>=60 and 3 not in levels_unlocked:
        print('Level up! Level 3 unlocked')
        print('New Maximum amount of fruits - 7')
        max_shape_amount=7
        levels_unlocked.append(3)
        max_length+=5
        lives=5
        lives_text.text=f'Lives Remaining: {lives}'
    if score>=90 and 4 not in levels_unlocked:
        print('Level up! Level 4 unlocked')
        print('New Shapes pool')
        fruit_pool=['watermelon','watermelon',
                    'apple','apple',
                    'orange','orange',
                    'bomb','bomb']
        max_length+=10
        lives=5
        lives_text.text=f'Lives Remaining: {lives}'
        levels_unlocked.append(4)
    if score>=120 and 5 not in levels_unlocked:
        print('Level up! Level 5 unlocked')
        print('New Delay: 0.75 seconds')
        print('New Maximum amount of fruits - 10')
        max_shape_amount=10
        delay=37
        levels_unlocked.append(5)
        max_length+=10
        lives=5
        lives_text.text=f'Lives Remaining: {lives}'
    if score>=150 and 6 not in levels_unlocked:
        print('Level up! Level 6 unlocked')
        print('New Delay: 0.5 seconds')
        print('New Maximum amount of fruits - 15')
        print('New Shapes pool')
        delay=25
        max_shape_amount=15
        max_length+=20
        fruit_pool=['watermelon','watermelon',
                    'apple',
                    'orange',
                    'bomb','bomb','bomb']
        lives=5
        lives_text.text=f'Lives Remaining: {lives}'
        levels_unlocked.append(6)
    
chopper=ball((5,5),5)
chopper.color=Color(180,180,20,255)

bottom=static_line((0,height),(width,height),5)

make_fruits()

add_observer(observer)

run()
