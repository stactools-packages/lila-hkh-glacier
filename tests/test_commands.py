import os.path
from tempfile import TemporaryDirectory

import pystac

from stactools.lila_hkh_glacier.commands import create_lilahkhglacier_command
from stactools.testing import CliTestCase

from tests import test_data


class CreateCollectionTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_lilahkhglacier_command]

    def test_create_slice_collection(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            metadata_path = os.path.join(test_path, "slices.geojson")

            result = self.run_command([
                "lilahkhglacier", "create-slice-collection", "-d", tmp_dir,
                "-m", metadata_path
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))

            collection.validate()

    def test_create_slice_item(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            metadata_path = os.path.join(test_path, "slices.geojson")

            slice_dir = os.path.join(test_path, "slices")

            result = self.run_command([
                "lilahkhglacier", "create-slice-item", "-d", tmp_dir, "-m",
                metadata_path, "-s", slice_dir
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 2)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

        item.validate()

    def test_create_fused_collection(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            fuseddir = os.path.join(test_path, "raster_data")

            result = self.run_command([
                "lilahkhglacier", "create-fused-collection", "-d", tmp_dir,
                "-f", fuseddir
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))

            collection.validate()

    def test_create_fused_item(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            cog_path = os.path.join(
                test_path, "raster_data/LE07_134040_20070922_clip.tif")

            result = self.run_command([
                "lilahkhglacier", "create-fused-item", "-d", tmp_dir, "-c",
                cog_path
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

        item.validate()
