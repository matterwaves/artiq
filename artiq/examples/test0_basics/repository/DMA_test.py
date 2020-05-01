from artiq.experiment import *


class DmaTest(EnvExperiment):
    """
    DMA timing test
    Credit: m-labs.hk/artiq/manual/getting_started_core.html#direct-memory-access-dma
    """
    def build(self):
        self.setattr_device("core")
        self.dma = self.get_device("core_dma")
        self.ttl = self.get_device("ttl6")

    @kernel
    def record(self):
        with self.dma.record("pulses"):
            for i in range(50):
                self.ttl.pulse(300*ns)
                delay(300*ns)

    @kernel
    def run(self):
        self.core.reset()
        self.record()
        # prefetch the address of the DMA buffer
        # for faster playback trigger
        pulses_handle = self.dma.get_handle("pulses")
        self.core.break_realtime()
        for _ in range(1000):
            # self.core.break_realtime()
            self.dma.playback_handle(pulses_handle)
