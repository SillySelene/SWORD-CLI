import requests
import json
import curses

s = requests.Session()

API_URL = "http://localhost:5000"

health_check = s.get(API_URL + "/health")

print(health_check.text)

def initTUI():
    # initialize the TUI pretty please
    pass

def GETHandler(args):
    GETRoutes = {       
        "tools" : "/tools",
        "code" : "/code",    
        "codecategory" : "/code/category",
        "codebytoolid" :  f"/code/t/{ f'/{args[1]}' if len(args) > 1 else ''}",
        "codebycategorylid" : f"/code/c{ f'/{args[1]}' if len(args) > 1 else ''}",
        "doc" : f"/doc{ f'/{args[1]}' if len(args) > 1 else ''}",
        "doccategory" : "/doc/category",
        "docbytoolid" :  f"/code/t/{ f'/{args[1]}' if len(args) > 1 else ''}",
        "docbycategoryid" : f"/code/c{ f'/{args[1]}' if len(args) > 1 else ''}",
        "dev" : "/dev"
    }
    if args[0] in GETRoutes.keys():
        routePartOne = GETRoutes[args[0].lower()]
        r = s.get(API_URL + routePartOne)
        print(r.text) 
    else:
        print("you passed a route that doesnt exist")

def PUSHHandler(args):
    pass

def UpdateHandler(args):
    pass

def logIn(args):
    print(args)
    print(len(args))
    if(len(args) >= 2):
        print("hi")
        email = args[0]
        password = args[1]

        res = s.post(API_URL + "/login", data={"email" : email, "password" : password})
        output = res.json()
        output = output['data']
        if(output['message'] == 'Log-In Successful'):
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
(G)et {collection} to GET for a certain thing. use '(G)et help'  for all options
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
        print("PUSHING")
        # this is where id put my PUSH code if i HAD ANY!
        getInput()
    elif(inp == "u" or inp == "update"):
        print("UPDATING")
        # this is where id ... update
        getInput()
    elif(inp == "t" or inp == "tui"):
        print("TUI")
        # init TUI mode. first: make TUI mode.
        initTUI()
    elif(inp == "l" or inp == "login"):
        # Log In. eventually.
        print("LOGGING IN")
        print(args)
        logIn(args)
        getInput()



if health_check.json() == {"status":"alive"}:
    print("enter help for help.")
    getInput()
