



#File looks like:
#number of states, alphabet
#GENERAL FORMAT: special status(optional),(Epsilons), state name, where to go if 1st element of alphabet, where to go if second element of alphabet, etc
#initial, 0, 1, 0  (if alphabet is 0,1)
#1,1,3
#2,3,1
#final, 3,0,2

def createNFA(inptstring):
    file = open("NFAstring.txt", "w+")
    file.write(str(len(inptstring)+1)+",01" +"\n")
    count  = 0
    length = len(inptstring)
    for char in inptstring[0:len(inptstring)]:
        if char == "0" and count >0:
            stringadd = str(count+1)+",n"
        elif char == "1" and count >0:
            stringadd = "n," + str(count+1)
        elif char == "0" and count ==0:
            stringadd = str(count+1)+",0"
        elif char == "1" and count ==0:
            stringadd = "0," + str(count+1)
        file.write("(0),"+"q"+str(count)+","+stringadd+"\n")    
        count = count+1
    file.write("final,"+ "(),"+"q"+str(count)+","+str(length)+ "," + str(length)+ "\n")
        

string1 = input("enter x1")
string2 = input("enter x2")
x1 = string1
x2 = string2
if len(string2)<len(string1):
    x1,x2 = x2, x1

createNFA(x1)

userinput = x2
file = open("NFAstring.txt", "r")
deltafunction = []
line = file.readline().rstrip()

while line:
    deltafunction = deltafunction + [line.split(",")]
    line = file.readline().rstrip()
print(deltafunction)

userinput = x2

numberofstates = deltafunction[0][0]
alphabet = list(deltafunction[0][1])
currentstates = ["0"]
alphabetflag = False
activestates = []


#function gets epsilon states of all active (and sub active) states and returns updates list of active states.
def EpsilonFunction(deltafunction, activestates, numberofstates):
    print("INSIDE EPSILON FUNCTION", activestates)

    newstates = []
    #go through the list of newstates repeatedly until no new changes occur
    while len(newstates)!= len(activestates):
        print("INSIDE EPSILON WHILE LOOP")
        #if while loop condition is true, then we must make the newstates = active
        #states for the current iteration. If changes arise, the while loop
        #condition will become true again. If no changes, that means
        #we need to return the newstates list.

        #add all the active states to the new states.
        #this way, any changes made are only through epsilon functions.
        newstates = activestates
        print("newstate = activestate in the beginning of the loop?:", newstates == activestates)
        print("newstates:", newstates, "activestates:", activestates)
        #list stores the new states, for one iteration through the list. 
        states_to_add =[]
        
        #now, go through the newstates, and find the epsilon arrows:
        for state in newstates:
            state_delta = deltafunction[int(state)+1]
            epsilons = state_delta[state_delta.index("q"+str(state))-1].split(".")
            if epsilons != ["()"]:
                for epsilon in epsilons:
                    states_to_add += [epsilon.lstrip("(").rstrip(")")]
        print("states_to_add", states_to_add)
        #now remove duplicate elements from states to add
        non_duplicate = []
        for element in states_to_add:
            if element not in non_duplicate:
                non_duplicate.append(element)
        print("non_duplicate", non_duplicate)
        #now add all elements that were not previously in newstates to it
        for element in non_duplicate:
            if element not in activestates:
                activestates.append(element)
        print("newstates:", newstates, "activestates:", activestates)
        print("newstate = activestate at the end of the loop?:", newstates == activestates)
        #now, we have a newstates list with a possibility of new states.
        #if there are new states, while loop condition will be true.
        #else, while loop condition will fail.

    #if while loop condition fails, it means no new states.
    return newstates
           


def UpdateFunction(alphabet, deltafunction, activestates, inpt):
    newstates = []
    print("INSIDE UPDATE FUNCTION")
    print("ACTIVE STATES:", activestates)
    for state in activestates:
        print("state:", state)
        state_delta = deltafunction[int(state) + 1]
        #print("statedelta", state_delta)
        possible_state_add = [state_delta[state_delta.index("q"+str(state))+ alphabet.index(str(inpt))+1]]
        #print("possible_state_add", possible_state_add)
        if possible_state_add != ["n"]:
            print("!!!!!!!!!!!!!thi is a possible state add:::", possible_state_add)
            newstates += possible_state_add
            print("newstates after adding possible new states", newstates)
    
    newstates = list(set(newstates))
    return(newstates)



for i in userinput:
    if i not in alphabet:
        print("Error, user input contains non alphabet characters. Update alphabet or User Input")
        alphabetflag = True
        break



while userinput and not(alphabetflag):
    newstates = EpsilonFunction(deltafunction, currentstates, numberofstates)
    print("1 After Epsilon Function!!!!!!!!", newstates)
    currentinput = userinput[0]
    newstates = UpdateFunction(alphabet, deltafunction, newstates, currentinput)
    print("2 After Update Function4444444444444", newstates)
    newstates = EpsilonFunction(deltafunction, newstates, numberofstates)
    print("3 After Epsilon Function!!!!!!!!", newstates)
    userinput = userinput[1:]
    currentstates = newstates



finalstates =currentstates
print(newstates)
if str(len(x1)) in finalstates:
    print("accepted")
else:
    print("not accepted")
