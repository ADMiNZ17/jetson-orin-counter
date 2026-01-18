# Jetson Orin Nano - Smart Bottle Counter 🍼🤖

This project is a Computer Vision application designed for the **NVIDIA Jetson Orin Nano**. It uses **YOLOv8** and **Docker** to detect, track, and count bottles in real-time. It supports both live camera feeds and video files, with automatic saving features.

## 🛠️ Hardware Requirements

Before you begin, ensure you have the following:

1.  **NVIDIA Jetson Orin Nano** (Developer Kit)
2.  **microSD Card** (Minimum 64GB recommended, flashed with JetPack 6.x)
3.  **USB Webcam** or **CSI Camera** (e.g., Raspberry Pi Camera V2)
4.  **Power Supply** (USB-C PD or DC Barrel Jack)
5.  **Internet Connection** (Ethernet or Wi-Fi)

---

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

Once logged into your Jetson terminal, follow these steps to set up the entire environment.

### 1. Clone this Repository
Download the project code to your Jetson.
```bash
# Clone the repo into a folder named 'counter_ws'
git clone [https://github.com/ADMiNZ17/jetson-orin-counter.git](https://github.com/ADMiNZ17/jetson-orin-counter.git) counter_ws

# Enter the directory
cd counter_ws
```

### 2. Run the Auto-Setup Script
I have provided a "One-Click" script (setup.sh) that will:

- Install Docker & Nvidia Container Runtime
- Install jtop (System Monitor)
- Configure GPU permissions
- Set up necessary folders
- Run these commands:
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
| `video_feed.py` | **Main Script:** Handles camera input, YOLO detection, counting logic, and video saving. |
| `setup.sh` | **Installer:** Automated script to install Docker, Nvidia Runtime, and dependencies. |
| `docker-compose.yml` | **Config:** Defines the container settings, GPU access, and devices. |
| `Dockerfile` | **Build:** Blueprint for building the AI environment (Python + YOLO + Libraries). |

## ⚠️ Troubleshooting

**Q: "Docker permission denied" error?**
> **Fix:** You forgot to reboot after running `setup.sh`. Run `sudo reboot` now.

**Q: Camera not opening / Source 0 failed?**
> **Fix:**
> 1. Ensure your USB camera is plugged in.
> 2. Run `ls /dev/video*` to see if `video0` exists.
> 3. If using a CSI camera (Raspberry Pi cam), you may need to enable `nvarguscamerasrc`.

**Q: The download is stuck or slow?**
> **Fix:** The first time you run Docker, it downloads a large image (approx 4-6GB). This depends on your internet speed. Be patient; subsequent runs will be instant.

**Q: Error "ObjectCounter object has no attribute count"?**
> **Fix:** Ensure you are using the latest `video_feed.py` provided in this repo, which contains the fix for the newest Ultralytics API.
