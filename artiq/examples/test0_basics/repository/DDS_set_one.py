from artiq.experiment import *


class DdsSetOne(EnvExperiment):
    """
    DDS test setting one frequency
    """
    def build(self):
        self.setattr_device("core")
        self.cpld = self.get_device("urukul0_cpld")
        self.dds = self.get_device("urukul0_ch0")

        self.setattr_argument("freq_in_MHz",
                              NumberValue(50, min=0, max=100))

    @kernel
    def run(self):
        self.core.break_realtime()
        self.cpld.init()
        self.dds.init()

        self.dds.set(self.freq_in_MHz*MHz) # amplitude?
        self.dds.sw.on()
        delay(5000*ms)
        self.dds.sw.off()

        self.core.wait_until_mu(now_mu())
