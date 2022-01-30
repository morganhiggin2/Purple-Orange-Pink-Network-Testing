#can just run this file and put call to test at top if wanting to just run tests and avoid command line

from user_module import UserModule

#file for query tests
class FriendTests:
    #test custom attributes
    def testAttributesQuery():
        #init
        UserModule.init()
        
        #create users
        UserModule.createUsers(1)
        
        #add attributes
        UserModule.addFriendAttribute(0, "hello")
        
        #call query
        
        #remove users
        UserModule.removeUsers()
        
        return
    
    def testOneStart(): 
        #init
        UserModule.init()
        
        #create users
        UserModule.createUsers(10)
        
        #save incase the next commands crash
        UserModule.saveUsers()
        
        #add attributes
        UserModule.makeRandomNumAttributes(5)
        
        #make query
        #UserModule.makeFriendSearchQueryRandom(2000, 2, 2)
        
        #save users
        UserModule.saveUsers()
        
    def testOneEnd():
        #load users
        UserModule.loadExistingUsers()
        
        #remove users
        UserModule.removeUsers()
    
FriendTests.testOneEnd()