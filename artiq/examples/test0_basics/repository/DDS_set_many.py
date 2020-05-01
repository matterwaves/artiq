from artiq.experiment import *


class DDSSetMany(EnvExperiment):
    """
    DDS test setting many frequencies
    Credit: github.com/m-labs/.../examples/kc705_nist_clock/repository/dds_test.py
    """
    def build(self):
        self.setattr_device("core")
        self.cpld = self.get_device("urukul0_cpld")
        self.dds = self.get_device("urukul0_ch0")

    @kernel
    def run(self):
        self.core.reset()
        self.cpld.init()
        self.dds.init()
        self.core.break_realtime()

        self.dds.sw.on()
        for i in range(10000):
            delay(1*ms)
            self.dds.set(10*MHz + 4*i*kHz) # amplitude?
        self.dds.sw.off()
