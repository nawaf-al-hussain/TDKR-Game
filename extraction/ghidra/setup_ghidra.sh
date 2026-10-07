#!/bin/bash
# Rebuild the Ghidra RE environment for TDKR libKRHP.so analysis (Ghidra 12.1.4 + JDK 25).
# Usage: bash setup_ghidra.sh   (~5 min on this network; needs ~1.6 GB disk)
# Then re-analyze (once): bash setup_ghidra.sh analyze
# Then decompile: python3 /home/z/my-project/scripts/decompile_by_addr.py <addr>...
#   or the name-based one-shot pattern in extraction/ghidra/RE_NOTES.md
set -e
GDIR=/home/z/ghidra_dl
mkdir -p $GDIR/projects
cd $GDIR

if [ ! -d ghidra_12.1.4_PUBLIC ]; then
  echo "[1/4] downloading Ghidra 12.1.4..."
  curl -C - -sL -o ghidra.zip "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip"
  echo "[2/4] unpacking (docs/GPL/server excluded to save disk)..."
  unzip -q ghidra.zip -x "*/docs/*" "*/GPL/*" "*/server/*" "*/licenses/*"
  rm -f ghidra.zip
fi

if [ ! -d jdk-25.0.4.1+1 ] && [ ! -d "$(ls -d jdk-25* 2>/dev/null | head -1)" ]; then
  echo "[3/4] downloading JDK 25 (full JDK; JRE/21/23 are rejected by Ghidra 12)..."
  curl -C - -sL -o jdk25.tar.gz "https://api.adoptium.net/v3/binary/latest/25/ga/linux/x64/jdk/hotspot/normal/eclipse"
  tar xzf jdk25.tar.gz && rm -f jdk25.tar.gz
fi
JDK=$(ls -d $GDIR/jdk-25*)

echo "[4/4] configuring JAVA_HOME_OVERRIDE..."
sed -i "s|^JAVA_HOME_OVERRIDE=.*|JAVA_HOME_OVERRIDE=$JDK|" ghidra_12.1.4_PUBLIC/support/launch.properties
echo "Ghidra ready: $GDIR/ghidra_12.1.4_PUBLIC (JDK: $JDK)"

if [ "${1:-}" = "analyze" ] && [ ! -d $GDIR/projects/TDKR.rep ]; then
  echo "analyzing libKRHP.so (30-60 min)..."
  $GDIR/ghidra_12.1.4_PUBLIC/support/analyzeHeadless $GDIR/projects TDKR \
    -import /home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so \
    -processor ARM:LE:32:v7 -cspec default -analysisTimeoutPerFile 3000
fi
echo "done."
