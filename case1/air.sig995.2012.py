# load library
import numpy as np
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
from palettable.colorbrewer.diverging import RdBu_11_r
import netCDF4 as nc

# read NetCDF file
fn = 'air.sig995.2012.nc'
data = nc.Dataset(fn, 'r') # 默认为读文件，此处 'r' 可省略
print(data['air'])
# 读取相关变量
lat = data.variables['lat'][:].data
lon = data.variables['lon'][:].data
time = data.variables['time'][:].data
air = data.variables['air'][:].data

# 添加数据循环，以防止在0和360时出现白色条状
# 添加数据循环和不添加数据循环的效果见后文两张图
cycle_air, cycle_lon = add_cyclic_point(air, coord=lon)
cycle_LON, cycle_LAT = np.meshgrid(cycle_lon, lat)

projection = ccrs.PlateCarree() # 设置投影
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(projection=projection))

con = ax.contourf(cycle_LON, cycle_LAT, cycle_air[0, ...],
                 np.arange(220, 321), cmap=RdBu_11_r.mpl_colormap)

ax.coastlines(linewidth=1) # 添加海岸线
ax.set_xticks(np.arange(-180, 181, 60), crs=projection)
ax.set_yticks(np.arange(-90, 91, 30), crs=projection)

# 设置 ticklabels 格式
lon_formatter = LongitudeFormatter(number_format='.0f',
                                  degree_symbol='°',
                                  dateline_direction_label=True)
lat_formatter = LatitudeFormatter(number_format='.0f',
                                 degree_symbol='°')

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.tick_params(labelsize=10)

# shrink 控制 colorbar 长度，pad 控制colorbar和图的距离
cb = fig.colorbar(con, shrink=0.5, pad=0.02)
ax2=cb.ax
ax2.set_ylabel('Air',fontsize=12)

# 调整 ticklabels
cb.set_ticks(np.arange(220, 321, 20))
cb.set_ticklabels(np.arange(220, 321, 20))

cb.ax.tick_params(direction='in', length=5,labelsize=8) # 控制 colorbar tick

# 保存文件, dpi用于设置图形分辨率, bbox_inches 尽量减小图形的白色区域

plt.savefig('test.png',dpi=900,bbox_inches='tight')
plt.show()