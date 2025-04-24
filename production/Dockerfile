FROM manimcommunity/manim:stable

# Use root for package installation
USER root

# Install ffmpeg and espeak-ng only (minimal install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# (Optional) Switch back to the default user
# If the base image defines a safe user (e.g., manim), uncomment the line below
# USER manim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

CMD ["python", "-u", "main.py"]