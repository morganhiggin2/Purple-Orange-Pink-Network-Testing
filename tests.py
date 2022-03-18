#can just run this file and put call to test at top if wanting to just run tests and avoid command line

from torch import floor
from user_module import UserModule
import datetime
import random
import math

#file for query tests
class FriendTests:
    numUsers = 10
    numActivities = 5
    
    #test custom attributes
    def testAttributesQuery():
        #init
        UserModule.init()
        
        #create users
        UserModule.createUsers(4)
        
        #add attributes
        #UserModule.addFriendAttribute(0, "hello")
        #UserModule.makeRandomNumAttributes(2)
        
        #call query
        
        #remove users
        UserModule.removeUsers()
        
        return
    
    def testOneStart(): 
        #init
        UserModule.init()
        
        #create users
        UserModule.createUsers(FriendTests.numUsers)
        
        #save incase the next commands crash
        UserModule.saveUsers()
        
        #set birthdays
        UserModule.setBirthdateOfUsers()
        
        #add attributes
        UserModule.makeRandomNumAttributes(1)
        
        #set locations
        UserModule.makeRandomCenteredLocationEachUser(37.8715, -122.2730, 10)
        
        #create activities
        UserModule.createRandomActivities(FriendTests.numActivities, 37.8715, -122.2730, 10)
        
        #save activities
        UserModule.saveActivities()
        
        #join users to activities
        UserModule.joinUsersToActivitiesRandom(FriendTests.numUsers, math.floor(FriendTests.numActivities / 2))
        
        #join users to admins of activities
        UserModule.adminUsersToActivitiesRandom(math.floor(FriendTests.numUsers / 2), math.floor(FriendTests.numActivities / 4))
        
        #make query
        #UserModule.makeFriendSearchQueryRandom(2000, 2, 2)
        
        #save users
        UserModule.saveUsers()
        
    def testOneEnd():
        #load users
        UserModule.loadExistingUsers()
        
        #load activities
        #UserModule.loadExistingActivities()
        
        #can do testing for joining, admin requesting, removing from, activties from postman using the admin account
        
        #remove existing activities
        UserModule.removeExistingActivities()
        
        #remove users
        UserModule.removeUsers()
    
#FriendTests.testOneStart()

#CHECK IF THERE ARE TESTING ENTITIES STILL IN SERVER, IF SO, RUN TEST END
FriendTests.testOneEnd()


#FriendTests.testAttributesQuery()