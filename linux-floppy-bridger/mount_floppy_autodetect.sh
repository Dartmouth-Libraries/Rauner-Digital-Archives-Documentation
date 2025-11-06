#!/usr/bin/env bash
#
# mount_floppy_autodetect.sh
#
# Auto-detect a ~1.4M "floppy" device, unmount any existing auto-mounted path,
# then mount it read-only at /mnt/floppy. Works in one run (no need to run twice).
#
# Usage:
#   sudo ./mount_floppy_autodetect.sh
#

set -e  # Exit on error

echo "=== Detecting floppy-like device (~1.4M) via lsblk ==="

# -----------------------------------------------------------------------------
# 1) Identify a disk with size "1.4M" in lsblk
# -----------------------------------------------------------------------------
FLOPPY_DEVICE_NAME=$(
  lsblk -lno NAME,TYPE,SIZE |
    awk '$2=="disk" && $3=="1.4M" {print $1; exit}'
)

if [[ -z "$FLOPPY_DEVICE_NAME" ]]; then
  echo "Error: No 1.4M disk device found in lsblk."
  echo "If your floppy is slightly different (e.g., 1.44M or 1.38M), adjust this script."
  exit 1
fi

DEVICE="/dev/$FLOPPY_DEVICE_NAME"
echo "Found device: $DEVICE"

# -----------------------------------------------------------------------------
# 2) Check if the device is mounted somewhere (including auto-mount)
#    We'll check lsblk's MOUNTPOINT field to catch any path (e.g. /media/moiz/2C92-CAD9)
# -----------------------------------------------------------------------------
EXISTING_MOUNTPOINT=$(
  lsblk -lno NAME,MOUNTPOINT | 
    awk -v dev="$FLOPPY_DEVICE_NAME" '$1==dev && $2!="" {print $2}'
)

# If that fails for some reason, we also look for the device in 'mount' output
# as a fallback. But usually the lsblk method is more reliable for Ubuntu auto-mount.
if [[ -z "$EXISTING_MOUNTPOINT" ]]; then
  # Attempt fallback check via 'mount'
  EXISTING_MOUNTPOINT=$(mount | awk -v dev="$DEVICE" '
      index($1, dev) != 0 {print $3; exit}
  ')
fi

# -----------------------------------------------------------------------------
# 3) If we found an existing mount, forcibly unmount it
# -----------------------------------------------------------------------------
if [[ -n "$EXISTING_MOUNTPOINT" ]]; then
  echo "Detected an existing mount at $EXISTING_MOUNTPOINT. Unmounting..."
  sudo umount "$EXISTING_MOUNTPOINT" || {
    echo "Failed to unmount $EXISTING_MOUNTPOINT."
    exit 1
  }
else
  echo "Device $DEVICE is not currently mounted elsewhere."
fi

# -----------------------------------------------------------------------------
# 4) Create mount point /mnt/floppy (if it doesn’t exist)
# -----------------------------------------------------------------------------
MOUNTPOINT="/mnt/floppy"
echo "Ensuring mount point exists: $MOUNTPOINT"
sudo mkdir -p "$MOUNTPOINT"

# -----------------------------------------------------------------------------
# 5) Attempt to set read-only at the block level
# -----------------------------------------------------------------------------
echo "Setting the device to read-only at block level (if supported): $DEVICE"
sudo blockdev --setro "$DEVICE" 2>/dev/null || {
  echo "Warning: blockdev --setro is not supported or failed."
}

# -----------------------------------------------------------------------------
# 6) Mount read-only
# -----------------------------------------------------------------------------
echo "Mounting $DEVICE at $MOUNTPOINT as read-only..."
sudo mount -t auto -o ro "$DEVICE" "$MOUNTPOINT"

# -----------------------------------------------------------------------------
# 7) Verify mount
# -----------------------------------------------------------------------------
echo "Verifying mount options..."
findmnt "$MOUNTPOINT" || {
  echo "Error: Could not verify the mount with findmnt."
  exit 1
}

echo "Check the OPTIONS column for 'ro' above."

# -----------------------------------------------------------------------------
# 8) Test that writing fails
# -----------------------------------------------------------------------------
echo "Attempting to write a test file (should fail in read-only mode)..."
TESTFILE="$MOUNTPOINT/test_write"
if touch "$TESTFILE" 2>/dev/null; then
  echo "Warning: Write test unexpectedly succeeded! Removing test file..."
  rm -f "$TESTFILE"
else
  echo "Write test failed as expected (read-only filesystem)."
fi

# -----------------------------------------------------------------------------
# 9) Done
# -----------------------------------------------------------------------------
echo "=== All done! ==="
echo "Device $DEVICE is now mounted at $MOUNTPOINT in read-only mode."
echo "You can read files safely without risking writes."
echo "To unmount:   sudo umount $MOUNTPOINT"
echo "To eject:     eject $DEVICE  (if supported)"
