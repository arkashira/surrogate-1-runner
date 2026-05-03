- name: Generate manifest (once per date)
  run: |
    HF_TOKEN=${{ secrets.HF_TOKEN }} \
    ./bin/gen-manifest.sh axentx/surrogate-1-training-pairs ${{ env.DATE_PATH }} > manifest-${{ env.DATE_PATH }}.json

- name: Run 16 shards in parallel
  run: |
    for SHARD in $(seq 0 15); do
      SHARD_ID=$SHARD TOTAL_SHARDS=16 \
      MANIFEST_FILE=manifest-${{ env.DATE_PATH }}.json \
      DATE_PATH=${{ env.DATE_PATH }} \
      ./bin/dataset-enrich.sh &
    done
    wait