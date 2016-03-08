import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Kitchen(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    spoon=ccm.Model(isa='spoon',location='left_pocket')
    spatula=ccm.Model(isa='spatula',location='right_pocket')
    small_pot=ccm.Model(isa='small_pot',location='on_floor_right')
    larg_pot=ccm.Model(isa='larg_pot',location='on_floor_left')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def grab_spoon(self):           # note that technically the motor module is outside the agent
        yield 2                   # but it is controlled from within the agent, i.e., it bridges the cognitive and the environment
        print "Pull spoon out of left pocket"
        self.parent.parent.spoon.location='left_hand'    # self=MotorModule, parent=MyAgent, parent of parent=Subway
    def grab_spatula(self):     
        yield 2                   # yield refers to how long the action takes, but cognition can continue while waiting for an action to complete
        print "Pull spatula out of right pocket"
        self.parent.parent.spatula.location='right_hand'   # in this case the motor actions make changes to the environment objects
    def Hit_small_pot(self):     
        yield 2
        print "striking small pot"
        self.parent.parent.small_pot.location='floor_right'
    def Hit_large_pot(self):     
        yield 2
        print "striking large pot"
        self.parent.parent.larg_pot.location='floor_left'
        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('x spoon')

    def spoon(focus='x spoon'):
        print "The spoon is in my right hand"     
        focus.set('x spatula')
        motor.grab_spoon()                  # direct the motor module to do an action

    def spatula(focus='x spatula', spoon='location:left_hand'):   # production fires off the environment directly
        print "The spatula is in my left hand"                                         # this is legitimate if it is assumed that the agent is... 
        focus.set('x small_pot')                                     # continuously and successfully monitoring the envionment
        motor.grab_spatula()                                             # and time for monitoring is incorporated into the action time

    def small_pot(focus='x small_pot', spatula='location:right_hand'):        # slot name required for objects
        print "smack goes the small pot"
        focus.set('x larg_pot')
        motor.Hit_small_pot()

    def larg_pot(focus='x larg_pot', small_pot='location:floor_right'):
        print "smack goes the larrg pot"
        focus.set('stop')
        motor.Hit_large_pot()

    def stop_production(focus='stop', larg_pot='location:floor_left'):  # wait for the action to complete before stopping
        print "That was a mad beat"
        self.stop()


tim=MyAgent()
env=Kitchen()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()

