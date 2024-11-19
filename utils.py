import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS
import pyproj

def convert_to_utm(dataset, target_epsg):
    """将栅格数据投影到UTM坐标系。"""
    source_crs = dataset.crs
    transform, width, height = calculate_default_transform(
        source_crs, target_epsg, dataset.width, dataset.height, *dataset.bounds)
    kwargs = dataset.meta.copy()
    kwargs.update({
        'crs': target_epsg,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open("temp.tif", 'w', **kwargs) as dst: #写入临时文件
        reproject(
            source=rasterio.band(dataset, 1),
            destination=rasterio.band(dst, 1),
            src_transform=dataset.transform,
            src_crs=source_crs,
            dst_transform=transform,
            dst_crs=target_epsg,
            resampling=Resampling.bilinear)


    with rasterio.open("temp.tif") as dst:
        utm_data = dst.read(1)
        return utm_data, dst.transform, dst.crs #返回UTM数据、transform和CRS


def latlon_to_utm(lat, lon, utm_crs):
    """将经纬度转换为UTM坐标."""
    transformer = pyproj.Transformer.from_crs("epsg:4326", utm_crs, always_xy=True)
    easting, northing = transformer.transform(lon, lat)
    return easting, northing