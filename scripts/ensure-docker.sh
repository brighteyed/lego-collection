#!/bin/sh
# Ensure a Docker daemon is reachable, starting Docker Desktop or OrbStack
# (macOS), Docker Desktop (Windows, when run from Git Bash/WSL), or the
# docker service (Linux) if necessary. Exits 0 as soon as `docker info` succeeds.
set -e

if docker info >/dev/null 2>&1; then
    echo "Docker daemon is running."
    exit 0
fi

echo "Docker daemon not reachable, trying to start it..."

case "$(uname -s)" in
    Darwin)
        if [ -d "/Applications/OrbStack.app" ]; then
            echo "Starting OrbStack..."
            open -a OrbStack
        elif [ -d "/Applications/Docker.app" ]; then
            echo "Starting Docker Desktop..."
            open --background -a Docker
        else
            echo "Error: neither OrbStack nor Docker Desktop found in /Applications." >&2
            exit 1
        fi
        ;;
    MINGW* | MSYS* | CYGWIN*)
        # Docker Desktop on Windows, started from Git Bash / MSYS / Cygwin.
        DOCKER_EXE="/c/Program Files/Docker/Docker/Docker Desktop.exe"
        if [ -f "$DOCKER_EXE" ]; then
            echo "Starting Docker Desktop..."
            "$DOCKER_EXE" &
        else
            echo "Error: Docker Desktop not found at '$DOCKER_EXE'." >&2
            exit 1
        fi
        ;;
    Linux)
        if command -v systemctl >/dev/null 2>&1 && systemctl is-enabled docker >/dev/null 2>&1; then
            echo "Starting docker service (systemctl)..."
            sudo systemctl start docker
        elif command -v service >/dev/null 2>&1; then
            echo "Starting docker service (service)..."
            sudo service docker start
        else
            echo "Error: no supported way to start docker on this system." >&2
            echo "Try: sudo systemctl start docker  (or start Docker Desktop / podman manually)." >&2
            exit 1
        fi
        ;;
    *)
        echo "Error: unsupported platform '$(uname -s)'." >&2
        exit 1
        ;;
esac

# Wait (up to ~120s) for the daemon to accept connections.
i=0
until docker info >/dev/null 2>&1; do
    i=$((i + 1))
    if [ "$i" -ge 60 ]; then
        echo "Error: Docker daemon did not become ready within 120 seconds." >&2
        exit 1
    fi
    sleep 2
done

echo "Docker daemon is ready."
