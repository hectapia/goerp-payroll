# Nginx Reverse Proxy Configuration

This directory contains the nginx configuration for GoERP Payroll's production deployment.

## Features

- **Static file serving**: Serves CSS, JavaScript, and images directly from nginx (faster than WSGI)
- **Reverse proxy**: Forwards application requests to the Gunicorn WSGI server
- **HTTPS support**: Ready for Let's Encrypt SSL certificates
- **Security headers**: Implements best practices for web security
- **Long request timeout**: Configured for long-running payroll calculations (300s)

## Configuration Files

- `nginx.conf` - Main nginx configuration with HTTP and HTTPS server blocks
- `init-letsencrypt.sh` - Helper script to obtain Let's Encrypt SSL certificates

## Quick Start (HTTP only - Development/Testing)

The default configuration serves traffic over HTTP on port 80. This is suitable for development or internal networks.

```bash
docker-compose up -d
```

Access the application at: `http://localhost` or `http://your-server-ip`

## Production Setup with HTTPS (Let's Encrypt)

### Prerequisites

1. A domain name pointing to your server's IP address
2. Ports 80 and 443 open on your firewall

### Step 1: Update Configuration

1. Edit `nginx/nginx.conf`:
   - Replace `your-domain.com` with your actual domain name
   - Uncomment the HTTPS server block (lines starting with `# server {`)
   - Uncomment the HTTP to HTTPS redirect (line with `# return 301 https://...`)

2. Edit `docker-compose.yml`:
   - Uncomment the certbot service
   - Update the email and domain in the certbot command

### Step 2: Obtain SSL Certificates

Run the Let's Encrypt initialization script:

```bash
chmod +x nginx/init-letsencrypt.sh
./nginx/init-letsencrypt.sh your-domain.com your-email@example.com
```

This script will:
1. Create a temporary nginx configuration for the ACME challenge
2. Request certificates from Let's Encrypt
3. Restart nginx with the full SSL configuration

### Step 3: Start Services

```bash
docker-compose up -d
```

Your application will now be available at: `https://your-domain.com`

### Step 4: Enable Auto-Renewal

Certbot is configured to run twice daily and renew certificates that are within 30 days of expiration:

```bash
docker-compose logs certbot
```

## Configuration Details

### Static Files

Static files are served directly by nginx from `/usr/share/nginx/html/static/`:
- CSS files: `goerp_payroll/static/*.css`
- JavaScript files: `goerp_payroll/static/*.js`
- Images: `goerp_payroll/static/logo/*`

These files are:
- Cached for 30 days (`expires 30d`)
- Served without access logging (better performance)
- Marked as immutable (aggressive caching)

### Proxy Settings

Application requests are proxied to the Gunicorn server with:
- Read timeout: 300 seconds (for long payroll calculations)
- Connect timeout: 75 seconds
- Proper header forwarding (`X-Real-IP`, `X-Forwarded-For`, etc.)
- WebSocket support (if needed in the future)

### Security Headers

The HTTPS configuration includes:
- `X-Frame-Options: SAMEORIGIN` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-XSS-Protection: 1; mode=block` - Enables XSS protection
- HSTS (optional) - Forces HTTPS for future requests

## Troubleshooting

### Static files not loading

1. Check that the volume is mounted correctly:
   ```bash
   docker-compose exec nginx ls -la /usr/share/nginx/html/static/
   ```

2. Check nginx logs:
   ```bash
   docker-compose logs nginx
   ```

### SSL certificate errors

1. Verify your domain points to the correct IP:
   ```bash
   dig your-domain.com
   ```

2. Check certbot logs:
   ```bash
   docker-compose logs certbot
   ```

3. Ensure ports 80 and 443 are accessible from the internet

### Application not responding

1. Check that the web service is running:
   ```bash
   docker-compose ps web
   ```

2. Check nginx can reach the backend:
   ```bash
   docker-compose exec nginx wget -O- http://web:5000/health
   ```

## Manual Certificate Renewal

If automatic renewal fails, you can manually renew:

```bash
docker-compose run --rm certbot renew
docker-compose exec nginx nginx -s reload
```

## Customization

### Custom SSL Certificates

If you have your own SSL certificates (not Let's Encrypt):

1. Copy your certificates to the certbot volume:
   ```bash
   docker cp fullchain.pem <container>:/etc/letsencrypt/live/your-domain.com/
   docker cp privkey.pem <container>:/etc/letsencrypt/live/your-domain.com/
   ```

2. Update `nginx.conf` with the correct paths

### Additional Security

For enhanced security, consider:
- Enabling HSTS (uncomment in nginx.conf)
- Adding Content Security Policy (CSP) headers
- Implementing rate limiting
- Using fail2ban for brute force protection

## Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
