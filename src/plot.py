import matplotlib.pyplot as plt
import numpy as np
import sys

x,y = np.loadtxt(sys.argv[1],delimiter=',',unpack = True)
plt.xlabel('Generation')

plt.ylabel('No. of prey offspring protected')


plt.title('No of prey offspring protected')


plt.plot(x,y,label="Average offspring protected")


plt.show()
