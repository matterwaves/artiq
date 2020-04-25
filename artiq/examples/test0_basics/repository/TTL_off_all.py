from artiq.experiment import *


class TTL_off_all(EnvExperiment):
    """
    Set all TTL channels to off
    """
    def build(self):
        self.setattr_device("core")
        self.ttls = [self.get_device("ttl" + str(i)) for i in range(4, 40)]

    @kernel
    def run(self):
        self.core.reset()
        delay(1*ms)
        for ttl in self.ttls:
            ttl.off()
            delay(1*ms)
        # self.core.wait_until_mu(now_mu())
