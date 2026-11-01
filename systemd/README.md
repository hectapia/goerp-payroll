# Systemd Unit Files

This directory contains systemd service unit files for deploying GoERP Payroll on Linux systems using systemd.

## Architecture

The systemd deployment follows **Option 3** (separate processes) architecture:

- **Web Service** (`goerp-payroll.service`): Serves the Flask application
- **Worker Service** (`goerp-payroll-worker.service`): Processes background payroll jobs with Dramatiq

This separation provides:
- Independent scaling of web and worker components
- Fault isolation (worker failures don't affect web serving)
- Optimized resource allocation per component
- Standard production deployment pattern

## Files

- **goerp-payroll.service**: Main web application service
- **goerp-payroll-worker.service**: Dramatiq background worker service for processing payroll jobs

## Deployment Options

### Option A: Full Setup (Web + Worker + Background Processing)

Use **both** services for production deployments with background payroll processing:

- Web service handles HTTP requests
- Worker service processes large payroll calculations asynchronously
- Both services share the same database and Redis

**Recommended for**: Production environments with >100 employees per payroll

### Option B: Web Only (No Background Processing)

Use **only** the web service if background processing is not needed:

- Set `QUEUE_ENABLED=0` in the web service
- Do not install/start the worker service
- All payroll calculations execute synchronously

**Recommended for**: Small deployments with <100 employees per payroll

## Prerequisites

1. A Linux system with systemd (Ubuntu 16.04+, Debian 8+, CentOS 7+, etc.)
2. Redis server installed and running (required for background processing)
3. PostgreSQL or MySQL database server
4. Python 3.11+ with virtual environment
5. GoERP Payroll installed in `/home/coati/goerp-payroll` (adjust paths as needed)

## Installation

### 1. Prepare the Environment

```bash
# Create coati user
sudo useradd -m -s /bin/bash coati

# Switch to coati user
sudo su - coati

# Clone and setup the application
git clone https://github.com/williamjmorenor/coati-payroll.git
cd goerp-payroll
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit both service files to match your deployment:

- `DATABASE_URL`: Your database connection string
- `SECRET_KEY`: Generate with `python -c 'import secrets; print(secrets.token_hex(32))'`
- `ADMIN_USER` and `ADMIN_PASSWORD`: Initial admin credentials
- `REDIS_URL`: Your Redis connection string

### 3. Install Service Files

```bash
# Copy service files to systemd directory
sudo cp systemd/goerp-payroll.service /etc/systemd/system/
sudo cp systemd/goerp-payroll-worker.service /etc/systemd/system/

# Reload systemd to recognize new services
sudo systemctl daemon-reload
```

### 4. Enable and Start Services

```bash
# Enable services to start on boot
sudo systemctl enable goerp-payroll-worker
sudo systemctl enable goerp-payroll

# Start the worker first (to process any queued jobs)
sudo systemctl start goerp-payroll-worker

# Start the main application
sudo systemctl start goerp-payroll
```

### 5. Verify Services

```bash
# Check worker status
sudo systemctl status goerp-payroll-worker

# Check main application status
sudo systemctl status goerp-payroll

# View worker logs
sudo journalctl -u goerp-payroll-worker -f

# View application logs
sudo journalctl -u goerp-payroll -f
```

## Service Management

### Start Services

```bash
sudo systemctl start goerp-payroll-worker
sudo systemctl start goerp-payroll
```

### Stop Services

```bash
sudo systemctl stop goerp-payroll
sudo systemctl stop goerp-payroll-worker
```

### Restart Services

```bash
sudo systemctl restart goerp-payroll-worker
sudo systemctl restart goerp-payroll
```

### View Logs

```bash
# Real-time logs
sudo journalctl -u goerp-payroll -f
sudo journalctl -u goerp-payroll-worker -f

# Last 100 lines
sudo journalctl -u goerp-payroll -n 100
sudo journalctl -u goerp-payroll-worker -n 100
```

## Background Processing

The `goerp-payroll-worker.service` is **required** for background processing of large payrolls. When configured:

1. **Queue Enabled**: Set `QUEUE_ENABLED=1` in both service files
2. **Redis Available**: Redis must be running and accessible at `REDIS_URL`
3. **Threshold Met**: Payrolls with more than `BACKGROUND_PAYROLL_THRESHOLD` employees will process in background

If any condition is not met, payroll calculations will execute synchronously.

### Worker Configuration

Adjust worker capacity in `goerp-payroll-worker.service`:

```ini
Environment="DRAMATIQ_WORKER_THREADS=8"    # Threads per process
Environment="DRAMATIQ_WORKER_PROCESSES=2"  # Number of worker processes
```

**Recommendations**:
- For small servers: 4 threads, 1-2 processes
- For medium servers: 8 threads, 2-4 processes
- For large servers: 8-16 threads, 4-8 processes

## Troubleshooting

### Worker not processing jobs

1. Check Redis is running: `sudo systemctl status redis`
2. Verify Redis URL in both services matches
3. Check worker logs: `sudo journalctl -u goerp-payroll-worker -f`
4. Restart worker: `sudo systemctl restart goerp-payroll-worker`

### Application not starting

1. Check service status: `sudo systemctl status goerp-payroll`
2. View error logs: `sudo journalctl -u goerp-payroll -xe`
3. Verify database is accessible
4. Check file permissions: `ls -la /home/coati/goerp-payroll`

### Database connection errors

1. Verify `DATABASE_URL` is correct in service file
2. Test database connection manually
3. Check database server is running
4. Verify network connectivity

## Security Considerations

Both service files include basic security hardening:

- `NoNewPrivileges=true`: Prevents privilege escalation
- `PrivateTmp=true`: Isolates /tmp directory
- Services run as dedicated `coati` user (not root)

For production deployments, consider additional hardening:

1. Use a reverse proxy (nginx/Apache) with HTTPS
2. Configure firewall rules
3. Implement rate limiting
4. Regular security updates
5. Database connection over SSL
6. Redis authentication

## See Also

- [Installation Guide](../docs/instalacion/instalacion.md)
- [Queue System Documentation](../docs/queue_system.md)
- [Background Processing](../docs/background-payroll-processing.md)
