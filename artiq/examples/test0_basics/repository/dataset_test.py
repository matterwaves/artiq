from artiq.experiment import *
import numpy as np
import time

# no hardware is required to run this test
class DatasetTest(EnvExperiment):
    """
    Dataset test saving and retrieving
    Test 1. in the same run/experiment, with archive=False,
            saving dataset in folder and later retrieving it in analyze()
         2. in a different run/experiment, with archive=False previously,
            retrieving dataset from folder
         3. set datatset as an attribute using setattr_dataset()
         4. after archive=True, viewing in artiq_browser the dataset in folder
         5. creating applet with ccb.issue() and plotting in GUI in real time
         6. making a GUI argument an integer by setting its ndecimals=0, step=1
    """
    def build(self):
        self.setattr_device("ccb")

        self.setattr_argument("len", NumberValue(20, min=1, max=100,
                                                 ndecimals=0, step=1)) # integer
        self.setattr_argument("to_initialize", BooleanValue(default=True))
        self.setattr_argument("to_archive", BooleanValue(default=False))

    def run(self):
        if self.to_initialize:
            # the '.' separates folders, see
            # https://m-labs.hk/artiq/manual/faq.html#organize-datasets-in-folders
            self.set_dataset("len", self.len,
                             persist=True, archive=self.to_archive)
            self.set_dataset("good_folder.len", self.len,
                             persist=True, archive=self.to_archive)
            self.set_dataset("best_folder.best_xs",
                             np.full(self.len, np.nan),
                             persist=True, archive=self.to_archive)
            self.set_dataset("best_folder.best_ys",
                             np.full(self.len, np.nan),
                             persist=True, archive=self.to_archive)

            self.ccb.issue("create_applet", "set_dataset_test",
                           "${artiq_applet}plot_xy "
                           "best_folder.best_ys --x best_folder.best_xs")
        else:
            # in a different run, retrieve datasets from folders and set datasets
            self.setattr_dataset("len") # setattr_dataset("good_folder.len") does not work
            self.set_dataset("new_folder.xs", self.get_dataset("best_folder.best_xs"),
                             persist=True, archive=True)
            self.set_dataset("new_folder.ys", self.get_dataset("best_folder.best_ys"),
                             persist=True, archive=True)

            self.ccb.issue("create_applet", "get_dataset_test",
                           "${artiq_applet}plot_xy "
                           "new_folder.ys --x new_folder.xs")

        if self.to_initialize:
            for i in range(self.len):
                self.mutate_dataset("best_folder.best_xs", i, i)
                self.mutate_dataset("best_folder.best_ys", i, np.sqrt(i))
                time.sleep(0.1)
        else:
            time.sleep(2)
            for i in range(self.len):
                self.mutate_dataset("new_folder.xs", i, i)
                self.mutate_dataset("new_folder.ys", i, i**2)
                time.sleep(0.1)

    def analyze(self):
        if self.to_initialize:
            # in the same run, retrieve dataset from folder
            self.get_dataset("best_folder.best_xs")
