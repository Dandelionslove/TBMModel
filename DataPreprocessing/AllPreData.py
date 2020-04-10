from DataPreprocessing import AllUnZip
from DataPreprocessing import RF
from DataPreprocessing import AdaCost
import pandas as pd
AllUnZip()
rf = RF()
rf.RFData()
adaCost = AdaCost()
adaCost.adaCostData()