

# AI for Robitics
# Lesson 1 - Localization
# Quiz: Localization Program

# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    for u, z in zip(motions, measurements):
        p = move(p, u[1], u[0], p_move, 1-p_move)
        p = sense(p, colors, sensor_right, z)

    return p

def sense(p, colors, sensor_right, measure):
    q = []
    s = 0
    for i in range(len(p)):
        l = []
        for j in range(len(p[i])):
            hit = (colors[i][j] == measure)
            l.append(p[i][j] * (hit * sensor_right + (1-hit) * (1 - sensor_right)))
        s = s + sum(l)
        q.append(l)
    # normalize
    for i in range(len(q)):
        for k in range(len(q[i])):
            q[i][k] = q[i][k] / s
        
    return q

# def sense(p, Z):
#     q=[]
#     for i in range(len(p)):
#         hit = (Z == world[i])
#         q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
#     s = sum(q)
#     for i in range(len(q)):
#         q[i] = q[i] / s
#     return q

def move(p, x, y, p_exact, p_fail):
    q = []
    # move x
    for i in range(len(p)): 
        row = []
        for j in range(len(p[i])):
            s = p[(i-y) % len(p)][(j-x) % len(p[i])] * p_exact
            s = p[(i) % len(p)][(j) % len(p[i])] * p_fail + s
            row.append(s)
        q.append(row)
    return q
    r = []
    # move y
    for i in range(len(p)):
        s = [p_exact * m for m in q[(i-y) % len(p)]]
        s = [p_fail * m + k for m, k in zip(q[(i-y+1) % len(p)], s)]
        r.append(s)
    return r

# def move_X(p, x):
#     q = []
#     for i in range(len(p)):
#         s = pExact * p[(i-x) % len(p)]
#         s = s + pOvershoot * p[(i-x-1) % len(p)]
#         s = s + pUndershoot * p[(i-x+1) % len(p)]
#         q.append(s)
#     return q

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
# show(p) # displays your answer

# exit(0)

## Test for sense()
p = [[0, 0, 0],
     [0, 1, 0],
     [0, 0, 0]]
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R']
sensor_right = 1.0
p = sense(p, colors, sensor_right, measurements[0])
# show(p)
# exit(0)

## Test for move()
p = [[0, 0, 0],
     [0, 1, 0],
     [0, 0, 0]]
x = 1
y = 1
p_exact = 0.9

p = move(p, x, y, p_exact, 1-p_exact)
show(p)
# exit(0)

# test 1
colors = [['G', 'G', 'G'],
          ['G', 'R', 'G'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0]])

if p != correct_answer:
    print 'Test#1 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #1 Passed'
# test 2
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.5, 0.5],
     [0.0, 0.0, 0.0]])

if p != correct_answer:
    print 'Test#2 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #2 Passed'

# test 3
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 0.8
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.06666666666, 0.06666666666, 0.06666666666],
     [0.06666666666, 0.26666666666, 0.26666666666],
     [0.06666666666, 0.06666666666, 0.06666666666]])

if p != correct_answer:
    print 'Test#3 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #3 Passed'

# test 4
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.03333333333, 0.03333333333, 0.03333333333],
     [0.13333333333, 0.13333333333, 0.53333333333],
     [0.03333333333, 0.03333333333, 0.03333333333]])

if p != correct_answer:
    print 'Test#4 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #4 Passed'

# test 5
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.0, 1.0],
     [0.0, 0.0, 0.0]])
if p != correct_answer:
    print 'Test#5 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #5 Passed'

# test 6
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 0.5
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0289855072, 0.0289855072, 0.0289855072],
     [0.0724637681, 0.2898550724, 0.4637681159],
     [0.0289855072, 0.0289855072, 0.0289855072]])

if p != correct_answer:
    print 'Test#6 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #6 Passed'

# test 7
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 0.5
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.33333333, 0.66666666],
     [0.0, 0.0, 0.0]])

if p != correct_answer:
    print 'Test#7 Failed'
    print 'Correct Answer:'
    show(correct_answer)
    print 'Result:'
    show(p)
else:
    print 'Test #7 Passed'
