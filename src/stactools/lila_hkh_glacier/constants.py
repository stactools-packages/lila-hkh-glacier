# flake8: noqa

from pystac import Link, Provider, ProviderRole
from pystac.extensions.eo import Band

FUSED_LICENSE = "PDDL-1.0"
FUSED_LICENSE_LINK = Link(
    rel="license",
    target="https://spdx.org/licenses/PDDL-1.0.html",
    title="Open Data Commons Public Domain Dedication & License 1.0",
)

LILA_HKH_GLACIER_FUSED_BANDS = [
    Band({
        "name": "LE7 B1",
        "common_name": "blue",
        "center_wavelength": 0.485
    }),
    Band({
        "name": "LE7 B2",
        "common_name": "green",
        "center_wavelength": 0.56
    }),
    Band({
        "name": "LE7 B3",
        "common_name": "red",
        "center_wavelength": 0.66
    }),
    Band({
        "name": "LE7 B4",
        "common_name": "nir",
        "center_wavelength": 0.835
    }),
    Band({
        "name": "LE7 B5",
        "common_name": "swir16",
        "center_wavelength": 1.65
    }),
    Band({
        "name": "LE7 B6_VCID_1",
        "common_name": "lwir",
        "center_wavelength": 11.45
    }),
    Band({
        "name": "LE7 B6_VCID_2",
        "common_name": "lwir",
        "center_wavelength": 11.45
    }),
    Band({
        "name": "LE7 B7",
        "common_name": "swir22",
        "center_wavelength": 2.215
    }),
    Band({
        "name": "LE7 B8",
        "common_name": "pan",
        "center_wavelength": 0.71
    }),
    Band({
        "name": "LE7 BQA",
    }),
    Band({
        "name": "NDVI",
    }),
    Band({"name": "NDSI"}),
    Band({"name": "NDWI"}),
    Band({"name": "SRTM 90 elevation"}),
    Band({"name": "SRTM 90 slope"}),
]
LILA_HKH_GLACIER_FUSED_ID = "lila-hkh-glacier-fused"
LILA_HKH_GLACIER_FUSED_DESCRIPTION = "Each fused image is a spatial area measuring roughly 6km x 7.5km (with definitions that roughly match up with USGS quarter quadrangles). Each fused image comes with one corresponding GeoTIFF file. The entire glacier mapping dataset contains 35 tiles from Afghanistan, Bangladesh, Bhutan, China, India, Myanmar, Nepal, and Pakistan. Each GeoTIFF tile consists of 15 channels. All channels are aligned at 30m spatial resolution. Elevation and slope channels were upsampled from 90m to 30m resolution."
LILA_HKH_GLACIER_FUSED_TITLE = "Hindu Kush Himalayas Glacier Mapping fused SRTM/Landsat 7 images"

LILA_HKH_GLACIER_SLICE_ID = "lila-hkh-glacier-slices"
LILA_HKH_GLACIER_SLICE_TITLE = "Hindu Kush Himalayas Glacier Mapping labelled image slices"
LILA_HKH_GLACIER_SLICE_DESCRIPTION = "This dataset couples annotated glacier locations with multispectral imagery from Landsat 7 and digital elevation and slope data from SRTM. Imagery are provided as numpy patches. Labels are available as multichannel numpy masks. Both the labels and the masks are cropped according to the borders of the HKH region."
LILA_HKH_GLACIER_PROVIDER = Provider(
    name="Labeled Information Library of Alexandria: Biology and Conservation",
    roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR, ProviderRole.HOST],
    url="http://lila.science/datasets/hkh-glacier-mapping")

SLICE_LICENSE = "CDLA-Permissive-1.0"
SLICE_LICENSE_LINK = Link(
    rel="license",
    target="https://spdx.org/licenses/CDLA-Permissive-1.0.html",
    title="Community Data License Agreement Permissive 1.0",
)

LABEL_DESCRIPTION = "The two channels in the pixel-wise masks correspond to clean-iced and debris-covered glaciers."

START_DATETIME = "2002-01-01T12:00:00Z"
END_DATETIME = "2008-12-31T12:00:00Z"
