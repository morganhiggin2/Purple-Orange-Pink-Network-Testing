import pandas
import numpy
from user_module import UserModule

#initialize
UserModule.init()

#user input loop
while True:
    user_input = input().split(" ")
    
    len = user_input.__len__()
    
    if (len >= 1):
        if (user_input[0] == "exit"):
                #remove users
                UserModule.removeUsers()
            
                exit(0)
        elif (user_input[0] == "create"):
            if (len >= 2):
                if(user_input[1] == "users"):
                    if (len >= 3):
                        #create user
                        UserModule.createUsers(int(user_input[2]))
                    else:
                        print("not valid command")
                else:
                    print("not valid command")
            else:
                print("not valid command")
        else:
            print("not valid command")
    else:
        print("not valid command")
    
    #match user_input.lower():
    #    case "create users"
    
    # do something based on the user input here
    # alternatively, let main do something with
    # self.last_user_input
    
    