# Automated Database Backups with Systemd Timers

This guide explains how to set up automated daily database backups on Unix/Linux servers using systemd timers.

## Overview

The `payrollctl database backup` command creates database backups using native database tools:
- **SQLite**: Copies the database file directly
- **PostgreSQL**: Uses `pg_dump` to create SQL dumps
- **MySQL**: Uses `mysqldump` to create SQL dumps

Backups are automatically named with timestamps (e.g., `coati_backup_20231213_140530.sql`).

## Prerequisites

### Database Clients

Ensure the appropriate database client is installed:

```bash
# For PostgreSQL
sudo apt-get install postgresql-client

# For MySQL/MariaDB
sudo apt-get install default-mysql-client

# SQLite (usually pre-installed)
sudo apt-get install sqlite3
```

### GoERP Payroll Installation

Install GoERP Payroll with the CLI tool:

```bash
pip install -e /path/to/goerp-payroll
```

This makes the `payrollctl` command available system-wide.

## Setting Up Systemd Timer

### 1. Create Backup Script

Create a backup script at `/usr/local/bin/coati-backup.sh`:

```bash
#!/bin/bash
# GoERP Payroll Database Backup Script

# Configuration
BACKUP_DIR="/var/backups/goerp-payroll"
RETENTION_DAYS=30
DATABASE_URL="${DATABASE_URL:-sqlite:////opt/goerp-payroll/goerp_payroll.db}"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Export DATABASE_URL for payrollctl
export DATABASE_URL

# Generate timestamped filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/coati_backup_$TIMESTAMP"

# Determine file extension based on database type
if [[ $DATABASE_URL == sqlite* ]]; then
    BACKUP_FILE="${BACKUP_FILE}.db"
elif [[ $DATABASE_URL == postgresql* ]] || [[ $DATABASE_URL == postgres* ]]; then
    BACKUP_FILE="${BACKUP_FILE}.sql"
elif [[ $DATABASE_URL == mysql* ]]; then
    BACKUP_FILE="${BACKUP_FILE}.sql"
fi

# Create backup
echo "Starting backup at $(date)"
/usr/local/bin/payrollctl database backup -o "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
    
    # Clean up old backups (keep last RETENTION_DAYS days)
    find "$BACKUP_DIR" -name "coati_backup_*" -type f -mtime +$RETENTION_DAYS -delete
    echo "Old backups cleaned up (retention: $RETENTION_DAYS days)"
else
    echo "Backup failed!" >&2
    exit 1
fi
```

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/coati-backup.sh
```

### 2. Create Systemd Service Unit

Create `/etc/systemd/system/coati-backup.service`:

```ini
[Unit]
Description=GoERP Payroll Database Backup
After=network.target

[Service]
Type=oneshot
User=coati
Group=coati
Environment="DATABASE_URL=postgresql://user:pass@localhost/goerp_payroll"
ExecStart=/usr/local/bin/coati-backup.sh
StandardOutput=journal
StandardError=journal

# Security hardening
PrivateTmp=yes
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/backups/goerp-payroll
```

**Important**: Update the `Environment` line with your actual database URL.

### 3. Create Systemd Timer Unit

Create `/etc/systemd/system/coati-backup.timer`:

```ini
[Unit]
Description=Daily GoERP Payroll Database Backup
Requires=coati-backup.service

[Timer]
# Run daily at 2:00 AM
OnCalendar=daily
OnCalendar=*-*-* 02:00:00

# If the system was off at 2:00 AM, run the backup 15 minutes after boot
Persistent=yes

[Install]
WantedBy=timers.target
```

### 4. Enable and Start the Timer

```bash
# Reload systemd to recognize new units
sudo systemctl daemon-reload

# Enable the timer (start on boot)
sudo systemctl enable coati-backup.timer

# Start the timer now
sudo systemctl start coati-backup.timer

# Check timer status
sudo systemctl status coati-backup.timer

# List all timers to verify it's scheduled
sudo systemctl list-timers coati-backup.timer
```

## Verification

### Test the Backup Manually

Run the service once to test:

```bash
sudo systemctl start coati-backup.service
```

Check the logs:

```bash
sudo journalctl -u coati-backup.service -n 50
```

Check the backup directory:

```bash
ls -lh /var/backups/goerp-payroll/
```

### Monitor Timer Execution

View timer status:

```bash
# When is the next backup scheduled?
systemctl list-timers coati-backup.timer

# View recent backup logs
journalctl -u coati-backup.service -since "7 days ago"
```

## Customization

### Change Backup Schedule

Edit the timer unit to change the schedule:

```bash
sudo systemctl edit coati-backup.timer
```

Examples:
- Every 6 hours: `OnCalendar=*-*-* 0/6:00:00`
- Twice daily (2 AM and 2 PM): `OnCalendar=*-*-* 02,14:00:00`
- Weekly on Sundays at 3 AM: `OnCalendar=Sun *-*-* 03:00:00`

After editing:

```bash
sudo systemctl daemon-reload
sudo systemctl restart coati-backup.timer
```

### Change Retention Period

Edit the backup script and modify `RETENTION_DAYS`:

```bash
sudo nano /usr/local/bin/coati-backup.sh
```

### Backup to Remote Location

Modify the backup script to copy backups to a remote server:

```bash
# Add to the end of coati-backup.sh
rsync -avz "$BACKUP_FILE" user@backup-server:/backups/goerp-payroll/
```

## Docker Deployments

For Docker deployments, you can use the host's cron or systemd timer to execute backups in the container:

### Docker Compose Example

```yaml
services:
  coati:
    image: goerp-payroll:latest
    volumes:
      - ./backups:/backups
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/coati
```

### Backup Script for Docker

```bash
#!/bin/bash
# Backup script for Docker deployment

CONTAINER_NAME="goerp-payroll"
BACKUP_DIR="/opt/goerp-payroll/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker exec "$CONTAINER_NAME" payrollctl database backup -o "/backups/coati_backup_$TIMESTAMP.sql"
```

## Troubleshooting

### Permission Denied

Ensure the `coati` user has write permissions to the backup directory:

```bash
sudo chown -R coati:coati /var/backups/goerp-payroll
sudo chmod 750 /var/backups/goerp-payroll
```

### Database Connection Errors

Verify the DATABASE_URL in the service file:

```bash
sudo systemctl edit coati-backup.service
```

Test the connection:

```bash
sudo -u coati DATABASE_URL="your_db_url" payrollctl database backup -o /tmp/test.sql
```

### Timer Not Running

Check if the timer is active:

```bash
sudo systemctl is-active coati-backup.timer
sudo systemctl is-enabled coati-backup.timer
```

View detailed status:

```bash
sudo systemctl status coati-backup.timer --full
```

## Security Considerations

1. **Protect Database Credentials**: Never store database passwords in plain text in scripts. Use environment files or secret management systems.

2. **Backup File Permissions**: Ensure backup files are only readable by authorized users:
   ```bash
   sudo chmod 600 /var/backups/goerp-payroll/*
   ```

3. **Encrypt Backups**: For sensitive data, encrypt backups:
   ```bash
   gpg --symmetric --cipher-algo AES256 backup_file.sql
   ```

4. **Off-site Backups**: Store backups in a different physical location or cloud storage.

## References

- [Systemd Timer Documentation](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)
- [PostgreSQL pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [MySQL mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
