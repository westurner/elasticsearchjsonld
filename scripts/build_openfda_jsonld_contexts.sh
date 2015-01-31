#!/bin/bash +e +x


download_es_schema() {
    SCHEMADIR=$1
    mkdir -p "${SCHEMADIR}"
    curl 'https://raw.githubusercontent.com/FDA/openfda/master/schemas/faers_mapping.json' -o "${SCHEMADIR}/faers_mapping.json"
    curl 'https://raw.githubusercontent.com/FDA/openfda/master/schemas/maude_mapping.json' -o "${SCHEMADIR}/maude_mapping.json"
    curl 'https://raw.githubusercontent.com/FDA/openfda/master/schemas/res_mapping.json' -o "${SCHEMADIR}/res_mapping.json"
    curl 'https://raw.githubusercontent.com/FDA/openfda/master/schemas/spl_mapping.json' -o "${SCHEMADIR}/spl_mapping.json"
}

generate_jsonld_contexts() {
    SCHEMADIR=$1
    JSONLDDIR=$2
    mkdir -p $JSONLDDIR
    for x in "faers" "maude" "res" "spl"; do
        esjson2jsonld -i "${SCHEMADIR}/${x}_mapping.json" --vocab="http://open.fda.gov/ns/${x}#" -o "${JSONLDDIR}/${x}.jsonld"
    done
}


main() {
    SCHEMADIR=${1:-'./openfda/schemas'}
    JSONLDDIR=${2:-'./openfda/ns'}

    download_es_schema "${SCHEMADIR}"
    generate_jsonld_contexts "${SCHEMADIR}" "${JSONLDDIR}"
}

main $@
