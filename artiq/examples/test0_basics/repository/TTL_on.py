from artiq.experiment import *


class TTL_on(EnvExperiment):
    """
    TTL on
    Test 1. whether the TTL channel value gets reset after the experiment exits
         2. whether there can be multiple handles, or references, to the same channel
    """
    def build(self):
        self.setattr_device("core")
        # this_switch and ttl6 refer to the same TTL channel
        self.setattr_device("this_switch")
        self.setattr_device("ttl6")

        # whether to turn off the TTL at the end of the experiment
        self.setattr_argument("off", BooleanValue(default=True))

    @kernel
    def run(self):
        print(self.this_switch is self.ttl6) # prints True!

        self.core.reset()
        delay(1000*ms)
        self.this_switch.on()
        delay(500*ms)

        if self.off:
            self.ttl6.off()

        self.core.wait_until_mu(now_mu())
