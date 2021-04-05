from pysolver import Constants
from pysolver import Flags
from pysolver import Settings
from pysolver import Variable


class Global:
    def __init__(self):
        self.SystemVariables = Variable.Variable()
        self.SystemSettings = Settings.Settings()
        self.SystemFlags = Flags.Flags()
        self.SystemConstants = Constants.Constants()
        None