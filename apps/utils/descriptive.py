import pandas
import statistics
import scipy
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

class Descriptive:

	def pdread(pfname):
		pdf = pandas.read_csv(pfname, header=0)
		return pdf
    