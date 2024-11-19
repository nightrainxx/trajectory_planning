import geopandas as gpd
import rasterio
# 原始数据均是在 espg4326投影系下完成的
# DEM 的边界信息 (西, 南, 东, 北): BoundingBox(left=34.0, bottom=47.69999999999998, right=36.0, top=49.0)
# 使用UTM 32N 区域
shapefile_path = r"/data/path_to_your_clipped_shapefile.shp"

try:
    gdf = gpd.read_file(shapefile_path)
    crs = gdf.crs
    epsg_code = crs.to_epsg()  # 获取 EPSG 代码

    if epsg_code is None:
        print("警告：无法从 Shapefile 中获取 EPSG 代码。请检查 Shapefile 是否有效。")
    else:
        print(f"Shapefile 的投影信息：EPSG:{epsg_code}")

except FileNotFoundError:
    print(f"错误：未找到 Shapefile 文件：{shapefile_path}")
except Exception as e:
    print(f"读取 Shapefile 失败：{e}")

dem_file_path = r"/data/gebco_2024_n49.0_s47.7_w34.0_e36.0.tif"

try:
    with rasterio.open(dem_file_path) as src:
        crs = src.crs
        print(f"DEM 文件的投影信息：{crs}")  # 输出投影信息

except FileNotFoundError:
    print(f"错误：未找到 DEM 文件：{dem_file_path}")
except Exception as e:
    print(f"读取 DEM 文件失败：{e}")

try:
    with rasterio.open(dem_file_path) as src:
        bounds = src.bounds
        print(f"DEM 的边界信息 (西, 南, 东, 北): {bounds}")
except FileNotFoundError:
    print(f"错误：未找到 DEM 文件：{dem_file_path}")
except Exception as e:
    print(f"读取 DEM 文件失败：{e}")