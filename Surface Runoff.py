# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-01-13 12:53:21
"""
import arcpy

def SurfaceRunoff():  # Surface Runoff

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("ImageAnalyst")

    Manual_Catchment = "Catchment_Buffer"
    DEM = arcpy.Raster("Terrain")
    Pour_Point = arcpy.Raster("Pour_points")

    # Process: Fill (Fill) (sa)
    Filled = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\Filled"
    Fill = Filled
    with arcpy.EnvManager(cellSize="10", extent="1456128.8199 6011571.9574 1469269.3117 6018999.2532"):
        Filled = arcpy.sa.Fill(in_surface_raster=DEM, z_limit=None)
        Filled.save(Fill)


    # Process: Flow Direction (Flow Direction) (sa)
    FlowDir = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\FlowDir"
    Flow_Direction = FlowDir
    FlowDrop = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\FlowDrop"
    with arcpy.EnvManager(cellSize="10"):
        FlowDir = arcpy.sa.FlowDirection(in_surface_raster=Filled, force_flow="NORMAL", out_drop_raster=FlowDrop, flow_direction_type="D8")
        FlowDir.save(Flow_Direction)

        FlowDrop = arcpy.Raster(FlowDrop)

    # Process: Flow Length (Flow Length) (sa)
    FlowLen = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\FlowLen_Flow1"
    Flow_Length = FlowLen
    FlowLen = arcpy.sa.FlowLength(in_flow_direction_raster=FlowDir, direction_measurement="DOWNSTREAM", in_weight_raster="")
    FlowLen.save(Flow_Length)


    # Process: Flow Accumulation (Flow Accumulation) (sa)
    FlowAcc = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\FlowAcc"
    Flow_Accumulation = FlowAcc
    with arcpy.EnvManager(cellSize="1"):
        FlowAcc = arcpy.sa.FlowAccumulation(in_flow_direction_raster=FlowDir, in_weight_raster="", data_type="FLOAT", flow_direction_type="D8")
        FlowAcc.save(Flow_Accumulation)


    # Process: Watershed (Watershed) (sa)
    Watershed_DEM = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\Watershed_DEM"
    Watershed = Watershed_DEM
    with arcpy.EnvManager(cellSize="10"):
        Watershed_DEM = arcpy.sa.Watershed(in_flow_direction_raster=FlowDir, in_pour_point_data=Pour_Point, pour_point_field="Value")
        Watershed_DEM.save(Watershed)


    # Process: Raster to Polygon (Raster to Polygon) (conversion)
    Automatic_catchment = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\RasterT_Watersh1"
    arcpy.conversion.RasterToPolygon(in_raster=Watershed_DEM, out_polygon_features=Automatic_catchment, simplify="SIMPLIFY", raster_field="Value", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Clip Raster (Clip Raster) (management)
    FlowAcc_clip = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\FlowAcc_Clip"
    arcpy.management.Clip(in_raster=FlowAcc, rectangle="1456128.8199 6011571.9574 1469268.8199 6019001.9574", out_raster=FlowAcc_clip, in_template_dataset=Automatic_catchment, nodata_value="3.4e+38", clipping_geometry="NONE", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    FlowAcc_clip = arcpy.Raster(FlowAcc_clip)

    # Process: Reclassify (Reclassify) (sa)
    FlowAcc_RC = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\Reclass_Flow1"
    Reclassify = FlowAcc_RC
    FlowAcc_RC = arcpy.sa.Reclassify(in_raster=FlowAcc_clip, reclass_field="VALUE", remap="", missing_values="DATA")
    FlowAcc_RC.save(Reclassify)


    # Process: Set Null (Set Null) (sa)
    Raster_stream = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\SetNull_Recl1"
    Set_Null = Raster_stream
    Raster_stream = arcpy.sa.SetNull(in_conditional_raster=FlowAcc_RC, in_false_raster_or_constant=FlowAcc_RC, where_clause="")
    Raster_stream.save(Set_Null)


    # Process: Stream to Feature (Stream to Feature) (sa)
    Vector_stream = "C:\\Users\\max_a\\Documents\\ArcGIS\\Projects\\Lab Surface Runoff\\Lab Surface Runoff.gdb\\StreamT_SetNull1"
    arcpy.sa.StreamToFeature(in_stream_raster=Raster_stream, in_flow_direction_raster=FlowDir, out_polyline_features=Vector_stream, simplify="SIMPLIFY")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\max_a\Documents\ArcGIS\Projects\Lab Surface Runoff\Lab Surface Runoff.gdb", workspace=r"C:\Users\max_a\Documents\ArcGIS\Projects\Lab Surface Runoff\Lab Surface Runoff.gdb"):
        SurfaceRunoff()
