FROM python:3.10.13-bullseye

# Prevents .pyc files from being written to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures Python output is directly sent to terminal without being buffered
ENV PYTHONUNBUFFERED=1

# Update packages and install dependencies
RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y gettext \
  && apt-get install -y ca-certificates \
  && apt-get install -y wget \
  && apt-get install -y unzip \
  && apt-get install -y fonts-liberation \
  && apt-get install -y libasound2 \
  && apt-get install -y libatk-bridge2.0-0 \
  && apt-get install -y libatk1.0-0 \
  && apt-get install -y libatspi2.0-0 \
  && apt-get install -y libcups2 \
  && apt-get install -y libdbus-1-3 \
  && apt-get install -y libdrm2 \
  && apt-get install -y libgbm1 \
  && apt-get install -y libgtk-3-0 \
  && apt-get install -y libnspr4 \
  && apt-get install -y libnss3 \
  && apt-get install -y libu2f-udev \
  && apt-get install -y libvulkan1 \
  && apt-get install -y libxcomposite1 \
  && apt-get install -y libxdamage1 \
  && apt-get install -y libxfixes3 \
  && apt-get install -y libxkbcommon0 \
  && apt-get install -y libxrandr2 \
  && apt-get install -y xdg-utils \
  && apt-get install -y --reinstall ca-certificates \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

### install chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt-get install -y ./google-chrome-stable_current_amd64.deb \
  && rm google-chrome-stable_current_amd64.deb

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs

# Copy the 'requirements.txt' file from the local build context to the container's file system
COPY ./requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --default-timeout=300 -r /requirements.txt --no-cache-dir

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json package-lock.json* ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app/

# Default command to run on container start
CMD ["python", "main.py"]