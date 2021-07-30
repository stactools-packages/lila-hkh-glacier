import click
import os
import logging

from stactools.lila_hkh_glacier import cog
from stactools.lila_hkh_glacier import stac
from stactools.lila_hkh_glacier import utils

logger = logging.getLogger(__name__)


def create_lilahkhglacier_command(cli: click.Group) -> click.Command:
    """Creates the lilahkhglacier command line utility."""
    @cli.group(
        "lilahkhglacier",
        short_help=(
            """Commands for working with LILA HKH Glacier Mapping data"""),
    )
    def lilahkhglacier() -> None:
        pass

    @lilahkhglacier.group(
        "lilahkhglacier-slice",
        short_help=("""Commands for working with labelled image slices"""),
    )
    def slice() -> None:
        pass

    @slice.command(
        "create-collection",
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
        required=True,
        help="The url to the metadata geojson",
    )
    def create_slice_collection_command(destination: str,
                                        metadata: str) -> None:
        """Creates a STAC Collection for labelled image slices from LILA HKH Glacier Mapping metadata

        Args:
            destination (str): Directory used to store the collection json
            metadata (str): Path to a geojson metadata file - provided by LILA
        Returns:
            Callable
        """
        metadata_dict = utils.get_metadata(metadata)
        epsg_code = utils.get_epsg(metadata_dict)
        transformer = utils.create_transformer(epsg_code)

        stac.create_slice_collection(metadata_dict, destination, transformer)

    @slice.command(
        "create-items",
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
        required=True,
        help="The url to the metadata geojson.",
    )
    @click.option(
        "-s",
        "--slicedir",
        required=True,
        help="The slices directory.",
    )
    def create_slice_item_command(destination: str, metadata: str,
                                  slicedir: str) -> None:
        """Generate STAC items using the metadata.

        Args:
            destination (str): Local directory to save the STAC Item json
            metadata (str): url containing the LILA HKH Glacier Mapping metadata
            slicedir (str): url of the LILA HKH Glacier Mapping slices directory
        """
        raw_metadata = utils.get_metadata(metadata)
        metadata_dict = utils.update_metadata_paths(raw_metadata, slicedir)
        epsg_code = utils.get_epsg(metadata_dict)
        transformer = utils.create_transformer(epsg_code)

        for feature in metadata_dict['features']:
            stac.create_slice_item(feature, destination, transformer,
                                   epsg_code)

    @lilahkhglacier.group(
        "lilahkhglacier-fused",
        short_help=(
            """Commands for working with SRTM/Landsat 7 fused images (COGs)"""
        ),
    )
    def fused() -> None:
        pass

    @fused.command(
        "create-collection",
        short_help=(
            "Create a STAC collection for SRTM/Landsat 7 fused images (COGs)"))
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    @click.option(
        "-f",
        "--fuseddir",
        required=True,
        help="The fused images directory.",
    )
    def create_fused_collection_command(destination: str,
                                        fuseddir: str) -> None:
        """Creates a STAC Collection for SRTM/Landsat 7 fused images (COGs)

        Args:
            destination (str): Directory used to store the collection json
            fuseddir (str): path to fused images directory
        Returns:
            Callable
        """
        stac.create_fused_collection(destination, fuseddir)

    @fused.command(
        "create-items",
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
    ) -> None:
        """Generate a STAC item for an SRTM/Landsat 7 fused image.

        Args:
            cog (str): location of a COG asset for the item
            destination (str): Local directory to save the STAC Item json
        """
        stac.create_fused_item(cog, destination)

    @lilahkhglacier.command(
        "create-cog",
        short_help="Transform Geotiff to Cloud-Optimized Geotiff.",
    )
    @click.option("-d",
                  "--destination",
                  required=True,
                  help="The output directory for the COG")
    @click.option("-s",
                  "--source",
                  required=True,
                  help="Path to an input GeoTiff")
    def create_cog_command(destination: str, source: str) -> None:
        """Generate a COG from a GeoTiff. The COG will be saved in the destination
        with `_cog.tif` appended to the name.

        Args:
            destination (str): Local directory to save output COGs
            source (str): An input GeoTiff
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        output_path = os.path.join(
            destination,
            os.path.splitext(os.path.basename(source))[0] + "_cog.tif")

        cog.create_cog(source, output_path)

    return lilahkhglacier
