from artiq.experiment import *


class TTL_onoff_all(EnvExperiment):
    """
    Set all TTL channels to on/off
    """
    def build(self):
        self.setattr_device("core")
        self.ttls = [self.get_device("ttl" + str(i)) for i in range(4, 40)]

        self.setattr_argument("on", BooleanValue(default=True))

    @kernel
    def run(self):
        self.core.reset()
        delay(1*ms)
        if self.on:
            for ttl in self.ttls:
                ttl.on()
                delay(1*ms)
        else:
            for ttl in self.ttls:
                ttl.off()
                delay(1*ms)
        # self.core.wait_until_mu(now_mu())
