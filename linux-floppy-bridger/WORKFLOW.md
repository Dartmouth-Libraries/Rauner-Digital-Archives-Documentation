# Workflow Guide for Floppy Disk Auto-Mount Tool

This document outlines the typical workflow for using the `mount_floppy_autodetect.sh` script and describes the development workflow for contributors.

## User Workflow

### 1. Preparation

Before using the script, ensure:
- Your floppy drive is properly connected to your Linux system
- You have a floppy disk ready to be mounted
- You have sudo/root privileges on your system

### 2. Mounting Process

The typical workflow for mounting a floppy disk is:

1. **Insert the floppy disk** into your floppy drive
2. **Run the script** with sudo privileges:
   ```bash
   sudo ./mount_floppy_autodetect.sh
   ```
3. **Wait for completion** - the script will:
   - Detect the floppy device
   - Unmount it if already mounted elsewhere
   - Mount it read-only at `/mnt/floppy`
   - Verify the mount is working and read-only

4. **Access your files** at `/mnt/floppy`:
   ```bash
   ls -la /mnt/floppy
   ```

### 3. After Use

When you're done with the floppy disk:

1. **Unmount the disk**:
   ```bash
   sudo umount /mnt/floppy
   ```

2. **Eject the disk** (if supported by your hardware):
   ```bash
   eject /dev/sdX  # Replace with your actual device name
   ```

3. **Physically remove** the floppy disk from the drive

## Development Workflow

For contributors who want to improve the script, here's the recommended workflow:

### 1. Setup Development Environment

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/yourusername/mount-floppy-autodetect.git
   cd mount-floppy-autodetect
   ```

2. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 2. Development Process

1. **Make your changes** to the script using your preferred text editor
   
2. **Test your changes** with real hardware if possible, or using virtual floppy devices:
   ```bash
   # Create a virtual floppy image for testing
   dd if=/dev/zero of=floppy.img bs=1024 count=1440
   mkfs.vfat floppy.img
   
   # Mount the virtual floppy for testing
   sudo losetup /dev/loop0 floppy.img
   
   # Test your script
   sudo ./mount_floppy_autodetect.sh
   ```

3. **Verify** that your changes work as expected and don't break existing functionality

### 3. Code Quality

Before submitting your changes:

1. **Run shellcheck** to ensure your bash script follows best practices:
   ```bash
   shellcheck mount_floppy_autodetect.sh
   ```

2. **Test on different Linux distributions** if possible

3. **Document your changes** in comments and update the README.md if necessary

### 4. Contribution Process

1. **Commit your changes** with a clear message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** against the main repository

4. **Respond to feedback** from maintainers and make any requested changes

## Troubleshooting Workflow

If you encounter issues with the script:

1. **Check system logs** for mount-related errors:
   ```bash
   dmesg | grep -i floppy
   journalctl -xe
   ```

2. **Verify device detection**:
   ```bash
   lsblk
   fdisk -l
   ```

3. **Test manual mounting** to isolate script issues:
   ```bash
   sudo mount -o ro /dev/sdX /mnt/floppy
   ```

4. **Report issues** with detailed information:
   - Linux distribution and version
   - Output of the script with any error messages
   - Hardware details (floppy drive model if known)
   - Steps to reproduce the issue

## Release Workflow

For maintainers handling releases:

1. **Update version number** in the script (if applicable)
2. **Update documentation** with any new features or changes
3. **Tag the release** with semantic versioning:
   ```bash
   git tag -a v1.0.1 -m "Version 1.0.1"
   git push origin v1.0.1
   ```
4. **Create a GitHub release** with release notes

## Continuous Integration

Future improvements could include:
- GitHub Actions for automated testing
- ShellCheck integration for code quality
- Automated testing with virtual floppy devices
