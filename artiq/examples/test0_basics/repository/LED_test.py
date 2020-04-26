from artiq.experiment import *


class LED_test(EnvExperiment):
    """
    LED test
    Credit: m-labs.hk/artiq/manual/getting_started_core.html#real-time-input-output-rtio
    """
    def build(self):
        self.setattr_device("core")
        self.led = self.get_device("led0")

    @kernel
    def run(self):
        self.core.reset()
        delay(500*ms)
        for index in range(1000):
            self.led.on()
            delay(500*ms)
            self.led.off()
        self.core.wait_until_mu(now_mu())
