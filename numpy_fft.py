import sys
import os
import string
import glob
import re
import yaml
import math
import matplotlib

import numpy as np
import numpy.fft as FT
import pandas as pd

fname = raw_input('input data file name\n')
df = pd.read_csv(fname.rstrip(),header=5)
print df
