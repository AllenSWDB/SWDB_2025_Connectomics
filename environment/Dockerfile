# hash:sha256:a3ba3604ef2ff932a4962c260934a5b7f15fa749288662ad4b4b3bfcf86d8d11
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/py-r:python3.12.4-R4.3.3-JupyterLab4.2.4-RStudiorstudio-server-2024.04.2-764-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip3 install -U --no-cache-dir \
    caveclient==7.11.0 \
    matplotlib==3.10.5 \
    numpy==2.3.2 \
    pandas==2.3.1 \
    pynwb==3.1.1 \
    scipy==1.16.1 \
    seaborn \
    skeleton-plot==0.1.0 \
    standard-transform==1.4.1 \
    tqdm==4.67.1
