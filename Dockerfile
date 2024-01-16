FROM python:3.12

ENV SRATOOLKIT_VERSION="3.0.0"
ENV USER="sratoolkituser"

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
RUN useradd -ms /bin/bash ${USER}
RUN mkdir /home/${USER}/.ncbi
RUN echo '/LIBS/GUID = "mock-uid"\nconfig/default = "true"' > /home/${USER}/.ncbi/user-settings.mkfg
USER ${USER}

CMD /bin/sh
