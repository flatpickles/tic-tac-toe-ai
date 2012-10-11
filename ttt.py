import sys

state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
game  = [0, 0, 0, 0, 0, 0, 0, 0]
wins = [None for i in range(9)]
# cols:   d1/d2\h1_h2-h3^v1<v2|v3>
wins[0] = [1, 0, 1, 0, 0, 1, 0, 0]
wins[1] = [0, 0, 1, 0, 0, 0, 1, 0]
wins[2] = [0, 1, 1, 0, 0, 0, 0, 1]
wins[3] = [0, 0, 0, 1, 0, 1, 0, 0]
wins[4] = [1, 1, 0, 1, 0, 0, 1, 0]
wins[5] = [0, 0, 0, 1, 0, 0, 0, 1]
wins[6] = [0, 1, 0, 0, 1, 1, 0, 0]
wins[7] = [0, 0, 0, 0, 1, 0, 1, 0]
wins[8] = [1, 0, 0, 0, 1, 0, 0, 1]

def addArr(a, b, c):
  out = []
  for i in range(len(a)):
    out.append(a[i] + c * b[i])
  return out

def p2d(a):
  m = [[a[6], a[7], a[8]], [a[3], a[4], a[5]], [a[0], a[1], a[2]]]
  for l in m:
    print "[%s][%s][%s]" % (" " if l[0] == 0 else ("X" if l[0] == 1 else "O"),\
                            " " if l[1] == 0 else ("X" if l[1] == 1 else "O"),\
                            " " if l[2] == 0 else ("X" if l[2] == 1 else "O"),)

def noState(n, flag):
  return flag == None and state[n] == 0

def checkGame():
  # get status
  status = 0
  if 3 in game: status = 1
  elif -3 in game: status = 2
  elif not 0 in state: status = 3
  # respond
  if status:
    if status == 1:
      print "You win! Final board:"
    elif status == 2:
      print "You lose. Final board:"
    else:
      print "Tie game. Final board:"
    p2d(state)
    sys.exit(0)

def play(x, y, player): # user: 1, comp: -1
  global game
  global state
  state[3 * y + x] = 1 if player > 0 else 2
  game = addArr(game, wins[3 * y + x], player)
  checkGame()

def compPlay():
  global game
  best = None
  i2 = -1 # find where user might be about to win
  try: i2 = game.index(2)
  except Exception: pass

  # solve advanced game states
  blocking = False
  splitting = False

  # detect split cases (the user attempting a split)
  cornerSplitCase = (state[0] == 1 and state[8] == 1) or (state[2] == 1 and state[6] == 1)
  edgeSplitCase = -1;
  if (state[1] == 1 and state[3] == 1 and noState(0, None)): edgeSplitCase = 0
  if (state[3] == 1 and state[7] == 1 and noState(6, None)): edgeSplitCase = 6
  if (state[7] == 1 and state[5] == 1 and noState(8, None)): edgeSplitCase = 8
  if (state[5] == 1 and state[1] == 1 and noState(2, None)): edgeSplitCase = 2

  # solve for win, block, and setup
  for i in range(9):
    if not noState(i, None): continue
    nextR = addArr(game, wins[i], -1)
    if -3 in nextR: # win
      best = i
      break
    elif not blocking and i2 >= 0 and nextR[i2] != 2: # block
      best = i
      blocking = True
    elif not (blocking or splitting) and nextR.count(-2) > 0: # setup for next turn
      if not cornerSplitCase and edgeSplitCase < 0: best = i
      if nextR.count(-2) > 1: splitting = True # split

  # address edge split case, if necessary
  if edgeSplitCase >= 0: best = edgeSplitCase

  # solve basic state or corner split case
  if best == None:
    # center if possible
    if noState(4, best): best = 4
    # edge case: don't get split
    if not cornerSplitCase:
      # play corners (if not in corner split case)
      if noState(0, best): best = 0
      elif noState(2, best): best = 2
      elif noState(6, best): best = 6
      elif noState(8, best): best = 8
    # play middle edges if corner split case, or no corners free
    if noState(1, best): best = 1
    elif noState(3, best): best = 3
    elif noState(5, best): best = 5
    elif noState(7, best): best = 7

  # do it
  if best != None: play(best % 3, best / 3, -1)

# I/O loop
while True:
  if game.count(0) == 8:
    print "\nWelcome! You are X and will play first.\nEnter (x, y) coordinates of your desired move; \nthe board is zero indexed from bottom left.\n"

  p2d(state)

  tryAgain = True
  while tryAgain:
    try:
      x = input("x: ")
      y = input("y: ")
      if x > 2 or x < 0 or y > 2 or y < 0: raise Exception()
      if noState(y * 3 + x, None):
        play(x, y, 1)
        tryAgain = False
      else:
        print "That space is taken, try again"
    except Exception as e:
      print "Invalid input, try again"

  compPlay()