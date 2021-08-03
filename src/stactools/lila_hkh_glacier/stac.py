import logging
import os
import pystac
import pytz
import rasterio
import rasterio.features
import rasterio.warp

from typing import Any, Dict
from datetime import datetime
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.label import LabelExtension, LabelType
from stactools.lila_hkh_glacier.constants import (
    FUSED_LICENSE, FUSED_LICENSE_LINK, LABEL_DESCRIPTION, SLICE_LICENSE,
    SLICE_LICENSE_LINK, LILA_HKH_GLACIER_FUSED_BANDS,
    LILA_HKH_GLACIER_FUSED_ID, LILA_HKH_GLACIER_FUSED_DESCRIPTION,
    LILA_HKH_GLACIER_FUSED_TITLE, LILA_HKH_GLACIER_SLICE_ID,
    LILA_HKH_GLACIER_SLICE_DESCRIPTION, LILA_HKH_GLACIER_PROVIDER,
    LILA_HKH_GLACIER_SLICE_TITLE, START_DATETIME, END_DATETIME)
from stactools.lila_hkh_glacier import utils
from shapely.geometry import MultiPolygon, Polygon, box, mapping
from shapely.ops import transform

logger = logging.getLogger(__name__)


def parse_datetime(path: str) -> datetime:
    """Parses datetime object from path, where filename must contain YYYYMMDD after second underscore.

    Args:
        path (str): file path. Filename must contain YYYYMMDD after second underscore.

    Returns:
        datetime: datetime object
    """
    utc = pytz.utc
    split_path = os.path.basename(path).split("_")
    path_date = datetime.strptime(split_path[2], "%Y%m%d")
    dataset_datetime = utc.localize(path_date)
    return dataset_datetime


def get_proj(dataset: rasterio.io.DatasetReader) -> Dict[str, Any]:
    """Extract projection extension parameters from dataset

    Args:
        dataset (rasterio.io.DatasetReader): dataset object

    Returns:
        dict: dictionary of projection extension parameters
    """
    proj_epsg = dataset.crs.to_epsg()
    proj_shape = (dataset.profile["height"], dataset.profile["width"])
    proj_transform = dataset.profile["transform"]
    bounds = dataset.bounds
    proj_bbox = [*bounds]

    return {
        "epsg": proj_epsg,
        "shape": proj_shape,
        "transform": proj_transform,
        "bbox": proj_bbox
    }


def create_slice_item(feature: Dict[str, Any], destination: str,
                      epsg_code: int) -> pystac.Item:
    """Creates a STAC item for a LILA HKH Glacier Mapping labelled slice image feature.

    Args:
        feature (dict): Path to provider metadata.
        destination (str): Path to output STAC item directory.
        epsg_code (int): EPSG code for feature's coordinate reference system

    Returns:
        pystac.Item: STAC Item object.
    """

    transformer = utils.create_transformer(epsg_code)

    split_img_slice = os.path.splitext(
        os.path.basename(feature["properties"]["img_slice"]))[0].split("_")
    id = "_".join([split_img_slice[1], split_img_slice[3]])

    geometry1 = Polygon(feature["geometry"].get("coordinates")[0])
    geometry2 = transform(transformer.transform, geometry1)
    bbox = geometry2.bounds

    geometry = mapping(geometry2)

    properties = {
        "start_datetime": START_DATETIME,
        "end_datetime": END_DATETIME,
    }

    # Create item
    item = pystac.Item(
        id=id,
        geometry=geometry,
        bbox=bbox,
        datetime=None,
        properties=properties,
        stac_extensions=[],
    )

    proj_bbox = list(geometry1.bounds)

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = epsg_code
    item_projection.shape = [512, 512]
    item_projection.transform = [
        30.0, 0.0, proj_bbox[0], 0.0, -30.0, proj_bbox[3], 0.0, 0.0, 1.0
    ]
    item_projection.bbox = proj_bbox

    item_label = LabelExtension.ext(item, add_if_missing=True)
    item_label.label_properties = None
    item_label.label_description = LABEL_DESCRIPTION
    item_label.label_tasks = ["segmentation"]
    item_label.label_type = LabelType.RASTER
    item_label.label_methods = ["automated"]

    # Create label asset
    item.add_asset(
        "raster_labels",
        pystac.Asset(
            href=feature["properties"]["mask_slice"],
            roles=["labels-raster"],
            title=os.path.basename(
                os.path.splitext(feature["properties"]["mask_slice"])[0]),
        ),
    )

    asset = pystac.Asset(
        href=feature["properties"]["img_slice"],
        title=os.path.basename(
            os.path.splitext(feature["properties"]["img_slice"])[0]),
        roles=["data"],
    )

    item.add_asset(
        "raster",
        asset,
    )

    eo = EOExtension.ext(asset, add_if_missing=True)
    eo.bands = LILA_HKH_GLACIER_FUSED_BANDS

    stac_item_url = os.path.join(destination, f"{id}.json")
    item.set_self_href(stac_item_url)

    return item


