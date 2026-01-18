# Base image for Jetson Orin Nano (JetPack 6)
FROM dustynv/l4t-pytorch:r36.2.0

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Install YOLOv8 and Tracking dependencies
RUN pip3 install --no-cache-dir --index-url https://pypi.org/simple \
    "numpy<2" \
    ultralytics \
    supervision \
    lapx \
    shapely

# Set working directory to allow easy file mapping
WORKDIR /app

CMD ["/bin/bash"]