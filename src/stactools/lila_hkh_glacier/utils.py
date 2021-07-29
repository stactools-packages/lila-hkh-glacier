import json
import os
from typing import Any, Dict
from pyproj import Transformer


def create_transformer(crs_from: int, crs_to: int = 4326) -> Transformer:
    return Transformer.from_crs(crs_from, crs_to, always_xy=True)


def get_epsg(metadata: Dict[str, Any]) -> int:
    crs = metadata["crs"]["properties"]["name"]
    return int(crs.split("EPSG::")[1])


def get_metadata(metadata_url: str) -> Dict[str, Any]:
    """Gets metadata from the LILA HKH Glacier Mapping geojson metadata.

    Args:
        metadata_url (str): url to get metadata from.

    Returns:
        dict: LILA HKH Glacier Mapping Metadata.
    """
    if metadata_url.endswith(".geojson"):
        with open(metadata_url) as f:
            metadata: Dict[str, Any] = json.load(f)
        return metadata
    else:
        # only geojson support.
        raise NotImplementedError()


def update_metadata_paths(raw_metadata: Dict[str, Any],
                          slicedir: str) -> Dict[str, Any]:
    """Updates image slice and mask slice urls in metadata.

    Args:
        raw_metadata (dict): original metadata.
        slicedir (str): url of the LILA HKH Glacier Mapping slices directory

    Returns:
        dict: Metadata with updated urls.
    """

    for feature in raw_metadata['features']:
        feature['properties']['img_slice'] = os.path.join(
            slicedir, os.path.basename(feature['properties']['img_slice']))
        feature['properties']['mask_slice'] = os.path.join(
            slicedir, os.path.basename(feature['properties']['mask_slice']))

    return raw_metadata
