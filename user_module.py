from codecs import ignore_errors
import pandas
import numpy
import string
import random
import requests
import math

class UserModule:
    #list of users
    users = pandas.DataFrame(columns={"username", "password", "firstname", "lastname", "email", "age", "gender", "longitude", "latitude", "friendattributes"})
    usersOther = pandas.DataFrame(columns={"username", "authentication_token"})
    names = None
    friendAttributes = pandas.DataFrame(columns={"attribute"})
    
    lettersAndNumbers = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
    
    def init():
        UserModule.names = pandas.read_csv("data/names.csv")
    
    #create users
    #numUsers: number of users to create
    def createUsers(numUsers):
        #change type of attributes column
        UserModule.users = UserModule.users.astype({"friendattributes": object})
        
        #number of names in the names table
        namesCount = UserModule.names.shape[0]
        
        for i in range(numUsers):
            
            #generate user values
            firstName = UserModule.names["name"][random.randint(0, namesCount)]
            
            lastName = UserModule.names["name"][random.randint(0, namesCount)]
                
            username = firstName + lastName[0] + ''.join(random.choice(UserModule.lettersAndNumbers) for i in range(10))
            
            password = ''.join(random.choice(UserModule.lettersAndNumbers) for i in range(10))
            
            gender = ''.join(random.choice(["male", "female"]) for i in range (1))
            email = firstName + lastName + username + "@gmail.com"
            age = random.randint(18, 70)
            longitude = random.SystemRandom().uniform(-180, 180) #random float from 180 to -180
            latitude = random.SystemRandom().uniform(-90, 90) #random float from 90 to -90
            
            #create user in server
            myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.post("https://localhost:5001/api/AccountManager/Register", json = {"Username": username, "Email": email, "Password": password}, verify = False)
            
            authenticationToken = ""
            
            if (response.status_code == 200):
                authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
            elif (response.status_code == 404):
                print("got status code 404 for registering user")
                #print(response.content)
                print(response.raw)
                print()
            else:
                print("got unknown status code for registering user: " + str(response.status_code))
                #print(response.request.body)
                print()
                print(response.content)
                print()
                
            #add basic information
            myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.post("https://localhost:5001/api/User/Generic/BasicInformation", cookies={".AspNetCore.Identity.Application": authenticationToken}, json = {"firstName": firstName, "lastName": lastName, "gender": gender, "age": age}, verify = False)
                        
            if (response.status_code == 200):
                None
            elif (response.status_code == 404):
                print("got status code 404 for basic information")
                print(response.content)
            else:
                print("got unknown status code for basic information: " + str(response.status_code))
                print(response.request.body)
                
            #add users to dataframes
            UserModule.users = UserModule.users.append({"username": username, "password": password, "firstname": firstName, "lastname": lastName, "email": email, "age": age, "gender": gender, "longitude": longitude, "latitude": latitude, "friendattributes": []}, ignore_index = True)
            UserModule.usersOther = UserModule.usersOther.append({"username": username, "authentication_token": authenticationToken}, ignore_index = True)
    
    def makeRandomCenteredLocationEachUser(lat, long, radius):
        for u in UserModule.users.index.values.tolist():
            UserModule.makeRandomCenteredLocation(u, lat, long, radius)
    
    #make random locations for users within a certain radius
    #max radius value is half the radius of the earth (this may too cause problems)
    def makeRandomCenteredLocation(index, lat, long, radius):
        #get radial components
        rx = random.SystemRandom().uniform(-1.0, 1.0) * radius
        ry = math.sqrt(radius ** 2.0 - rx ** 2.0) * (1.0 - 2.0 * float(random.randint(0, 1)))
        
        #get longitude and latitude
        latitude = ((ry / 24901.461 * 360)) + lat
        longitude = ((rx / 24901.461 * 360)) + long
        
        #set in database
        UserModule.users.at[index, "longitude"] = longitude
        UserModule.users.at[index, "latitude"] = latitude
        
        #send location to user
        UserModule.sendLocation(index, latitude, longitude)
             
    #send locations
    def sendLocations():
        for u in UserModule.users.index.values.tolist():
            UserModule.sendLocation(u, UserModule.users["longitude"].iloc[0], UserModule.users["latitude"].iloc[0])
    
    #send location
    #index: index of user in users table
    def sendLocation(index, lat, long):
        authenticationToken = str(UserModule.usersOther["authentication_token"].iloc[index])
        myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
        response = requests.post("https://localhost:5001/api/User/Friends/SetLocation", json = {"latitude": lat, "longitude": long}, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
        
        if (response.status_code == 200):
            #authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
            None
        elif (response.status_code == 404):
            print("got status code 404 for set location")
            print(response.content)
        else:
            print("got unknown status code for set location: " + str(response.status_code))
            print(response.request.body)
                
    #add attribute to attribute list for user at index {index}
    def addFriendAttribute(index, attr):  
        #att attribute to table      
        
        #add attribute to server
        authenticationToken = str(UserModule.usersOther["authentication_token"].iloc[index])
        myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
        response = requests.post("https://localhost:5001/api/User/Friends/AddAttribute", json = {"attribute": attr}, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
        
        if (response.status_code == 200):
            #authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
            None
        elif (response.status_code == 404):
            print("got status code 404 for adding friend attribute")
            print(response.content)
        else:
            print("got unknown status code for addiing friend attribute: " + str(response.status_code))
            print(response.request.body)
        
        try:
            attributeReturned = response.json()["attribute_name"]
        except Exception:
            attributeReturned = None;
        
        if (attributeReturned != None):
            if (attributeReturned not in UserModule.friendAttributes["attribute"].values):
                UserModule.friendAttributes = UserModule.friendAttributes.append({"attribute": attributeReturned}, ignore_index = True)
                
            UserModule.users.at[index, "friendattributes"] = (UserModule.users["friendattributes"].iloc[index] + [attributeReturned])
        
        return
        
    def makeRandomNumAttributes(numAttributes):
        #number of users
        numUsers = UserModule.users.shape[0]
        
        #for each random attribute
        for a in range(numAttributes):
            UserModule.makeRandomAttributes(random.randint(1, numUsers))
        
    def makeRandomAttributes(numUsers):
        attributeName = ''.join(random.choice(UserModule.lettersAndNumbers) for i in range(4))

        randomList = []
        
        #get random list of user indexes
        for i in range(numUsers):
            #randomList += [random.randint(0, numUsers - 1)]
            randomList += [random.choice(UserModule.users.index.values.tolist())]
            
        #add random users to new random attribute
        for u in randomList:
            UserModule.addFriendAttribute(u, attributeName)
        
    def makeFriendSearchQueryRandom(radius, pageSize, numAttributes, minAge = 18, maxAge = 100, gender = "", pageNumber = 1, provideLocation = False):
        #list of attributes
        attributes = []
        
        #get index of user
        index = random.choice(UserModule.users.index.values.tolist())
        
        print(UserModule.friendAttributes.shape[0])
        
        #get random list of attributes of quantity numAttributes
        for i in range(numAttributes):
            attributes += [UserModule.friendAttributes["attribute"].iloc[random.randint(0, UserModule.friendAttributes.shape[0] - 1)]]
            
        #call make query function
        UserModule.makeFriendSearchQuery(index, radius, pageSize, attributes, minAge, maxAge, gender, pageNumber, provideLocation)
        
    def makeFriendSearchQuery(index, radius, pageSize, attributes, minAge = 18, maxAge = 100, gender = "", pageNumber = 1, provideLocation = False):
        #download the response and put in file or convert json list to csv
        body = {}
        
        if (provideLocation):
            body = {"location": {"latitude": random.SystemRandom().uniform(-90, 90), "longitude": random.SystemRandom().uniform(-180, 180)}, "radius": radius, "pageSize": pageSize, "pageNumber": pageNumber, "minimumAge": minAge, "maximumAge": maxAge, "gender": gender, "attributes": attributes}
        else:
            body = {"radius": radius, "pageSize": pageSize, "pageNumber": pageNumber, "minimumAge": minAge, "maximumAge": maxAge, "gender": gender, "attributes": attributes}
        
        authenticationToken = str(UserModule.usersOther["authentication_token"].iloc[index])
        myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
        response = requests.post("https://localhost:5001/api/User/Friends/SearchUsers", json = body, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
        
        if (response.status_code == 200):
            #authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
            None
        elif (response.status_code == 404):
            print("got status code 404 for make friend search query")
            print(response.content)
        else:
            print("got unknown status code for make freind search query: " + str(response.status_code))
            print(response.request.body)
        
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
        UserModule.usersOther.to_csv("data/created_users_authentication.csv", index=False)
        UserModule.friendAttributes.to_csv("data/friend_attributes.csv", index=False)
        
    def loadExistingUsers():
        UserModule.users = pandas.read_csv("data/created_users.csv")
        UserModule.usersOther = pandas.read_csv("data/created_users_authentication.csv")
        UserModule.friendAttributes = pandas.read_csv("data/friend_attributes.csv")