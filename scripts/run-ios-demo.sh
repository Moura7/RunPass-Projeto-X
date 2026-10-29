#!/usr/bin/env bash
# Build outside Documents to avoid Finder metadata breaking ad-hoc codesigning.
set -euo pipefail
runpass_demo_repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
runpass_demo_flutter="${FLUTTER:-flutter}"
runpass_demo_device="${1:-booted}"
runpass_demo_build="$(mktemp -d /private/tmp/runpass-ios-demo.XXXXXX)"
trap 'rm -rf -- "$runpass_demo_build"' EXIT
COPYFILE_DISABLE=1 rsync -a --exclude=build --exclude=.dart_tool --exclude=.idea --exclude=.git \
  --exclude=ios/Flutter/ephemeral --exclude=ios/Flutter/Generated.xcconfig \
  --exclude=ios/Flutter/flutter_export_environment.sh \
  "$runpass_demo_repo/mobile/" "$runpass_demo_build/"
(
  cd -- "$runpass_demo_build"
  "$runpass_demo_flutter" build ios --simulator --debug -t lib/main_demo.dart
)
xcrun simctl bootstatus "$runpass_demo_device" -b
xcrun simctl install "$runpass_demo_device" "$runpass_demo_build/build/ios/iphonesimulator/Runner.app"
xcrun simctl launch "$runpass_demo_device" br.com.runpass.runpass
