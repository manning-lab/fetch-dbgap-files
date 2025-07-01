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
        Boolean verify = 'yes'
        String output_directory
        Int disk_gb = 50
    }

    command {
        set -e -o pipefail
        python3 /usr/local/fetch-dbgap-files/fetch.py \
            --prefetch /opt/sratoolkit.3.2.1-ubuntu64/bin/prefetch \
            --ngc ~{ngc_file} \
            --cart ~{cart_file} \
            --verify ~{verify} \
            --outdir tmp_download \
            --untar
        gcloud storage cp -r tmp_download/* ~{output_directory}
    }

    runtime {
        docker: "uwgac/fetch-dbgap-files:0.3.0"
        disks: "local-disk ~{disk_gb} HDD"
    }
}
