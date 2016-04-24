# -CGSC6004W-Winter-2016-class-mini-assignments
#################### ham cheese production model ###################

# this is the simplest type of act-r model
# it uses only the production system and one buffer
# the buffer represents the focus of thought
# we call it the focus buffer but it is often called the goal buffer
# productions fire if they match the focus buffer
# each production changes the contents of focus buffer so a different production will fire on the next cycle


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

    def init():
        focus.set('goal:read textmessage:power_button')

    def power_button(focus='goal:read textmessage:power_button'):     # if focus buffer has this chunk then....
        print "I have press the powe button"                            # print
        focus.set('goal:open texting app:swipe_up_lockscreen')                   # change chunk in focus buffer

    def swipe_up_lockscreen(focus='goal:read textmessage:swipe_up_lockscreen'):          # the rest of the productions are the same
        print "I have unlocked the lockscreen"                         # but carry out different actions
        focus.set('goal:open texting app: press_icon')

    def press_icon(focus='goal:read textmessage: press_icon'):
        print "I have press the text icon"
        focus.set('goal: read textmessage: read_texts')

    def read_texts(focus='goal: read textmessage:read_texts'):
        print "I have read the text"
        print "I have read the new text message"
        focus.set('goal:stop')   

    

    def stop_production(focus='goal:stop'):
        self.stop()                                           # stop the agent

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