def create_fused_item(cog: str, destination: str) -> pystac.Item:
    """Creates a STAC item for an SRTM/Landsat 7 fused image (COG).

    Args:
        cog (str): Path to COG asset. COG name must contain YYYYMMDD after second underscore.
        metadata_url (str): Path to provider metadata.

    Returns:
        pystac.Item: STAC Item object.
    """

    id = os.path.splitext(os.path.basename(cog))[0]

    dataset_datetime = parse_datetime(cog)

    with rasterio.open(cog, 'r') as dataset:
        mask = dataset.dataset_mask()

        proj_ext = get_proj(dataset)

        for geom, val in rasterio.features.shapes(mask,
                                                  transform=dataset.transform):
            geometry = rasterio.warp.transform_geom(dataset.crs,
                                                    'EPSG:4326',
                                                    geom,
                                                    precision=6)

        bbox = Polygon(geometry.get("coordinates")[0]).bounds

    properties: Dict[str, Any] = {}

    # Create item
    item = pystac.Item(
        id=id,
        geometry=geometry,
        bbox=bbox,
        datetime=dataset_datetime,
        properties=properties,
        stac_extensions=[],
    )

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = proj_ext["epsg"]
    item_projection.shape = proj_ext["shape"]
    item_projection.transform = list(proj_ext["transform"])
    item_projection.bbox = proj_ext["bbox"]

    asset = pystac.Asset(
        href=cog,
        media_type=pystac.MediaType.COG,
        roles=["data"],
        title="SRTM/Landsat 7 fused image (COG)",
    )

    item.add_asset(
        "cog",
        asset,
    )

    eo = EOExtension.ext(asset, add_if_missing=True)
    eo.bands = LILA_HKH_GLACIER_FUSED_BANDS

    stac_item_url = os.path.join(destination, f"{id}.json")
    item.set_self_href(stac_item_url)

    return item


def create_slice_collection(metadata_dict: Dict[str, Any],
                            destination: str) -> pystac.Collection:
    """Create a STAC Collection using a geojson file provided by LILA
    and save it to a destination.

    The metadata dict may be created using `utils.get_metadata`

    Args:
        metadata (dict): metadata parsed from jsonld
        destination (str): Path to output STAC item directory.
    Returns:
        pystac.Collection: pystac collection object
    """

    epsg_code = utils.get_epsg(metadata_dict)
    transformer = utils.create_transformer(epsg_code)

    utc = pytz.utc
    start_datetime = utc.localize(
        datetime.strptime(START_DATETIME, "%Y-%m-%dT%H:%M:%SZ"))
    end_datetime = utc.localize(
        datetime.strptime(END_DATETIME, "%Y-%m-%dT%H:%M:%SZ"))

    polygons = []
    for feature in metadata_dict["features"]:
        geometry1 = Polygon(feature["geometry"].get("coordinates")[0])
        geometry2 = transform(transformer.transform, geometry1)
        polygons.append(geometry2)

    bbox = MultiPolygon(polygons).bounds

    collection = pystac.Collection(
        id=LILA_HKH_GLACIER_SLICE_ID,
        title=LILA_HKH_GLACIER_SLICE_TITLE,
        description=LILA_HKH_GLACIER_SLICE_DESCRIPTION,
        providers=[LILA_HKH_GLACIER_PROVIDER],
        license=SLICE_LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent([bbox]),
            pystac.TemporalExtent(
                [[start_datetime or None, end_datetime or None]]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(SLICE_LICENSE_LINK)

    stac_collection_url = os.path.join(destination,
                                       f"{LILA_HKH_GLACIER_SLICE_ID}.json")

    collection.set_self_href(stac_collection_url)

    return collection


def create_fused_collection(destination: str,
                            fuseddir: str) -> pystac.Collection:
    """Create a STAC Collection with extent covering images in fuseddir

    Args:
        destination (str): Path to output STAC item directory.
        fuseddir (str): Path to fused images directory.

    Returns:
        pystac.Collection: pystac collection object
    """
    tif_files = [f for f in os.listdir(fuseddir) if f.endswith('.tif')]

    dataset_datetimes = []
    bboxes = []
    for f in tif_files:
        dataset_datetimes.append(parse_datetime(f))

        with rasterio.open(os.path.join(fuseddir, f), 'r') as dataset:
            bounds1 = dataset.bounds
            bounds2 = rasterio.warp.transform_bounds(dataset.crs, 'EPSG:4326',
                                                     *bounds1)
            bboxes.append(box(*bounds2))

    bbox = MultiPolygon(bboxes).bounds

    dataset_datetimes.sort()
    start_datetime = dataset_datetimes[0]
    end_datetime = dataset_datetimes[-1]

    collection = pystac.Collection(
        id=LILA_HKH_GLACIER_FUSED_ID,
        title=LILA_HKH_GLACIER_FUSED_TITLE,
        description=LILA_HKH_GLACIER_FUSED_DESCRIPTION,
        providers=[LILA_HKH_GLACIER_PROVIDER],
        license=FUSED_LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent([bbox]),
            pystac.TemporalExtent(
                [[start_datetime or None, end_datetime or None]]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(FUSED_LICENSE_LINK)

    stac_collection_url = os.path.join(destination,
                                       f"{LILA_HKH_GLACIER_FUSED_ID}.json")

    collection.set_self_href(stac_collection_url)

    return collection
