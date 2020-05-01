from artiq.experiment import *


def print_underflow(iter) -> TNone:
    print("RTIO underflow occured at iteration {}".format(iter))

class TtlTiming(EnvExperiment):
    """
    TTL timing test
    Credit: m-labs.hk/artiq/manual/getting_started_core.html#real-time-input-output-rtio
    """
    def build(self):
        self.setattr_device("core")
        self.ttl = self.get_device("ttl6")

    @kernel
    def run(self):
        self.core.reset()
        try:
            for index in range(5000):
                delay(1*ms)
                self.ttl.pulse(1*ms)
        except RTIOUnderflow:
            print_underflow(index)
        self.core.wait_until_mu(now_mu())
