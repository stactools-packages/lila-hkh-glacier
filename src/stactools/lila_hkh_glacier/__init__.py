import stactools.core
from stactools.cli import Registry
from stactools.lila_hkh_glacier import commands
from stactools.lila_hkh_glacier.stac import (create_slice_collection,
                                             create_slice_item,
                                             create_fused_collection,
                                             create_fused_item)

__all__ = [
    create_slice_collection.__name__, create_slice_item.__name__,
    create_fused_collection.__name__, create_fused_item.__name__
]

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    registry.register_subcommand(commands.create_lilahkhglacier_command)


__version__ = "0.2.0"
