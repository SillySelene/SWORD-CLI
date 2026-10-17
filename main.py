import requests
import json
import curses

s = requests.Session()

API_URL = "http://localhost:5000"

health_check = s.get(API_URL + "/health")

print(health_check.text)

def initTUI():
    # initialize the TUI pretty please
    std_scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    std_scr.keypad(True)
    # all the really fun curses init stuff ^

    selection= curses.newwin(10, 10, 5, 5)
    selection.addstr("HAAHAHAH")

    selection.getkey()

    std_scr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def GETHandler(args):
    GETRoutes = {       
        "tools" : "/tools",
        "code" : "/code",    
        "codecategory" : "/code/category",
        "codebytoolid" :  f"/code/t/{ f'/{args[1]}' if len(args) > 1 else ''}",
        "codebycategoryid" : f"/code/c{ f'/{args[1]}' if len(args) > 1 else ''}",
        "doc" : f"/doc{ f'/{args[1]}' if len(args) > 1 else ''}",
        "doccategory" : "/doc/category",
        "docbytoolid" :  f"/code/t/{ f'/{args[1]}' if len(args) > 1 else ''}",
        "docbycategoryid" : f"/code/c{ f'/{args[1]}' if len(args) > 1 else ''}",
        "dev" : "/dev"
    }
    if args[0].lower() in GETRoutes.keys():
        routePartOne = GETRoutes[args[0].lower()]
        r = s.get(API_URL + routePartOne)
        print(r.text)
        return r.json()
    else:
        print("you passed a route that doesnt exist")

# Games, infinite games? but no games?
# Okay....

def PUSHHandler(args):
    PUSHRoutes = {
        "tool" : "/tool",
        "code" : "/snippet",
        "codecategory" : "/c-category",
        "doccategory" : "/d-category",
        "doc" : "/doc",    }
    schemas = {
        "toolschema" : {
        "toolName" : {"type" : "str", "required" : True}
    },
        "codecategoryschema" : {
        "categoryName" : {"type" : "str", "required" : True}
    },
        "doccategoryschema" : {
        "categoryName" : {"type" : "str", "required" : True}
    },
        "snippetschema" : {
        "snippetName" : {"type" : "str", "required": True},
        "snippet" : {"type" : "str", "required" : True},
        "tool" : {"type" : "str", "required" : True },
        "categories" : {"type" : "arr", "required" : True}
    },
        "docschema" : {
        "docName" : {"type" : "str", "required" : True},
        "tool" : {"type" : "str", "required" : True},
        "category" : {"type" : "str", "required" : True},
        "docText" : {"type" : "str", "required" : True}
    },
    }
    

    if(args[0] in PUSHRoutes.keys()):
        routePartOne = PUSHRoutes[args[0].lower()]
        if(args[1] in schemas.keys()):
            chosenSchema = schemas[args[1]]
            if(len(args) == 2):
            # Get input according to schema
                pass
            else:
                # parse args for input
                schemaKeys = chosenSchema.keys()
                j = 2
                for i in schemaKeys:
                    chosenSchema[i] = args[j]
                    j += 1
                r = s.post(API_URL+"/dev" + routePartOne, data=chosenSchema)
                if(r.status_code == 201):
                    print(args[0] + " Made!")
                else:
                    print("failure, couldnt make " + args[0])
    else:
        print("gotta give me a route thats REAL sorry")

def PATCHHandler(args):
    getCurrent = GETHandler(args)
    if(getCurrent):
        data = getCurrent['data']
        j = 1
        returnObj = {}
        for arg in args[1:]:
            if(arg == "."):
                returnObj[data.keys()[j]] = data[data.keys()[j]]
            else:
                returnObj[data.keys()[j]] = arg
            j += 1
        r = s.post(API_URL + "/" + args[0], data=returnObj)
        if(r.status_code == 201):
            print("update successful")
        else:
            print("error: " + r.json())

def logIn(args):
    if(len(args) >= 2):
        email = args[0]
        password = args[1]
        res = s.post(API_URL + "/login", data={"email" : email, "password" : password})
        if res.status_code != 401:
            output = res.json()
            output = output['data']
            if(output['message'] == 'Log-In Successful'):
                print('Logged In!')
                s.headers.update({'authorization' : f'Bearer {output["token"]}'})




def getInput():
    print("Input: ")
    inp = input("")
    args = inp.split(" ")[1:]
    inp = inp.split(" ")[0]
    inp.lower()
    if(inp == "h" or inp == "help"):
        print(
"""(H)elp to bring up this menu
(G)et {colection} to GET for a certain thing. use '(G)et help'  for all options
(P)ush {collection} to PUSH for a certain thing. use '(P)ush help' for all options.
(U)pdate {collection} to PATCH for a certain thing. use '(U)pdate help' for all options.

(D)isplay data.
(T)UI will open the Terminal User Interface mode. (curses)

(L)ogin to log into your superuser account. (unless your the dev of a SWORD shard, this wont apply.)""")
        getInput()
    elif(inp == "g" or inp == "get"):
        print("GETTING")
        # this is where id put my GET code if i HAD ANY
        GETHandler(args)
        getInput()
    elif(inp == "p" or inp == "push"):
        # this is where id put my PUSH code if i HAD ANY!
        PUSHHandler(args)
        getInput()
    elif(inp == "u" or inp == "update"):
        PATCHHandler(args)
        # this is where id ... update
        getInput()
    elif(inp == "t" or inp == "tui"):
        # init TUI mode. first: make TUI mode.
        initTUI()
    elif(inp == "l" or inp == "login"):
        # Log In. eventually.
        logIn(args)
        getInput()
    elif(inp == "e" or inp == "exit"):
        pass



if health_check.json() == {"status":"alive"}:
    print("enter help for help. and e to exit")
    getInput()
