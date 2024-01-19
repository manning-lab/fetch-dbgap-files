version 1.0

workflow fetch_dbgap_files {
    input {
        File cart_file
        File manifest_file
        File ngc_file
        String output_directory
        Int? disk_gb
    }

    call fetch_files {
        input:
            cart_file=cart_file,
            manifest_file=manifest_file,
            ngc_file=ngc_file,
            output_directory=output_directory,
            disk_gb=disk_gb
    }

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }

}


task fetch_files {
    input {
        File cart_file
        File manifest_file
        File ngc_file
        String output_directory
        Int disk_gb = 50
    }
    command {
        python3 /usr/local/fetch-dbgap-files/fetch.py \
            --prefetch /opt/sratoolkit.3.0.10-ubuntu64/bin/prefetch \
            --ngc ~{ngc_file} \
            --cart ~{cart_file} \
            --manifest ~{manifest_file} \
            --outdir tmp_download \
            --untar
        gsutil cp -m -r tmp_download/* ~{output_directory}
    }
    runtime {
        # Pull from DockerHub
        docker: "uwgac/fetch-dbgap-files:0.1.0"
        disks: "local-disk ${disk_gb} SSD"
    }
}
