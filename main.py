
class rule:
  State: str
  Input: str
  Pop: str
  NextState: str
  Push: list
  def __init__(self,state,sInput,pop,nextState,push):
    self.State = state
    self.Input = sInput
    self.Pop = pop
    self.NextState = nextState
    self.Push = push
  def __str__(self):
    return (f"[{self.State},{self.Input},{self.Pop},{self.NextState},{self.Push}]")
    
daRulez: list[rule] = []

def evaluate_syntax(html_path):
  """
  Melakukan evaluasi sintaks dengan PDA

  Args:
    pda: Object PDA
    html: String HTML

  Returns:
    String "Accepted" jika input diterima atau "Syntax Error" di line ke [current_position]
  """

  global startState
  global startStack
  global daRulez
  global acceptStates
  global acceptStateEmptyStacks

  rule_found: bool

  stack = [startStack]
  current_state = startState
  current_position = 0
  line_count = 0 #line pointer

  try :
    with open(html_path,'r') as html:
      #for every line in the html
      for line in html:
        line_count += 1
        current_position = 0 #ini kaya, col pointer

        #for every char in the line, strip is to remove \n lololol
        for char in line.strip():
            rule_found = False
            for rulez in daRulez:
              #find a rule that fits both readed char and current stack top
              #print (stack[0],rulez.Pop)
              if check_char(char, rulez.Input) and stack[0] == rulez.Pop:
                #do the things that need to be done
                current_state = rulez.NextState
                stack = stack[1:]
                if rulez.Push != []:
                  stack = rulez.Push + stack
                rule_found = True
                #break the rulez loop to continue to the next char
                break
            
            #if no rules are found, error is raised
            if (not rule_found):
              print(line)
              print(f"Error at line {line_count}, col {current_position}")
              raise ValueError("invalid char!")

    #udah closed at this point
    if current_state in acceptStates:
      print("Accepted")
    elif current_state in acceptStateEmptyStacks and stack == []:
      print("Accepted")
    else:
      print(current_state,acceptStates)
      print("File unfinished!/ Incomplete!")
      #return f"Syntax Error di line ke {current_position}, transisi {invalid_transition}"

  except ValueError:
    print("Error at this line")

def check_char(read: str,rule: str) -> bool:
  #fungsi ini diperlukan karena ada beberapa char kusus
  if rule == 'ANY':
    return True
  elif read == 'EMPTY':
    return True
  elif read == rule:
    return True
  else:
    return False
    


def read_pda(filename):
  global daRulez
  global states
  global inputSymbols
  global stackSymbols
  global startState
  global startStack
  global acceptStates
  global acceptStateEmptyStacks

  with open(filename) as pdatxt:
    states = pdatxt.readline().strip().split()
    inputSymbols = pdatxt.readline().strip().split()
    stackSymbols = pdatxt.readline().strip().split()
    startState = pdatxt.readline().strip().split()[0]
    startStack = pdatxt.readline().strip().split()[0]
    acceptStates = pdatxt.readline().strip().split()
    acceptStateEmptyStacks = pdatxt.readline().strip().split()

    #rules
    for lines in pdatxt:
      #print(lines)
      line = lines.strip().split()
      #print(line)
      state = line[0]
      sInput = line[1]
      pop = line[2]
      nextState = line[3]
      if len(line) > 4:
        push = line[4].split(",")
      else:
        push = []
      daRulez.append(rule(state,sInput,pop,nextState,push))


read_pda("test.txt")
evaluate_syntax("testhtml.txt")