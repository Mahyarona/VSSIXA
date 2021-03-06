# Vegetation Spectral-Structral Information eXtraction Algorithm (VSSIXA):

To analyze and extract 3D information from the point cloud dataset and spectral information from the high-resolution imagery, a new algorithm called Vegetation Structural-Spectral Information eXtraction Algorithm (VSSIXA), using Python and ArcGIS Pro libraries, was developed. The code of this algorithm is available at (https://github.com/Mahyarona/VSSIXA).  Fig 1 shows components of VSSIXA in a flowchart diagram. 

| ![A workflow of proposed VSSIXA algorithm \label{fig:6-1}](https://github.com/Mahyarona/VSSIXA/blob/master/Flowchart_VSSIXA.png) | 
|:--:| 
| *Fig 1. A workflow of proposed VSSIXA algorithm* |

<!---![A workflow of proposed VSSIXA algorithm](https://github.com/Mahyarona/VSSIXA/blob/master/Flowchart_VSSIXA.png)-->

As shown in Fig 1, The VSSIXA algorithm requires a point cloud dataset as the primary input and a shapfile, optical and thermal imagery, and a ground point as the secondary inputs. In the first step, a vine spacing grid shapefile is read and point cloud, ground points, and UAV imagery are clipped for each grid of the shapefile. In this step, the average of the UAV imagery for each band and for each grid, and consequently the partitioning of Tr into soil temperature (Ts) and canopy temperature (Tc) are executed and stored. In this step, Ts and Tc estimations are by-products of VSSIXA. Next, clipped ground points and point cloud datasets are converted to individual point datasets, Red (R), Green (G), Blue (B), near-infrared (NIR), and Tr bands from UAV imagery along with z values from ground points are assigned to each single point cloud based on nearest distance, and relative height (Point cloud z - Ground z) is calculated. Therefore, the Attribute Table of each point constitutes point cloud height, ground height, relative height, RGB, NIR, and thermal information. Next, the individual points are separated into vegetation and non-vegetation points using a VI threshold (e.g. NDVI>0.6), and volume, surface area, height, and the average of Tr and optical bands for vegetation points using a triangulated irregular network (TIN) are calculated and appended into the Attribute Table. In the last stage, vegetation points are separated into vine canopy and cover crop points based on a relative height threshold (0.5m in this study) and derived structural and spectral information for vine and cover crop points is separately recalculated. Because structural and spectral information for each point has been extracted and geographical information for those single points has been accessed, a profile of information, such as average height, vine temperature, and VIs, can be extracted. VSSIXA is able to extract and store these profiles in a Comma-separated values (CSV) format.       

# VSSIXA-I and VSSIXA-II:

 VSSIXA is coded in two different versions, VSSIXA-I and VSSIXA-II. VSSIXA-I requires only a point cloud dataset, while VSSIXA-II requires both point cloud data and LiDAR ground points. In VSSIXA-I, after appending multi-spectral information to each point in each grid, the point cloud is classified into the ground and non-ground classes based on an NDVI threshold. The relative height is calculated based on Point Cloud z and the minimum value of ground point heights. Therefore, the structural information is calculated between TIN created from non-ground points and a surface with height zero. If there are no multi-spectral data to separate ground points from non-ground points or if a grid has no ground points (e.g., fully covered by vegetation), VSSIXA-I considers the minimum z value from all points to calculate relative height. In contrast, the classified ground points exist for VSSIXA-II, due to LiDAR penetration into vegetation and detection of ground. Therefore, z values from LiDAR ground points are affixed to the point cloud from a spatial perspective (e.g., closest distance) to calculate relative height and then, similar to VSSIXA-I, the structural information is calculated. Since VSSIXA-I assigns one value (minimum z value of ground points) to non-ground points in each grid, it assumes that the slope of the ground surface in each grid is close to zero. Thus, VSSIXA-I is appropriate for flat terrain,  even though it requires only a point cloud dataset. In contrast, because VSSIXA-II assigns ground z values to each point, the impact of slope is considered, albeit it requires both point cloud and LiDAR ground point datasets (Fig 2). 

| ![Differences between VSSIXA-I and VSSIXA-II determination of ground elevation and canopy height](https://github.com/Mahyarona/VSSIXA/blob/master/VSSIXA.png) | 
|:--:| 
| *Fig 2. Differences between VSSIXA-I and VSSIXA-II determination of ground elevation and canopy height* |


The difference between VSSIXA-I and VSSIXA-II in relative height calculation may lead to differences in the estimation of canopy volume. It is expected that VSSIXA-II estimates higher values for canopy volume compared to VSSIXA-I. In contrast, there should not be a significant difference between surface area or projected surface area estimated by VSSIXA-I and VSSIXA-II (Fig 3). Thus, if all the structural parameters are used to evaluate the relationship between LAI and VSSIXA outputs, either VSSIXA-I or VSSIXA-II must be employed for the entire study area due to inconsistency between canopy volume and height estimated by VSSIXA-I and -II unless the slope of each grid can be considered as zero (similar to the current study area).

| ![Differences between VSSIXA-I and VSSIXA-II in estimation of canopy surface area, projected surface area, volume and average height](https://github.com/Mahyarona/VSSIXA/blob/master/VSSIXA_Sub02.png) | 
|:--:| 
| *Fig 3. Differences between VSSIXA-I and VSSIXA-II in estimation of canopy surface area, projected surface area, volume and average height* |

# Citation:
If you use VSSIXA in any academic work then you *must* cite the following papers:

Aboutalebi, M., Torres-Rua, A., McKee, M., Kustas, W. P., Nieto, H., Alsina, M., White, A., Prueger, J., McKee, L., Alfieri, J., Hipps, L., Coopmans, C., and Dokoozlian, N. "Incorporation of Unmanned Aerial Vehicle (UAV) Point Cloud Product into Remote Sensing Evapotranspiration Models", Remote Sensing, 2019.


In BibTeX format:

@Article{Aboutalebi2019,
  Title                    = {Incorporation of Unmanned Aerial Vehicle (UAV) Point Cloud Product into Remote Sensing Evapotranspiration Models},
  Author                   = {M. Aboutalebi and A. Torres-Rua and M. McKee and W. P. Kustas and H. Nieto and M. Alsina and A. White and J. Prueger and L. McKee and J. Alfieri and L. Hipps and C. Coopmans and N. Dokoozlian},
  Journal                  = {Remote Sensing},
  Year                     = {2019},
  Number                   = {},
  Pages                    = {},
  Volume                   = {}
}
