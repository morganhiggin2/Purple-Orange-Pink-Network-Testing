import pandas
import numpy
import string
import random

class UserModule:
    #list of users
    users = pandas.DataFrame(columns={"username", "password", "firstname", "lastname", "email", "age", "gender", "longitude", "latitude"})
    names = None
    
    def init():
        UserModule.names = pandas.read_csv("data/names.csv")
    
    #create users
    #numUsers: number of users to create
    def createUsers(numUsers):
        lettersAndNumbers = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
        
        #number of names in the names table
        namesCount = UserModule.names.shape[0]
        
        for i in range(numUsers):
            
            firstName = UserModule.names["name"][random.randint(0, namesCount)]
            
            lastName = UserModule.names["name"][random.randint(0, namesCount)]
                
            username = firstName + lastName[0] + ''.join(random.choice(lettersAndNumbers) for i in range(10))
            
            password = ''.join(random.choice(lettersAndNumbers) for i in range(10))
            
            gender = ''.join(random.choice(["male", "female"]) for i in range (1))
            email = firstName + lastName + username + "@gmail.com"
            age = random.randint(18, 70)
            longitude = 0
            latitude = 0
            
            #UserModule.users.append({"username": username}, ignore_index = True)
            UserModule.users = UserModule.users.append({"username": username, "password": password, "firstname": firstName, "lastname": lastName, "email": email, "age": age, "gender": gender, "longitude": longitude, "latitude": latitude}, ignore_index = True)
            
        UserModule.users.to_csv("data/created_users.csv", index=False)
    