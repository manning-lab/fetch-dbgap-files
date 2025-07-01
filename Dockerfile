# Latest gcloud SDK version where make is still included
FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:532.0.0-slim

# Install cmake, required to build sra-toolkit
RUN \
  apt update && \
  apt install cmake -y && \
  rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Build & install ncbi-vdb (dependency), then sra-toolkit.
RUN \
  git clone https://github.com/ncbi/sra-tools.git && \
  git clone https://github.com/ncbi/ncbi-vdb.git  && \
  cd    ncbi-vdb  && ./configure && make -j && \
  cd ../sra-tools && ./configure && make -j # TODO: add a sed command to remove prefetch.c's file size checks
ENV PATH="$PATH:~/ncbi-outdir/sra-tools/linux/gcc/x86_64/rel/bin"

# Create and set the sra-toolkit user.
RUN mkdir ~/.ncbi
RUN echo '/LIBS/GUID = "mock-uid"\nconfig/default = "true"' > ~/.ncbi/user-settings.mkfg

# Get fetch.py
RUN \
  git clone https://github.com/manning-lab/fetch-dbgap-files.git && \
  cp fetch-dbgap-files/fetch.py .

CMD /bin/sh
