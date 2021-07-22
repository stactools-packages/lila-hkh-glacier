# flake8: noqa

from pystac import Provider
from pystac import Link

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
    target="https://cdla.dev/permissive-1-0",
    title="CDLA-Permissive-1.0",
)

LABEL_DESCRIPTION = "The two channels in the pixel-wise masks correspond to clean-iced and debris-covered glaciers."

START_DATETIME = "2002-01-01T12:00:00Z"
END_DATETIME = "2008-12-31T12:00:00Z"