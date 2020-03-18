from artiq.experiment import *


class TTL_timing(EnvExperiment):
    """ Basic TTL timing test
        Credit: m-labs.hk/artiq/manual/getting_started_core.html#real-time-input-output-rtio
    """
    def print_underflow(iter) -> TNone:
        print("RTIO underflow occured at iteration {}".format(iter))

    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl0.output()
        # try:
        #     for index in range(100000):
        #         delay(5*us)
        #         self.ttl0.pulse(5*us)
        # except RTIOUnderflow:
        #     print_underflow(index)
        delay(5*us)
        self.ttl0.pulse(5*us)
