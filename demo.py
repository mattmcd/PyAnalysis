# Example of data analysis functions
import mda.tutorial.pandastut as pdtut

viewer = pdtut.Viewer()

viewer.all()

viewer.head(3)

viewer.describe()

# Package management
import mda.tutorial as tut
from mda.tutorial import * #Adds times2 and pandastut 
print tut.times2.times2(5)
