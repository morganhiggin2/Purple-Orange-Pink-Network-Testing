from codecs import ignore_errors
import pandas
import numpy
import string
import random
import requests

class UserModule:
    #list of users
    users = pandas.DataFrame(columns={"username", "password", "firstname", "lastname", "email", "age", "gender", "longitude", "latitude", "friendattributes"})
    usersOther = pandas.DataFrame(columns={"username", "authentication_token"})
    names = None
    
    def init():
        UserModule.names = pandas.read_csv("data/names.csv")
    
    #create users
    #numUsers: number of users to create
    def createUsers(numUsers):
        #change type of attributes column
        UserModule.users = UserModule.users.astype({"friendattributes": object})
        
        lettersAndNumbers = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
        
        #number of names in the names table
        namesCount = UserModule.names.shape[0]
        
        for i in range(numUsers):
            
            #generate user values
            firstName = UserModule.names["name"][random.randint(0, namesCount)]
            
            lastName = UserModule.names["name"][random.randint(0, namesCount)]
                
            username = firstName + lastName[0] + ''.join(random.choice(lettersAndNumbers) for i in range(10))
            
            password = ''.join(random.choice(lettersAndNumbers) for i in range(10))
            
            gender = ''.join(random.choice(["male", "female"]) for i in range (1))
            email = firstName + lastName + username + "@gmail.com"
            age = random.randint(18, 70)
            longitude = random.SystemRandom().uniform(-180, 180) #random float from 180 to -180
            latitude = random.SystemRandom().uniform(-90, 90) #random float from 90 to -90
            
            #create user in server
            myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.post("https://localhost:5001/api/AccountManager/Register", json = {"userName": username, "email": email, "password": password}, verify = False)
            
            authenticationToken = ""
            
            if (response.status_code == 200):
                authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
            elif (response.status_code == 404):
                print("got status code 404 for registering user")
                print(response.content)
            else:
                print("got unknown status code for registering user: " + str(response.status_code))
                print(response.request.body)
            
            #add users to dataframes
            UserModule.users = UserModule.users.append({"username": username, "password": password, "firstname": firstName, "lastname": lastName, "email": email, "age": age, "gender": gender, "longitude": longitude, "latitude": latitude, "friendattributes": []}, ignore_index = True)
            UserModule.usersOther = UserModule.usersOther.append({"username": username, "authentication_token": authenticationToken}, ignore_index = True)
        
    #add attribute to attribute list for user at index {index}
    def addFriendAttribute(index, attr):        
        UserModule.users.at[index, "friendattributes"] = (UserModule.users["friendattributes"].iloc[index] + ["hello"])
        
        return
        
    def makeFriendSearchQuery():
        #download the response and put in file or convert json list to csv
        return
        
    def removeUsers():
        #save the users 
        UserModule.saveUsers()
        
        #remove users from database
        for i in UserModule.users.index.tolist():
            authenticationToken = str(UserModule.usersOther["authentication_token"].iloc[i])
            myHeaders = {"User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.delete("https://localhost:5001/api/AccountManager/Remove", cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
              
            if (response.status_code == 200):
                None          
            elif (response.status_code == 404):
                print("got status code 404 for removing user")
                print(response.content)
                print(response.headers)
            else:
                print("got unknown status code for removing user: " + str(response.status_code))
                print(response.request.body)
            
    
    def saveUsers(): 
        UserModule.users.to_csv("data/created_users.csv", index=False)