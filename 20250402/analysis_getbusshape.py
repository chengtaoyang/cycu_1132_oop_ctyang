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

    import folium

    # Create a Folium map centered on the data
    center = gdf.geometry.iloc[0].centroid.coords[0][::-1]  # (lat, lon)
    m = folium.Map(location=center, zoom_start=13)

    # Add LineString routes to the map
    for _, row in gdf.iterrows():
        x_array = row.geometry.xy[0]
        y_array = row.geometry.xy[1]
        points = list(zip(y_array, x_array))
        folium.PolyLine(locations=points, tooltip=row['UniRouteId']).add_to(m)

    # Save to HTML
    m.save("bus_routes_map.html")

except Exception as e:

    print("Error processing the file:", e)
