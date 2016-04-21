
#################### ham cheese production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Room(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    f_message=ccm.Model(isa='f-message',state='not_displayed')
    j_message=ccm.Model(isa='j-message',state='not_displayed')
    
    f_press=ccm.Model(isa='f-key',state='not_pressed')
    j_press=ccm.Model(isa='j-key',state='not_pressed')

    finish_message=ccm.Model(isa='finish_message',state='not_displayed')

  
    tim_location=ccm.Model(isa='location', state='Room', x='5', y='23')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def f_message(self):           # note that technically the motor module is outside the agent
        yield 2                   # but it is controlled from within the agent, i.e., it bridges the cognitive and the environment
        print "show f key message"
        self.parent.parent.f_message.state='displayed'   # self=MotorModule, parent=MyAgent, parent of parent=Subway
    def j_message(self):     
        yield 2                   # yield refers to how long the action takes, but cognition can continue while waiting for an action to complete
        print "show j key message"
        self.parent.parent.j_message.state='displayed'   # in this case the motor actions make changes to the environment objects
    def j_press(self):     
        yield 2
        print "pressing j"
        self.parent.parent.j_press.state='pressed'
    def f_press(self):     
        yield 2
        print "pressing f"
        self.parent.parent.f_press.state='pressed'


    def change_state(self, env_object, slot_value, k):
 #       k=2
        yield k
        x = eval('self.parent.parent.' + env_object)
        x.state = slot_value
        print env_object
        print slot_value
 
    def change_xx(self, env_object, slot_value, k):
 #       k=2
        yield k
        x = eval('self.parent.parent.' + env_object)
        x.xx = slot_value
        print env_object
        print slot_value

    def change_yy(self, env_object, slot_value, k):
 #       k=2
        yield k
        x = eval('self.parent.parent.' + env_object)
        x.yy = slot_value
        print env_object
        print slot_value

        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('f message')

    def respond_f(focus='f message', f_message = 'state:displayed'):
        print "tim - I'm responding to the f message"     
        focus.set('next_message')
        motor.f_press()                  # direct the motor module to do an action

    def respond_j(focus='next_message', j_message = 'state:displayed'):   # production fires off the environment directly
        print "tim - I'm responding to the j message"                                         # this is legitimate if it is assumed that the agent is... 
        focus.set('last_message')                                     # continuously and successfully monitoring the envionment
        motor.j_press()                                             # and time for monitoring is incorporated into the action time

    def stop_production(finish_message ='state:displayed'):                # wait for sue to say she is finished
        print "tim - we are done here"
        target="tim_location"
        motor.change_state(target, "home", 2)
        
        self.stop()                        # stops the whole thing, not just the agent

class MyAgent2(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('game')

    def display_f_message(focus='game'):        # slot name required for objects
        print "display - f message"
        focus.set('next_message')
        motor.f_message()

    def display_j_message(focus='next_message', f_press = 'state:pressed'):
        print "display - f message"
        focus.set('finished')
        motor.j_message()

    def finished(focus='finished', j_press = 'state:pressed'):  # wait for the action to complete before stopping
        print "display- thank you for participated in the experiment"
        print "display - finished"
        focus.set('stop')

        target="finish_message"
        motor.change_state(target, "displayed", 1)

tim=MyAgent()
sue=MyAgent2()
env=Room()
env.agent=tim
env.agent=sue

ccm.log_everything(env)

env.run()
ccm.finished()
