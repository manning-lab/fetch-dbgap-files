FROM us.gcr.io/broad-dsp-gcr-public/anvil-rstudio-bioconductor:3.18.0

ENV SRATOOLKIT_VERSION="3.2.1"

# Check out repository files.
RUN cd /usr/local && \
    git clone https://github.com/UW-GAC/fetch-dbgap-files.git

# Install SRA Toolkit.
RUN cd /opt/ \
    && \
    wget \
        https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/${SRATOOLKIT_VERSION}/sratoolkit.${SRATOOLKIT_VERSION}-ubuntu64.tar.gz \
    && \
    tar \
        xvf \
        sratoolkit.${SRATOOLKIT_VERSION}-ubuntu64.tar.gz
# Add sratoolkit commands to the path.
ENV PATH=/opt/sratoolkit.3.0.0-ubuntu64/bin:${PATH}
# Create and set the SRA Toolkit user.
RUN mkdir ~/.ncbi
RUN echo '/LIBS/GUID = "mock-uid"\nconfig/default = "true"' > ~/.ncbi/user-settings.mkfg

CMD /bin/sh
