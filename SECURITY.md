# Security Documentation

This document outlines the security measures implemented in the Khanqah Yaseen Zai backend.

## Security Features

### 1. File Upload Security

#### Validation Layers
- **Extension Validation**: Only allowed file extensions are accepted
- **MIME Type Validation**: Files are checked to ensure MIME type matches extension
- **File Signature Validation**: Binary file headers are verified (prevents file type spoofing)
- **Size Limits**: Strict file size limits enforced
- **Filename Sanitization**: Dangerous characters and path components are removed

#### Allowed File Types
- **PDFs**: `.pdf` (max 50MB)
- **Images**: `.jpg`, `.jpeg`, `.png`, `.webp` (max 5MB)
- **Audio**: `.mp3`, `.wav`, `.m4a`, `.ogg` (max 100MB)

### 2. Media File Serving Security

The custom media file serving view (`serve_media_file`) includes:
- **Directory Traversal Protection**: Prevents access to files outside MEDIA_ROOT
- **Extension Whitelist**: Only serves files with allowed extensions
- **Request Logging**: All file access attempts are logged
- **IP Tracking**: Client IP addresses are logged for security monitoring
- **Error Handling**: Secure error messages that don't leak system information

### 3. Security Headers

All responses include security headers:

- **X-Content-Type-Options**: `nosniff` - Prevents MIME type sniffing
- **X-XSS-Protection**: `1; mode=block` - Enables browser XSS filter
- **Referrer-Policy**: Controls referrer information leakage
- **Permissions-Policy**: Restricts browser features (geolocation, camera, etc.)
- **Content-Security-Policy (CSP)**: Configurable CSP to prevent XSS attacks
- **Strict-Transport-Security (HSTS)**: Forces HTTPS in production

### 4. Authentication & Authorization

- **JWT Authentication**: Secure token-based authentication
- **Token Blacklisting**: Revoked tokens are blacklisted
- **Token Rotation**: Refresh tokens are rotated on use
- **Password Validation**: Strong password requirements enforced

### 5. Rate Limiting

- **API Rate Limits**: 
  - Anonymous: 100 requests/hour
  - Authenticated: 1000 requests/hour
- **Contact Form**: 5 submissions/hour per IP
- **Configurable**: Rates can be adjusted via environment variables

### 6. CORS & CSRF Protection

- **CORS**: Strict origin whitelist (configurable)
- **CSRF**: Enabled for all state-changing operations
- **Trusted Origins**: Configurable trusted origins for CSRF

### 7. Security Monitoring

#### Security Middleware
The `SecurityMiddleware` logs:
- Admin access attempts
- Suspicious request patterns (SQL injection, XSS attempts)
- 403/404 responses (potential scanning)
- Security-related events

#### Logging
- All security events are logged to `logs/django.log`
- Log levels: INFO, WARNING, ERROR
- IP addresses are tracked for security incidents

### 8. Input Validation

- **Serializer Validation**: All inputs validated via DRF serializers
- **SQL Injection Prevention**: Django ORM prevents SQL injection
- **XSS Prevention**: Template auto-escaping enabled
- **Path Traversal Prevention**: File paths are sanitized and validated

### 9. Production Security Settings

When `DEBUG=False`, additional security measures are enabled:

- **HTTPS Enforcement**: `SECURE_SSL_REDIRECT = True`
- **Secure Cookies**: `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`
- **HSTS**: Strict Transport Security enabled
- **X-Frame-Options**: Set to `DENY` (no iframe embedding)
- **Stricter CSP**: More restrictive Content Security Policy

## Security Best Practices

### Development
1. Never commit `.env` files
2. Use strong `SECRET_KEY` in production
3. Keep `DEBUG=False` in production
4. Use environment variables for sensitive data
5. Regularly update dependencies

### Production Deployment
1. Use HTTPS (SSL/TLS certificates)
2. Configure proper `ALLOWED_HOSTS`
3. Set up firewall rules
4. Use a reverse proxy (nginx/Apache)
5. Enable database backups
6. Monitor logs regularly
7. Keep Django and dependencies updated

### File Uploads
1. Always validate file types and sizes
2. Store uploads outside web root when possible
3. Use unique filenames to prevent overwrites
4. Scan uploaded files for malware (consider adding ClamAV)
5. Limit file access to authenticated users when appropriate

### API Security
1. Use authentication for sensitive endpoints
2. Implement rate limiting
3. Validate all inputs
4. Use HTTPS in production
5. Monitor API usage for anomalies

## Security Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS for production domain
- [ ] Set up proper database backups
- [ ] Configure email settings
- [ ] Review and adjust rate limits
- [ ] Set up log rotation
- [ ] Configure firewall rules
- [ ] Enable security monitoring
- [ ] Test file upload security
- [ ] Review and test all API endpoints
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Document security procedures

## Incident Response

If a security incident occurs:

1. **Immediate Actions**:
   - Change `SECRET_KEY`
   - Review logs for suspicious activity
   - Check for unauthorized file uploads
   - Review database for unauthorized changes

2. **Investigation**:
   - Check security logs in `logs/django.log`
   - Review access logs
   - Identify affected systems/data
   - Document the incident

3. **Remediation**:
   - Patch vulnerabilities
   - Revoke compromised tokens
   - Reset affected user passwords
   - Restore from backups if needed

4. **Prevention**:
   - Update security measures
   - Review and improve monitoring
   - Conduct security audit
   - Update documentation

## Dependencies

### Security-Related Packages
- `django-cors-headers`: CORS management
- `djangorestframework-simplejwt`: JWT authentication
- `python-decouple`: Secure environment variable management
- `django-ratelimit`: Rate limiting (if used)

### Optional Security Enhancements
- `python-magic`: Better MIME type detection (install: `pip install python-magic-bin` on Windows)
- `django-axes`: Login attempt monitoring
- `django-ratelimit`: Advanced rate limiting
- `django-csp`: Content Security Policy management

## Reporting Security Issues

If you discover a security vulnerability, please:
1. Do not create a public issue
2. Contact the project maintainers privately
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed before disclosure

## References

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django REST Framework Security](https://www.django-rest-framework.org/topics/security/)

