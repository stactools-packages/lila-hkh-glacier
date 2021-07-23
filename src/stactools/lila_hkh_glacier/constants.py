# flake8: noqa

from pystac import Provider
from pystac import Link

FUSED_LICENSE = "PDDL-1.0"
FUSED_LICENSE_LINK = Link(
    rel="license",
    target="https://spdx.org/licenses/PDDL-1.0.html",
    title="Open Data Commons Public Domain Dedication & License 1.0",
)

LILA_HKH_GLACIER_FUSED_ID = "lila-hkh-glacier-fused"
LILA_HKH_GLACIER_FUSED_DESCRIPTION = "Each fused image is a spatial area measuring roughly 6km x 7.5km (with definitions that roughly match up with USGS quarter quadrangles). Each fused image comes with one corresponding GeoTIFF file. The entire glacier mapping dataset contains 35 tiles from Afghanistan, Bangladesh, Bhutan, China, India, Myanmar, Nepal, and Pakistan. Each GeoTIFF tile consists of 15 channels. All channels are aligned at 30m spatial resolution. Elevation and slope channels were upsampled from 90m to 30m resolution."
LILA_HKH_GLACIER_FUSED_TITLE = "Hindu Kush Himalayas Glacier Mapping fused SRTM/Landsat 7 images"

LILA_HKH_GLACIER_SLICE_ID = "lila-hkh-glacier-slices"
LILA_HKH_GLACIER_SLICE_TITLE = "Hindu Kush Himalayas Glacier Mapping labelled image slices"
LILA_HKH_GLACIER_SLICE_DESCRIPTION = "This dataset couples annotated glacier locations with multispectral imagery from Landsat 7 and digital elevation and slope data from SRTM. Imagery are provided as numpy patches. Labels are available as multichannel numpy masks. Both the labels and the masks are cropped according to the borders of the HKH region."
LILA_HKH_GLACIER_PROVIDER = Provider(
    name="Labeled Information Library of Alexandria: Biology and Conservation",
    roles=["producer", "processor", "host"],
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