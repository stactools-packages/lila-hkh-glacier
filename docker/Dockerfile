ARG STACTOOLS_VERSION=latest
FROM ghcr.io/stac-utils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/stactools-lila-hkh-glacier

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/lila_hkh_glacier/__init__.py src/stactools/lila_hkh_glacier/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/lila_hkh_glacier

COPY src ./src
RUN pip install .
