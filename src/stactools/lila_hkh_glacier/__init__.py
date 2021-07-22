import stactools.core
from stactools.lila_hkh_glacier.stac import create_slice_collection, create_slice_item

__all__ = [create_slice_collection, create_slice_item]

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.lila_hkh_glacier import commands

    registry.register_subcommand(commands.create_lilahkhglacier_command)


__version__ = "0.2.0"
