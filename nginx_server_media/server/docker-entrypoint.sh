#!/bin/sh

ffmpeg -r 30 -f lavfi -i testsrc -vf scale=1280:960 -vcodec libx264 -profile:v baseline -pix_fmt yuv420p -f flv rtmp://localhost:1935/live/test

echo "/patched-lib" > /etc/ld.so.conf.d/000-patched-lib.conf && \
mkdir -p "/patched-lib" && \
PATCH_OUTPUT_DIR=/patched-lib /usr/local/bin/patch.sh && \
cd /patched-lib && \
for f in * ; do
    suffix="${f##*.so}"
    name="$(basename "$f" "$suffix")"
    [ -h "$name" ] || ln -sf "$f" "$name"
    [ -h "$name" ] || ln -sf "$f" "$name.1"
done && \
ldconfig
[ "$OLDPWD" ] && cd -
exec "$@"

