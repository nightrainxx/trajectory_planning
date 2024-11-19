# src/data_io.py
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS
import geopandas as gpd
import numpy as np
from shapely.geometry import mapping
from utils import convert_to_utm, latlon_to_utm


def load_dem(dem_file, target_epsg):
    """加载DEM数据并转换为UTM坐标系。"""
    with rasterio.open(dem_file) as src:
        dem_utm, transform_utm, crs_utm = convert_to_utm(src, target_epsg)
        return dem_utm, transform_utm, crs_utm

def load_roads(road_file, dem_transform, dem_crs, target_epsg):
    """加载道路数据并转换为UTM坐标系，然后栅格化。"""
    roads_gdf = gpd.read_file(road_file)
    # 转换道路数据到UTM坐标系
    roads_gdf = roads_gdf.to_crs(dem_crs)  # 先确保道路数据和DEM是同一个坐标系
    roads_gdf = roads_gdf.to_crs(target_epsg)


    # 栅格化道路
    roads_raster = rasterize_roads(roads_gdf, dem_transform, dem_crs, target_epsg)
    return roads_gdf, roads_raster

def rasterize_roads(roads_gdf, dem_transform, dem_crs, target_epsg):
    """栅格化道路数据。"""
    with rasterio.open("temp.tif") as dem_raster:
        # 使用与DEM相同大小和变换参数的空栅格
        meta = dem_raster.meta.copy()
        meta.update(dtype=rasterio.uint8, count=1, nodata=0)

        with rasterio.open("temp_roads.tif", 'w', **meta) as out:
            # 使用栅格化函数
            out_array = np.zeros((meta['height'], meta['width']), dtype=np.uint8)

            # 使用 roads_gdf 的 geometry 列进行栅格化
            shapes = ((geom, 1) for geom in roads_gdf.geometry)

            burned = rasterio.features.rasterize(shapes=shapes, fill=0, out=out_array, transform=dem_raster.transform)
            out.write_band(1, burned)
    with rasterio.open("temp_roads.tif") as roads_raster:
        roads_array = roads_raster.read(1)
        return roads_array

def load_data(dem_file, road_file, target_epsg):
    """加载DEM和道路数据，并进行预处理。"""
    dem_utm, transform_utm, crs_utm = load_dem(dem_file, target_epsg)
    roads_gdf, roads_raster = load_roads(road_file, transform_utm, crs_utm, target_epsg)
    resolution = transform_utm[0]
    bounds_utm = rasterio.transform.array_bounds(dem_utm.shape[0], dem_utm.shape[1], transform_utm)
    return dem_utm, transform_utm, crs_utm, roads_raster, resolution, bounds_utm, dem_utm.shape


#  示例用法 (在main.py中):
# from data_io import load_data

# dem_utm, transform_utm, crs_utm, roads_raster, resolution, bounds_utm = load_data("data/dem.tif", "data/roads.shp", 32636)