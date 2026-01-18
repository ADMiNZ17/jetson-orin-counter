import cv2
import os
import sys
from ultralytics import solutions, YOLO

# --- STUDENT INFORMATION HEADER ---
def print_student_info():
    print("\n" + "="*50)
    print("      UNIVERSITI TUN HUSSEIN ONN MALAYSIA")
    print("="*50)
    print(f" Name    : Ahmad Adham bin Azhar (a.k.a. Adam)")
    print(f" Matrix  : CE210228")
    print(f" Email   : ce210228@student.uthm.edu.my")
    print("="*50 + "\n")

# --- UTILITY: GET UNIQUE OUTPUT FILENAME ---
def get_unique_filename(base_name="output", ext=".mp4"):
    counter = 1
    filename = f"{base_name}{counter}{ext}"
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_name}{counter}{ext}"
    return filename

def main():
    print_student_info()

    # --- STEP 1: ASK USER FOR MODE ---
    print("Select Detection Mode:")
    print(" [1] Live Camera (Webcam/CSI)")
    print(" [2] Video File Input")
    
    # Use sys.stdin.readline to be safer in Docker environments
    try:
        mode = input("\nEnter choice (1 or 2): ").strip()
    except EOFError:
        print("Error: Input stream closed. Make sure you run with 'stdin_open: true' or '-it'.")
        return
    
    video_source = 0  # Default to camera
    
    if mode == '2':
        fname = input("Enter video filename (e.g., test.mp4): ").strip()
        if os.path.exists(fname):
            video_source = fname
        else:
            print(f"Error: File '{fname}' not found!")
            return
    elif mode == '1':
        video_source = 0
    else:
        print("Invalid selection. Exiting.")
        return

    # --- STEP 2: SETUP MODEL & OUTPUT ---
    model_path = "yolov8n.pt"
    output_filename = get_unique_filename("output")
    
    print(f"\n[INFO] Source: {video_source}")
    print(f"[INFO] Saving to: {output_filename}")
    print(f"[INFO] Loading Model: {model_path}...")

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error opening video source.")
        return

    # Force resolution for camera (optional, safer for Jetson)
    if mode == '1':
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) if mode == '2' else 30

    # Video Writer
    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    # Center Line Configuration
    line_x = w // 2
    line_points = [(line_x, 0), (line_x, h)]
    
    # Init Object Counter
    counter = solutions.ObjectCounter(
        show=True,
        region=line_points,
        model=model_path,
        classes=[39], # 39 = Bottle
        show_in=True,
        show_out=True,
        line_width=2
    )

    print("\n[INFO] Processing started... Press 'q' to stop.")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("End of video or read error.")
                break

            # --- SMART COUNTING LOGIC (The Fix) ---
            try:
                # 1. Latest API (Callable Object)
                if callable(counter) and not hasattr(counter, 'count') and not hasattr(counter, 'start_counting'):
                    result = counter(frame)
                    if hasattr(result, 'plot_im'): 
                        frame = result.plot_im 
                    elif isinstance(result, type(frame)):
                        frame = result         
                    else:
                        pass 

                # 2. Recent API (.count method)
                elif hasattr(counter, 'count'):
                    frame = counter.count(frame)

                # 3. Old API (.start_counting method)
                elif hasattr(counter, 'start_counting'):
                    # Load model manually if needed for old API
                    model = YOLO(model_path) 
                    tracks = model.track(frame, persist=True, show=False, verbose=False, conf=0.25)
                    frame = counter.start_counting(frame, tracks)

                else:
                    print("\nCRITICAL ERROR: Ultralytics API has changed significantly.")
                    break

            except Exception as e:
                print(f"\nError inside counting loop: {e}")
                break

            # --- RED DOT DRAWING ---
            # Re-run inference briefly to get coordinates for the red dot
            # (We use a try-block so this doesn't crash the video if it fails)
            try:
                # We can access the model attached to the counter for inference
                results = counter.model(frame, verbose=False, classes=[39], conf=0.25)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Get Box Coordinates
                        b = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                        
                        # Calculate Center
                        cx = int((x1 + x2) / 2)
                        cy = int((y1 + y2) / 2)
                        
                        # Draw Red Dot
                        cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
            except Exception:
                pass 

            # Write to file
            video_writer.write(frame)

            # Optional: Show if GUI is available
            # cv2.imshow("Detection", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'): break

    except KeyboardInterrupt:
        print("\nStopping...")

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    print(f"\n[SUCCESS] Video saved as: {output_filename}")

if __name__ == "__main__":
    main()