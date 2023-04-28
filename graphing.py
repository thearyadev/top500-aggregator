import matplotlib.pyplot as plt
import numpy as np

import database

db = database.DatabaseAccess("data/data.db")
data = db.get_all_records(2)
r = list()
for a in data:
    r.append(a.games)
print(len(r))
print(min(r))
print(max(r))

x = np.array(r)

plt.scatter(x, np.sort(x))
plt.show()
