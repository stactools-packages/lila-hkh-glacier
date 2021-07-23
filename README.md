# stactools-lila-hkh-glacier

- Name: lila-hkh-glacier
- Package: `stactools.lila-hkh-glacier`
- PyPI: https://pypi.org/project/stactools-lila-hkh-glacier/
- Owner: @darrenwiens
- Dataset homepage: http://lila.science/datasets/hkh-glacier-mapping
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [eo](https://github.com/stac-extensions/eo)
  - [label](https://github.com/stac-extensions/label)

This package creates STAC items for fused SRTM/Landsat 7 images, and image slices (tiles) that are labelled for presence of clean-iced and debris-covered glaciers.

## Examples


### STAC objects

- Fused SRTM/Landsat 7 images
  - [Collection](examples/fused-collection.json)
  - [Item](examples/fused-item.json)
- Labelled image slices
  - [Collection](examples/slice-collection.json)
  - [Item](examples/slice-item.json)

### Command-line usage

Create a collection for fused SRTM/Landsat 7 images.

```bash
$ stac lilahkhglacier create-fused-collection -d destination -f fuseddir
```

Create a collection for labelled image slices.

```bash
$ stac lilahkhglacier create-slice-collection -d destination -m metadata_geojson
```

Create an item for a fused SRTM/Landsat 7 image (COG).

```bash
$ stac lilahkhglacier create-fused-item -d destination -c cog
```

Create an item for labelled image slices.

```bash
$ stac lilahkhglacier create-slice-item -d destination -m metadata_geojson -s slice_directory
```

Convert GeoTiff to Cloud-optimized GeoTiff (COG).

```bash
$ stac lilahkhglacier create-cog -d destination -s source
```

Use `stac lilahkhglacier --help` to see all subcommands and options.
