from codecs import ignore_errors
from datetime import date
import pandas
import numpy
import string
import random
import requests
import math
import datetime
import json

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
            response = requests.post("https://www.purpleorangepink.com/api/AccountManager/Register", json = {"Username": username, "Email": email, "Password": password}, verify = False)
            
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
            response = requests.post("https://www.purpleorangepink.com/api/User/Generic/UpdateUserInformation", cookies={".AspNetCore.Identity.Application": authenticationToken}, json = {"portal_type": "friends", "firstName": firstName, "lastName": lastName, "gender": gender, "age": age}, verify = False)
                        
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
        response = requests.post("https://www.purpleorangepink.com/api/User/Generic/UpdateUserInformation", cookies={".AspNetCore.Identity.Application": authenticationToken}, json = {"portal_type": "friends", "location": {"latitude": lat, "longitude": long}}, verify = False)
        
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
        response = requests.post("https://www.purpleorangepink.com/api/User/Friends/AddAttribute", json = {"attribute": attr}, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
        
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
        
    def setBirthdateOfUsers(): 
        for u in UserModule.users.index.values.tolist():
            birthdate = datetime.datetime(random.randint(1970, 2002), random.randint(1, 12), random.randint(1, 28))
            
            authenticationToken = str(UserModule.usersOther["authentication_token"].iloc[u])
            myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.post("https://www.purpleorangepink.com/api/User/Generic/UpdateUserInformation", json = {"portal_type": "friends", "birthdate": birthdate.strftime("%d/%m/%Y")}, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
                        
            if (response.status_code == 200):
                #authenticationToken = response.cookies[".AspNetCore.Identity.Application"]
                None
            elif (response.status_code == 404):
                print("got status code 404 for set birthdate")
                print(response.content)
            else:
                print("got unknown status code for set birthdate: " + str(response.status_code))
                print(response.request.body)
    
        
    def makeFriendSearchQueryRandom(radius, pageSize, numAttributes, minAge = 18, maxAge = 100, gender = "", pageNumber = 1, provideLocation = False):
        #list of attributes
        attributes = []
        
        #get index of user
        index = random.choice(UserModule.users.index.values.tolist())
        
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
        response = requests.post("https://www.purpleorangepink.com/api/User/Friends/SearchUsers", json = body, cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
        
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
            response = requests.delete("https://www.purpleorangepink.com/api/AccountManager/Remove", cookies={".AspNetCore.Identity.Application": authenticationToken}, verify = False)
              
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
        
    #ACTIVITIES
    #list of users
    
    #dont save activity details, just save user-to-activity links
    
    activities = pandas.DataFrame(columns={"activity_id"})
    activityLinks = pandas.DataFrame(columns={"user_index", "activity_id", "position"})
    
    def createRandomActivities(numActivities, lat, long, radius):
        for i in range(numActivities):
            #get random user
            userIndex = random.choice(UserModule.users.index.values.tolist())
            userAuthToken = str(UserModule.usersOther["authentication_token"].iloc[i])
            
            #generate user values
            title = "".join(random.choice(UserModule.lettersAndNumbers) for ii in range(10))
            
            dateTime = datetime.datetime(random.randint(1970, 2002), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
            stringDate = dateTime.strftime("%d/%m/%Y %H:%S")

            isPhysical = (random.randint(0, 9) > 2)
            
            #make random location
            
            #get radial components
            rx = random.SystemRandom().uniform(-1.0, 1.0) * radius
            ry = math.sqrt(radius ** 2.0 - rx ** 2.0) * (1.0 - 2.0 * float(random.randint(0, 1)))
            
            #get longitude and latitude
            latitude = ((ry / 24901.461 * 360)) + lat
            longitude = ((rx / 24901.461 * 360)) + long

            size = random.randint(0, 10)
            
            gender = ''.join(random.choice(["all", "all", "all", "male", "female"]) for i in range (1))
            
            minAge = random.randint(18, 25)
            maxAge = random.randint(40, 100)

            body = {}

            if (isPhysical):
                #set target location
                
                #20% chance we set search location
                if (random.randint(0, 9) > 7):                    
                    body = {
                        "portal_type": "friends",
                        "title": title,
                        "datetime": stringDate,
                        "isPhysical": isPhysical,
                        "gender": gender,
                        "minimumAge": minAge,
                        "maximumAge": maxAge,
                        "targetLocation":  {
                            "latitude": latitude,
                            "longitude": longitude,
                        },
                        "searchLocation":  {
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                    }
                else:
                    body = {
                        "portal_type": "friends",
                        "title": title,
                        "datetime": stringDate,
                        "isPhysical": isPhysical,
                        "gender": gender,
                        "minimumAge": minAge,
                        "maximumAge": maxAge,
                        "targetLocation":  {
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                    }
            else:
                #80% chance we set target location
                if (random.randint(0, 9) > 1):
                    body = {
                        "portal_type": "friends",
                        "title": title,
                        "datetime": stringDate,
                        "isPhysical": isPhysical,
                        "gender": gender,
                        "minimumAge": minAge,
                        "maximumAge": maxAge,
                        "searchLocation": {
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                    }
                else:
                    body = {
                        "portal_type": "friends",
                        "title": title,
                        "datetime": stringDate,
                        "isPhysical": isPhysical,
                        "gender": gender,
                        "minimumAge": minAge,
                        "maximumAge": maxAge
                    }
                        
            #create user in server
            myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
            response = requests.post("https://www.purpleorangepink.com/api/User/Friends/CreateActivity", json = body, cookies={".AspNetCore.Identity.Application": userAuthToken}, verify = False)
            
            activityId = ""
            
            if (response.status_code == 200):
                activityId = response.json()["stats"]["activity_id"]
            elif (response.status_code == 404):
                print("got status code 404 for creating activity")
                #print(response.content)
                print(response.raw)
                print()
            else:
                print("got unknown status code for creating activity: " + str(response.status_code))
                #print(response.request.body)
                print()
                print(response.content)
                print()
                
            UserModule.activities = UserModule.activities.append({"activity_id": activityId}, ignore_index = True)    
            UserModule.activityLinks = UserModule.activityLinks.append({"user_index": userIndex, "activity_id": activityId, "position": "admin"}, ignore_index=True)
    
    def saveActivities(): 
        UserModule.activities.to_csv("data/created_activities.csv", index=False)
        UserModule.activityLinks.to_csv("data/created_activity_links.csv", index=False)
        
    def loadExistingActivities():
        UserModule.activities = pandas.read_csv("data/created_activities.csv")
        UserModule.activityLinks = pandas.read_csv("data/created_activity_links.csv")
    
    def joinUsersToActivitiesRandom(numUsers, numActivitiesPerUser):
        for ui in UserModule.users.index.values.tolist():
            userAuthToken = str(UserModule.usersOther["authentication_token"].iloc[ui])
            
            randomActivityRange = random.randint(1, numActivitiesPerUser)
            
            for ai in range (randomActivityRange):
                activityIndex = random.choice(UserModule.activities.index.values.tolist())
                activityId = UserModule.activities["activity_id"].iloc[activityIndex]
                
                myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
                response = requests.get("https://www.purpleorangepink.com/api/User/Friends/RequestToJoinActivityAsParticipant?id=" + str(activityId), cookies={".AspNetCore.Identity.Application": userAuthToken}, verify = False)
                 
                if (response.status_code == 200):
                    pass
                elif (response.status_code == 404):
                    print("got status code 404 for joining activity")
                    #print(response.content)
                    print(response.raw)
                    print()
                else:
                    print("got unknown status code for joining activity: " + str(response.status_code))
                    #print(response.request.body)
                    print()
                    print(response.content)
                    print()
                
                #add to activities links
                UserModule.activityLinks = UserModule.activityLinks.append({"user_index": ui, "activity_id": activityId, "position": "participant"}, ignore_index=True)
    
    def adminUsersToActivitiesRandom(numUsers, numActivitiesPerUser):
        for ui in UserModule.users.index.values.tolist():
            userAuthToken = str(UserModule.usersOther["authentication_token"].iloc[ui])
            
            randomActivityRange = random.randint(1, numActivitiesPerUser)
            
            for ai in range (randomActivityRange):
                activityIndex = random.choice(UserModule.activities.index.values.tolist())
                activityId = UserModule.activities["activity_id"].iloc[activityIndex]
                
                myHeaders = {"Content-Type": "application/json", "User-Agent": "PostmanRuntime/7.28.4", "Accept": "*/*", "Connection": "keep-alive", "Host": "Testing_Program"}
                response = requests.get("https://www.purpleorangepink.com/api/User/Friends/JoinActivityAsAdmin?id=" + str(activityId), cookies={".AspNetCore.Identity.Application": userAuthToken}, verify = False)
                
                if (response.status_code == 200):
                    pass
                elif (response.status_code == 404):
                    print("got status code 404 for admining activity")
                    #print(response.content)
                    print(response.raw)
                    print()
                else:
                    print("got unknown status code for admining activity: " + str(response.status_code))
                    #print(response.request.body)
                    print()
                    print(response.content)
                    print()
                
                #add to activities links
                UserModule.activityLinks = UserModule.activityLinks.append({"user_index": ui, "activity_id": activityId, "position": "admin"}, ignore_index=True)

    
    def adminUserToActivity(userIndex, activityIndex):
        return 0
    
    def removeExistingActivities():
        UserModule.saveActivities()
