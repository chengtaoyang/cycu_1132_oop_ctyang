import geopandas as gpd

def main():
    shapefile_path = "data/busstop/busstop.shp"
    busstops = gpd.read_file(shapefile_path)
    # set the coordinate reference system to EPSG:4326
    busstops = busstops.set_crs(epsg=4326)


    busstops.to_file("data/taipei_city_bus_stop.gpkg", driver="GPKG")
if __name__ == "__main__":
    main()