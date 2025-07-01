version 1.0

workflow fetch_dbgap_files {
    call fetch_files
    output { Array[File] downloaded_files = fetch_files.downloaded_files }

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}

task fetch_files {
    input {
        File cart_file
        File ngc_file
        String output_directory
        Int disk_gb = 50
    }

    command <<<
        python3 /usr/local/fetch-dbgap-files/fetch.py \
            --prefetch /opt/sratoolkit.3.2.1-ubuntu64/bin/prefetch \
            --ngc ~{ngc_file} \
            --cart ~{cart_file} \
            --outdir tmp_download \
            --untar
        #gcloud storage cp -r tmp_download/* ~{output_directory}
    >>>

    output { Array[File] downloaded_files = glob("tmp_download/*") }

    runtime {
        docker: "manninglab/fetch-dbgap-files:0.4.0"
        disks: "local-disk ~{disk_gb} HDD"
    }
}
