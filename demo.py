# Example of data analysis functions
import mda.tutorial.pandastut as pdtut

viewer = pdtut.Viewer()

viewer.all()

viewer.head(3)

viewer.describe()

# Package management
import mda.tutorial.tut as tut
from mda.tutorial import * #Adds times2 and pandastut 
print tut.times2(5)

# Read datasets from website for 'Elements of Statistical Learning'
from mda.read.esl import data
ds = data.read( 'prostate', '\t')
ds.describe()
