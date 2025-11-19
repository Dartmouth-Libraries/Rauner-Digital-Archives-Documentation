# Floppy Disk Auto-Mount Tool

**Part of the Rauner Digital Archives Project**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A robust bash script for automatically detecting, unmounting (if necessary), and safely mounting floppy disks in read-only mode on Linux systems.

## Overview

The `mount_floppy_autodetect.sh` script provides a reliable solution for working with legacy floppy disks on modern Linux systems. It automatically detects a 1.4MB floppy disk device, forcibly unmounts any previously mounted location (including auto-mounted paths), and remounts it as read-only at `/mnt/floppy`. This is ideal for preserving legacy data from old floppy disks without the risk of accidental writes.

## Implementation Details

The script performs the following operations in one seamless run:

1. **Device Detection**: Identifies the floppy disk by checking for ~1.4M devices using `lsblk`
2. **Mount Point Detection**: Checks for existing mountpoints, including auto-mounted locations
3. **Smart Unmounting**: Unmounts the device if already mounted using `umount`
4. **Mount Point Preparation**: Creates the `/mnt/floppy` mountpoint if it doesn't exist
5. **Block-Level Protection**: Sets the device to read-only using `blockdev --setro`
6. **Safe Mounting**: Mounts the device read-only at `/mnt/floppy`
7. **Mount Verification**: Confirms mount status using `findmnt`
8. **Write Protection Test**: Performs a write test, which should fail on a read-only filesystem
9. **User Feedback**: Outputs success information, including tips for unmounting and ejecting

## Usage

### Prerequisites

- You must have root privileges (use `sudo`) to mount devices
- Your floppy device must be connected and appear as a ~1.4M disk in `lsblk`

### Basic Usage

```bash
sudo ./mount_floppy_autodetect.sh
```

This will:
- Detect the appropriate device (e.g., `/dev/sdX`)
- Unmount it if it's already mounted elsewhere (like `/media/youruser/XXXX`)
- Mount it read-only at `/mnt/floppy`
- Confirm the mount worked and is read-only
- Attempt a write test (which should fail)

### After Mounting

**Browse contents:**
```bash
ls /mnt/floppy
```

**Unmount when done:**
```bash
sudo umount /mnt/floppy
```

**Eject the floppy (if supported):**
```bash
eject /dev/sdX  # Replace with actual device name (e.g., /dev/sdb)
```

## Installation

### Setup on a Different Linux Machine

1. **Install Required Packages**

   Ensure the following commands are available:
   ```bash
   sudo apt update
   sudo apt install util-linux mount eject coreutils
   ```

   For other distributions, use the appropriate package manager:
   ```bash
   # Fedora/RHEL/CentOS
   sudo dnf install util-linux mount eject coreutils
   
   # Arch Linux
   sudo pacman -S util-linux eject coreutils
   ```

2. **Clone or Copy Script**

   Option A: Clone from repository:
   ```bash
   git clone https://github.com/yourusername/mount-floppy-autodetect.git
   cd mount-floppy-autodetect
   ```

   Option B: Download directly:
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/mount-floppy-autodetect/main/mount_floppy_autodetect.sh
   ```

3. **Set Permissions**

   Make the script executable:
   ```bash
   chmod +x mount_floppy_autodetect.sh
   ```

4. **Run the Script**

   ```bash
   sudo ./mount_floppy_autodetect.sh
   ```

5. **Optional: Add User to Disk Group**

   On some systems, you may need to add your user to the disk group:
   ```bash
   sudo usermod -aG disk yourusername
   ```
   (Requires logout/login to take effect)

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Linux (Debian, Ubuntu, Fedora, CentOS, Arch, etc.) |
| Shell | Bash |
| Privileges | Root / sudo access |
| Tools Used | lsblk, awk, mount, umount, blockdev, findmnt, eject, touch, mkdir, rm |
| Storage Device | External or internal floppy drive (1.4MB recognized via lsblk) |

## Troubleshooting

### No Floppy Device Detected

If the script reports "No 1.4M disk device found in lsblk", check:
- Is the floppy disk properly inserted?
- Is the floppy drive connected and powered?
- Does your floppy have a slightly different size? You may need to modify the script to look for "1.44M" or similar.

### Permission Issues

If you encounter permission errors:
- Make sure you're running the script with `sudo`
- Check that the script has execute permissions (`chmod +x mount_floppy_autodetect.sh`)

### Mount Failures

If mounting fails:
- The floppy might be damaged or unformatted
- The filesystem might not be recognized (try specifying `-t vfat` or another filesystem type)
- The device might be busy (try running the script again)

## Notes

- Only works for devices exactly listed as 1.4M in lsblk. You can modify the size check (awk '$3=="1.4M"') if your media reports 1.44M, 1.38M, etc.
- Some virtual floppy disks or USB floppy drives may report slightly different sizes.

## Uninstallation

To remove this script, simply delete the file:

```bash
rm mount_floppy_autodetect.sh
```

## Contributing

PRs and suggestions are welcome! Make sure to test on real or virtual hardware before submitting fixes.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [WORKFLOW.md](WORKFLOW.md) for detailed development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the challenges of working with legacy media in modern systems
- Thanks to the Linux community for maintaining support for legacy hardware
