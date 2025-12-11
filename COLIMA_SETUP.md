# Colima Setup Guide

## What is Colima?

**Colima** (Containers on Lima) is a lightweight alternative to Docker Desktop. It provides:
- ✅ Docker-compatible API (works with all Docker commands)
- ✅ Much lighter resource usage than Docker Desktop
- ✅ No GUI overhead
- ✅ Free and open source
- ✅ Works on Mac and Linux

## Installation

### macOS (using Homebrew)

```bash
# Install Colima and Docker CLI
brew install colima docker

# Start Colima
colima start
```

That's it! Colima will download a Linux VM image on first start (one-time download).

## Usage

Once Colima is running, use Docker commands exactly as you would with Docker Desktop:

```bash
# Check Docker is working
docker ps

# Build images
docker build -t my-image .

# Run containers
docker run --rm my-image

# Everything works the same!
```

## Managing Colima

```bash
# Start Colima
colima start

# Stop Colima
colima stop

# Check status
colima status

# View logs
colima logs

# Delete and recreate (if needed)
colima delete
colima start
```

## Resource Configuration

By default, Colima uses:
- 2 CPU cores
- 2GB RAM
- 60GB disk

To customize (before first start):

```bash
# Set custom resources
colima start --cpu 4 --memory 8

# Or edit config after creation
colima edit
```

## Benefits Over Docker Desktop

| Feature | Docker Desktop | Colima |
|--------|---------------|--------|
| Resource Usage | Heavy (~2GB RAM) | Light (~500MB RAM) |
| GUI Required | Yes | No |
| Startup Time | Slow | Fast |
| Cost | Free (with limits) | Free |
| CLI Only | No | Yes |

## Troubleshooting

### Docker daemon not running
```bash
# Make sure Colima is started
colima status

# If not running, start it
colima start
```

### Permission issues
Colima handles permissions automatically, but if you have issues:
```bash
# Check Colima is running
colima status

# Restart if needed
colima restart
```

### Switching from Docker Desktop

If you had Docker Desktop installed:
1. Stop Docker Desktop
2. Install Colima: `brew install colima docker`
3. Start Colima: `colima start`
4. Use Docker commands as normal!

The Docker context will automatically switch to Colima.

