from artiq.experiment import *


class core_reset(EnvExperiment):
    """
    Core reset
    Runs only the instruction core.reset()
    """
    def build(self):
        self.setattr_device("core")

    @kernel
    def run(self):
        self.core.reset()
