import logging
import os
import pystac
import pytz

from datetime import datetime
from pyproj import Transformer
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.label import LabelExtension
from stactools.lila_hkh_glacier.constants import (
    LABEL_DESCRIPTION, SLICE_LICENSE, SLICE_LICENSE_LINK,
    LILA_HKH_GLACIER_SLICE_ID, LILA_HKH_GLACIER_SLICE_DESCRIPTION,
    LILA_HKH_GLACIER_PROVIDER, LILA_HKH_GLACIER_SLICE_TITLE, START_DATETIME,
    END_DATETIME)
from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import transform

logger = logging.getLogger(__name__)


def create_slice_item(feature: dict, destination: str,
                      transformer: Transformer) -> pystac.Item:
    """Creates a STAC item for a LILA HKH Glacier Mapping labelled slice image feature.

    Args:
        feature (dict): Path to provider metadata.
        destination (str): Path to output STAC item directory.
        transformer (Transformer): pyproj Transformer for converting from data projection to 4326.

    Returns:
        pystac.Item: STAC Item object.
    """

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

    item_projection = ProjectionExtension.ext(item, add_if_missing=True)
    item_projection.epsg = int(
        transformer._transformer_maker.crs_from.split(":")[1])

    item_label = LabelExtension.ext(item, add_if_missing=True)
    item_label.label_properties = None
    item_label.label_description = LABEL_DESCRIPTION
    item_label.label_tasks = ["segmentation"]
    item_label.label_type = "raster"
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

    # Create image asset
    item.add_asset(
        "raster",
        pystac.Asset(
            href=feature["properties"]["img_slice"],
            title=os.path.basename(
                os.path.splitext(feature["properties"]["img_slice"])[0]),
        ),
    )

    stac_item_url = os.path.join(destination, f"{id}.json")
    item.set_self_href(stac_item_url)

    item.save_object()

    return item


def create_slice_collection(metadata: dict, destination: str,
                            transformer: Transformer) -> pystac.Collection:
    """Create a STAC Collection using a geojson file provided by LILA
    and save it to a destination.

    The metadata dict may be created using `utils.get_metadata`

    Args:
        metadata (dict): metadata parsed from jsonld
        destination (str): Path to output STAC item directory.
        transformer (Transformer): pyproj Transformer for converting from data projection to 4326.

    Returns:
        pystac.Collection: pystac collection object
    """
    utc = pytz.utc
    start_datetime = utc.localize(
        datetime.strptime(START_DATETIME, "%Y-%m-%dT%H:%M:%SZ"))
    end_datetime = utc.localize(
        datetime.strptime(END_DATETIME, "%Y-%m-%dT%H:%M:%SZ"))

    polygons = []
    for feature in metadata["features"]:
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
            pystac.TemporalExtent([start_datetime, end_datetime]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )
    collection.add_link(SLICE_LICENSE_LINK)

    stac_collection_url = os.path.join(destination,
                                       f"{LILA_HKH_GLACIER_SLICE_ID}.json")

    collection.set_self_href(stac_collection_url)

    collection.save_object()

    return collection
