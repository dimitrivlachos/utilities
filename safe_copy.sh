#!/bin/bash

# Usage: ./safe_dataset_copy.sh /path/to/source_dataset /dls/mx-scratch/dimitri
# Example: ./safe_dataset_copy.sh /dls/staging/dls/i03/data/2025/cm40607-1/TestInsulin/ins_7 /dls/mx-scratch/dimitri

set -euo pipefail

SRC="$1"
DST_PARENT="$2"
BASENAME="$(basename "$SRC")"
DST="$DST_PARENT/$BASENAME"

echo "📦 Copying '$SRC' to '$DST'..."
cp -a "$SRC" "$DST"

echo "🔐 Fixing directory permissions..."
chmod 755 "$DST"
setfacl --remove-all "$DST"
setfacl --remove-all -d "$DST" || true  # Not all filesystems support default ACLs

echo "📄 Fixing file permissions..."
find "$DST" -type f -exec chmod 644 {} +
find "$DST" -type f -exec setfacl --remove-all {} +

echo "📁 Fixing subdirectory permissions..."
find "$DST" -type d -exec chmod 755 {} +
find "$DST" -type d -exec setfacl --remove-all {} +
find "$DST" -type d -exec setfacl --remove-all -d {} + 2>/dev/null || true

echo "✅ Done. Dataset copied and sanitised:"
ls -ld "$DST"
