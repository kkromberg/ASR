import matplotlib.pyplot as plt
import numpy as np
import argparse

boundaries_exercise5 = [22, 116]
boundaries_exercise6 = [22, 118]
y = np.fromfile('data/probe1.ascii', sep='\n')
for energie in y:
    print energie
x = np.array(xrange(0, len(y)))

plt.plot(x, y, label="Energies")
boundaries_plt = plt.vlines(boundaries_exercise5, np.min(y), np.max(y), colors='r', label="Speech boundaries exercise 5")
boundaries_plt = plt.vlines(boundaries_exercise6, np.min(y), np.max(y), colors='g', linestyles='dashed', label="Speech boundaries exercise 6")
plt.xlabel('Time')
plt.ylabel('Energy')
plt.legend()
plt.grid(True)
plt.savefig('speechBoundaries.png')
plt.show()
