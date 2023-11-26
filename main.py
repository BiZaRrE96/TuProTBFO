
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

  global stack
  global current_state
  rule_found: bool

  stack = [startStack]
  current_state = startState
  line_count = 0 #line pointer
  default_rule = None

  try :
    with open(html_path,'r') as html:
      #for every line in the html
      for line in html:
        line_count += 1

        current_line_length = 0
        for thing in line.strip("\n"):
          current_line_length += 1
        
        prog = 0 #progress
        while (prog < current_line_length):
            #DEBUG
            #print(char)
            if (find_rule(line[prog],True)):
              prog += 1
              #print(prog)
            #print("CHAR :",char)
            #print("TOP :",stack[0])
            
    #udah closed at this 
    loop_count = 0
    max_loop = 10
    print("STAGE 2")
    while (not (current_state in acceptStateEmptyStacks or current_state in acceptStates) and loop_count < max_loop):
        found = find_rule(line[prog-1],True)
        loop_count += 1
        #print(loop_count)
    if loop_count == max_loop:
      print("error, Too many empty loops")
    elif current_state in acceptStates:
      print("Accepted")
    elif current_state in acceptStateEmptyStacks and stack == []:
      print("Accepted")
    else:
      print("CURRENT STATE :",current_state)
      print("ACCEPTED STATES :",acceptStates)
      print("CURRENT STACK :",stack)
      print("DEFAULT RULE :",default_rule)
      print("File unfinished!/ Incomplete!")
      #return f"Syntax Error di line ke {current_position}, transisi {invalid_transition}"

  except ValueError:
    print("Current state:",current_state)
    print(stack)
    print(f"Error at line {line_count}, col {prog}")
    print(line)
    for i in range(prog):
      print(end=" ")
    print("^")
    print("Error at this line")

def find_rule(currentchar: chr, verbose: bool = False):
        global daRulez
        global stack
        default_rule = None
        
        for rulez in daRulez:
          #find a rule that fits both readed char and current stack top
          if verbose:
            pass
            
          
          if check_char(currentchar, rulez) and stack[0] == rulez.Pop and current_state == rulez.State:
            
            if (rulez.Input == "EMPTY"):
              if (verbose):
                print("DEFAULT RULE SET:",rulez)
              default_rule = rulez
              pass
            else:
              #DEBUG
              #print(stack)
              #do the things that need to be done
              if verbose:
                print(currentchar)
                print(stack)
                print("ACCEPTED RULE:",rulez)
              accept_rule(rulez)
              return True
              #break the rulez loop to continue to the next char
            
        #if no rules are found, error is raised
        
        if (default_rule != None):
          if verbose: print("DEFAULT RULE ACCEPTED :",default_rule)
          accept_rule(default_rule)
        else:
          raise ValueError("invalid char!")
        return False

def check_char(read: str,rulez: rule) -> bool:
  #fungsi ini diperlukan karena ada beberapa char kusus
  if rulez.Input == 'ANY':
    return True
  elif rulez.Input == 'EMPTY':
    return True
  elif rulez.Input == 'SPACE' and read == ' ':
    return True
  elif read == rulez.Input:
    return True
  else:
    return False
    
def accept_rule(rulez: rule):
  global current_state
  global stack
  
  current_state = rulez.NextState
  stack = stack[1:]
                
  if rulez.Push != ["EMPTY"] and rulez.Push != [] :
    stack = rulez.Push + stack


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
      try:
        if line == []:
          pass
        elif line[0][0] == "#":
          pass
        else:
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
      except :
        print("Error reading this rule :")
        print(lines)
        exit(1)


read_pda("pda.txt")
evaluate_syntax("testhtml.txt")