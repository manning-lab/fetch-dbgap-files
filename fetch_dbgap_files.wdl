version 1.0

workflow fetch_dbgap_files {
    call fetch_files
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task fetch_files {
    input {
        File cart_file
        File ngc_file
        Boolean verify = true
        String output_directory
        Int disk_gb = 50
    }

    command {
        set -e -o pipefail
        python3 fetch.py \
            --prefetch /opt/sratoolkit.3.2.1-ubuntu64/bin/prefetch \
            --ngc ~{ngc_file} \
            --cart ~{cart_file} \
            --verify ~{true="yes" false="no" verify} \
            --outdir tmp_download \
            --untar
        gcloud storage cp -r tmp_download/* ~{output_directory}
    }

    runtime {
        docker: "manninglab/fetch-dbgap-files:0.4.0"
        disks: "local-disk ~{disk_gb} HDD"
    }
}
