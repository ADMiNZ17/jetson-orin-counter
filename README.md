# 🚀 Jetson Orin Nano - TensorRT Optimized Counter (Engine Branch)

> **⚠️ CRITICAL WARNING:** This branch is **HARDWARE LOCKED**.
> It contains a pre-compiled `yolov8n.engine` file that is specifically tuned for the **NVIDIA Jetson Orin Nano GPU**.
> * ❌ **DO NOT RUN** on Raspberry Pi, PC, or Jetson Nano (older).
> * ❌ **DO NOT RUN** on Jetson AGX Orin (the engine will fail).
> * ✅ **ONLY** for Jetson Orin Nano (8GB/4GB).

This project uses **TensorRT (FP32/FP16)** to achieve maximum FPS for bottle counting. It is configured with `show=True` to display live detection results on a connected monitor.

---

## 🛠️ Hardware Requirements

1.  **NVIDIA Jetson Orin Nano** (Developer Kit) - **REQUIRED**
2.  **Monitor/Display** (Connected via DisplayPort) - **REQUIRED** for `show=True`
3.  **USB Webcam** or **CSI Camera**
4.  **JetPack 6.x** installed.

## 🚀 Step 1: Connect to Your Jetson (SSH)

You don't need a monitor! You can control your Jetson remotely using SSH. Choose your preferred method below:

### 💻 Method A: Windows PowerShell (Easy)
1.  Connect your PC and Jetson to the same Wi-Fi network.
2.  Open **PowerShell** on your PC.
3.  Type the command below (replace `username` and `IP_ADDRESS`):
    ```powershell
    ssh username@192.168.x.x
    ```
4.  Enter your password when prompted.

### 📱 Method B: Termux (Android)
1.  Install **Termux** from the Google Play Store or F-Droid.
2.  Open Termux and install OpenSSH:
    ```bash
    pkg install openssh
    ```
3.  Connect to your Jetson:
    ```bash
    ssh username@192.168.x.x
    ```

### 🆚 Method C: VS Code (Best for Coding)
1.  Install the **Remote - SSH** extension in VS Code.
2.  Press `F1` and type `Remote-SSH: Connect to Host...`.
3.  Enter `username@192.168.x.x`.
4.  It will open a new window where you can edit files directly on the Jetson!

---

## 📥 Step 2: Installation

### 1. Clone the "Engine" Branch
We will clone only this specific optimized branch into your workspace.

```bash
# Clone the 'engine' branch specifically
git clone -b engine https://github.com/ADMiNZ17/jetson-orin-counter.git counter_ws

# Enter the directory
cd counter_ws
```
### 2. Run the Auto-Setup Script
I have provided a "One-Click" script (setup.sh) that will:

- Install Docker & Nvidia Container Runtime
- Install jtop (System Monitor)
- Configure GPU permissions
- Set up necessary folders

Run these commands:
```bash
chmod +x setup.sh
sudo ./setup.sh
```
### 3. Reboot (Critical!)
After the script finishes, you MUST reboot your Jetson to apply the new Docker permissions.
```bash
sudo reboot
```
## 🎬 Step 3: Running the Project
After rebooting, log back in and navigate to your workspace:
```bash
cd counter_ws
```
### Option A: Run Interactive Mode (Recommended)
This allows you to select between Live Camera or Video File mode using your keyboard.
```bash
sudo docker-compose run --rm camera-app
```
### How to use:
1. The menu will appear asking for input.
2. Type 1 for Live Camera.
3. Type 2 for Video File (enter filename when asked).
4. To stop, click the video window and press q or press Ctrl+C in the terminal.

### Option B: Run in Background
If you just want it to run without menus:
```bash
sudo docker-compose up
```
## 📊 Monitoring Performance
To check your GPU usage, temperature, and RAM while the AI is running, open a new terminal tab and run:
```bash
jtop
```
(Press ALL or GPU tabs to see the statistics)

## 📁 File Structure

| File | Description |
| :--- | :--- |
| `video_feed.py` | **Main Script:** Configured to use `.engine` model and `show=True` (GUI enabled). |
| `yolov8n.engine` | **TensorRT Engine:** High-performance binary model optimized **only** for Orin Nano. |
| `setup.sh` | **Installer:** Automated script to install Docker, Nvidia Runtime, and dependencies. |
| `docker-compose.yml` | **Config:** Maps the display and GPU for the container. |
| `Dockerfile` | **Build:** Blueprint for building the AI environment (Python + YOLO + Libraries). |

## ⚠️ Troubleshooting

**Q: "qt.qpa.xcb: could not connect to display"**
> **Fix:** The code is trying to open a window (`show=True`) but can't find a screen.
> 1. Ensure a monitor is plugged in.
> 2. Run `xhost +` in the terminal before starting.
> 3. If using SSH only (no monitor), you must edit `video_feed.py` and set `show=False`.

**Q: "Corrupted size vs. prev_size" (Crash at end)**
> **Fix:** This is a known TensorRT cleanup bug on Jetson. **Ignore it.** If the video saved successfully and the engine ran, the program worked.

**Q: "Engine plan file is not compatible"**
> **Fix:** You are likely running this on a different device (e.g., Orin NX or AGX). You must re-export the engine manually: `yolo export model=yolov8n.pt format=engine device=0`.

**Q: "Docker permission denied" error?**
> **Fix:** You forgot to reboot after running `setup.sh`. Run `sudo reboot` now.
