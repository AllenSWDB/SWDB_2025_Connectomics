# hash:sha256:ba9c9d44f0dea83594fb90cb9fa565fbece660d5c72d62a1a2509bc545be9dfa
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/py-r:python3.12.4-R4.3.3-JupyterLab4.2.4-RStudiorstudio-server-2024.04.2-764-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip3 install -U --no-cache-dir \
    caveclient \
    matplotlib \
    numpy \
    pandas \
    pynwb \
    scipy \
    seaborn \
    skeleton-plot \
    standard-transform \
    tqdm
