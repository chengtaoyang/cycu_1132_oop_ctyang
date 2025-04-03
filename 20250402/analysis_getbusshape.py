import pandas as pd
import geopandas as gpd
from shapely import wkt
import json

# 嘗試將內容讀取為 JSON 並轉換為 GeoDataFrame
try:
    # 讀取 JSON 檔案
    with open("GetBusShape", "r", encoding="utf-8") as file:
        content = file.read()

    # 先將字串內容處理為 JSON 格式
    data = json.loads(content)
    
    # 轉換為 DataFrame
    df = pd.DataFrame(data)
    
    # 將 'wkt' 欄位轉換為幾何圖形
    df["geometry"] = df["wkt"].apply(wkt.loads)
    
    # 建立 GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    
    # 儲存為 GeoJSON 檔案
    gdf.to_file("bus_route.geojson", driver="GeoJSON")

    # 儲存為 gpkg 檔案
    gdf.to_file("taipei_city_bus_route.gpkg", driver="GPKG")
except Exception as e:
    str(e)
