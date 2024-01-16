version 1.0

workflow fetch_dbgap_files {
    input {
        File cart_file
        File manifest_file
        File ngc_file
        String output_directory
    }

    call download_files {
        input:
            cart_file=cart_file,
            manifest_file=manifest_file,
            ngc_file=ngc_file,
            output_directory=output_directory
    }

    call copy_files {
        input: output_directory=output_directory
    }

    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }

}


task download_files {
  input {
        File cart_file
        File manifest_file
        File ngc_file
        String output_directory
  }
  command {
    python3 /projects/primed/analysts/amstilp/devel/fetch-dbgap-files/fetch.py \
        --ngc /projects/primed/dbgap/prj_33119_D13875.ngc \
        --cart ~{cart_file}
        --manifest ~{manifest_file} \
        --outdir  tmp_download \
        --untar
  }
  runtime {
    # Pull from DockerHub
    docker: "uwgac/fetch-dbgap-files:0.0.999.1"
  }
}

task copy_files {
    input {
        String output_directory
    }

    command {
        gsutil_cp tmp_download/* ~{output_directory}
    }
}
