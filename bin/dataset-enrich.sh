SLICE=$(python -c "import hashlib, sys; print(int(hashlib.sha1('$GITHUB_REPOSITORY'.encode()).hexdigest(),16) % 16)")
export SHARD_ID=$SLICE