#################### ham cheese production DM model ###################

# this builds on the production model
# two productions are added
# the first requests that the declarative memory module retrieves the condiment that the cutomer ordered
# which is stored in declarative memory
# the second production fires when this has happened


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent


class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    DM.add('fight_action:parry')              # put a chunk into DM
    focus.set('fight hitman_jab')
        
    def hitman_jab(focus='fight hitman_jab'):   
        print "He threw a jab at me!"         
        focus.set('do_fight_action')

    def fight_action_recall(focus='do_fight_action'):
        print "recalling what to do if a hitman throws a jab"
        DM.request('fight_action:?')                # retrieve a chunk from DM into the DM buffer
        focus.set('fight fight_action')         # ? means that slot can match any content

    def fight_action(focus='fight fight_action', DMbuffer='fight_action:?fight_action'):  # match to DMbuffer as well
        print "I recall he threw......."                                 # put slot 2 value in ?condiment
        print fight_action             
        print "i have deflected his punch"
        focus.set('fight cross')

    def cross(focus='fight cross'):        
        print "I got him with the cross!"
        print "He is out for the count"
        focus.set('stop')


    def stop_production(focus='stop'):
        self.stop()


tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
