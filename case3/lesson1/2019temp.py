import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

# 数据读取及时间平均处理
ds = xr.open_dataset('2019temp.nc')
print(ds['t2m'])
temp = (ds['t2m'] - 273.15).mean(dim='time')  #把温度转换为℃并对其时间维求平均
temp.attrs['units'] = 'deg C'  #温度单位转换为℃

# 创建画图空间
proj = ccrs.PlateCarree()  #创建投影
fig = plt.figure(figsize=(9,6))  #创建页面
ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  #子图

# 设置地图属性:加载国界、海岸线、河流、湖泊。zorder是控制各地图属性在z方向上的高低,越高，其在地图上的投影就略小
ax.add_feature(cfeat.BORDERS.with_scale('50m'), linewidth=0.8, zorder=1)
ax.add_feature(cfeat.COASTLINE.with_scale('50m'), linewidth=0.6, zorder=1)
ax.add_feature(cfeat.RIVERS.with_scale('50m'), zorder=1)
ax.add_feature(cfeat.LAKES.with_scale('50m'), zorder=1)

# 设置经纬度网格点属性
gl = ax.gridlines(crs=proj,draw_labels=True,
  linewidth=1.2, color='k', alpha=0.5, linestyle='--')

# 设置经纬度格式
gl.top_labels = False  #关闭顶端标签
gl.right_labels = False  #关闭右侧标签
gl.xformatter = LONGITUDE_FORMATTER  #x轴设为经度格式
gl.yformatter = LATITUDE_FORMATTER  #y轴设为纬度格式
gl.xlocator=ticker.FixedLocator(np.arange(-180,181,30))
gl.ylocator=ticker.FixedLocator(np.arange(-90,91,30))

# 设置colorbar
cbar_kwargs = {
   'orientation': 'horizontal',
   'label': '2m temperature (℃)',
   'shrink': 0.6,
    'pad': 0.05,
   'ticks': np.arange(-30,30+5,5)
}
# 画图
levels = np.arange(-30,30+1,1)
temp.plot.contourf(ax=ax, levels=levels, cmap='Spectral_r',
    cbar_kwargs=cbar_kwargs, transform=proj)

# 可以设定范围，显示中国区域的地图
# ax.set_xlim(60,140)
# ax.set_ylim(0,60)

plt.tight_layout()
plt.savefig('2019temp.png',dpi=900,bbox_inches='tight')
plt.show()