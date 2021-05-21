import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

ds = xr.open_dataset('example.ncf')

# 两种方式转换为numpy数组类型

ef =ds['EF_ISOP'].data

print(ds)
print(ef)
print('*'*20)
ef2 = np.squeeze(ef)
print(ef2)
plt.contourf(ef2,cmap='rainbow')
plt.colorbar()
np.savetxt('ef.txt',ef2)
plt.show()