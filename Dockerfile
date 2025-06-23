FROM amazonlinux:2023

# Update system and install required packages
RUN dnf -y update && \
    dnf install -y --setopt=install_weak_deps=False --best --allowerasing \
    python3.11 \
    python3.11-pip \
    gcc \
    postgresql-devel \
    net-tools \
    nc \
    curl && \
    dnf clean all

# Configure Python and pip aliases
RUN alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    alternatives --install /usr/bin/pip pip /usr/bin/pip3.11 1

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
