FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:489.0.0-slim

ENV SRATOOLKIT_VERSION="3.2.1"

# Install SRA Toolkit.
RUN cd /opt/ \
    && \
    curl -LO \
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

# Check out repository files.
RUN cd /usr/local && \
    git clone https://github.com/manning-lab/fetch-dbgap-files.git


CMD /bin/sh
