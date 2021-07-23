import click
import logging

from stactools.lila_hkh_glacier import stac
from stactools.lila_hkh_glacier import utils

logger = logging.getLogger(__name__)


def create_lilahkhglacier_command(cli):
    """Creates the lilahkhglacier command line utility."""
    @cli.group(
        "lilahkhglacier",
        short_help=(
            """Commands for working with LILA HKH Glacier Mapping data"""),
    )
    def lilahkhglacier():
        pass

    @lilahkhglacier.command(
        "create-slice-collection",
        short_help=("Create a STAC collection for labelled image slices"))
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    @click.option(
        "-m",
        "--metadata",
        help="The url to the metadata geojson",
    )
    def create_slice_collection_command(destination: str, metadata: str):
        """Creates a STAC Collection for labelled image slices from LILA HKH Glacier Mapping metadata

        Args:
            destination (str): Directory used to store the collection json
            metadata (str): Path to a geojson metadata file - provided by LILA
        Returns:
            Callable
        """
        metadata = utils.get_metadata(metadata)
        epsg_code = utils.get_epsg(metadata)
        transformer = utils.create_transformer(epsg_code)

        stac.create_slice_collection(metadata, destination, transformer)

    @lilahkhglacier.command(
        "create-slice-item",
        short_help="Create a STAC item for labelled image slices",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json",
    )
    @click.option(
        "-m",
        "--metadata",
        help="The url to the metadata geojson.",
    )
    @click.option(
        "-s",
        "--slicedir",
        help="The slices directory.",
    )
    def create_slice_item_command(destination: str, metadata: str,
                                  slicedir: str):
        """Generate STAC items using the metadata.

        Args:
            destination (str): Local directory to save the STAC Item json
            metadata (str): url containing the LILA HKH Glacier Mapping metadata
            slicedir (str): url of the LILA HKH Glacier Mapping slices directory
        """
        raw_metadata = utils.get_metadata(metadata)
        metadata = utils.update_metadata_paths(raw_metadata, slicedir)
        epsg_code = utils.get_epsg(metadata)
        transformer = utils.create_transformer(epsg_code)

        for feature in metadata['features']:
            stac.create_slice_item(feature, destination, transformer)

    @lilahkhglacier.command(
        "create-fused-item",
        short_help="Create a STAC item for an SRTM/Landsat 7 fused image (COG)",
    )
    @click.option("-c", "--cog", required=True, help="COG href")
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json",
    )
    def create_fused_item_command(
        cog: str,
        destination: str,
    ):
        """Generate a STAC item for an SRTM/Landsat 7 fused image.

        Args:
            cog (str): location of a COG asset for the item
            destination (str): Local directory to save the STAC Item json
        """
        stac.create_fused_item(cog, destination)

    return lilahkhglacier
