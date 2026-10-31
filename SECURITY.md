# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers (see repository for contact)
3. Include detailed description
4. Allow reasonable time for response
5. Do not disclose publicly until fixed

## Security Features

### Authentication
- Admin endpoints protected by token
- Session-based authentication for experiments
- No password storage (anonymous participants)

### Authorization
- Admin token required for sensitive operations
- Participants can only access their own session
- No privilege escalation possible

### Data Protection
- No PII collection
- Anonymous session tokens
- Local storage only
- No external transmission

### Input Validation
- Pydantic schemas for all inputs
- SQL injection prevention (parameterized queries)
- XSS prevention (Jinja2 autoescape)
- CSRF protection

### Security Headers
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- X-XSS-Protection

### Rate Limiting
- In-memory rate limiting per session
- Configurable limits
- No IP-based tracking

## Known Limitations

- Admin token is simple string comparison
- Rate limiting resets on server restart
- No DDoS protection
- No WAF or advanced security

## Best Practices

### For Developers
1. Never commit secrets
2. Use environment variables
3. Validate all inputs
4. Follow secure coding practices
5. Keep dependencies updated

### For Deployers
1. Change SECRET_KEY in production
2. Use HTTPS
3. Set secure cookies
4. Enable admin authentication
5. Regular security updates
6. Monitor logs

### For Researchers
1. Protect participant privacy
2. Follow data protection laws
3. Secure database backups
4. Limit access to sensitive data
5. Report incidents promptly

## Compliance

- Designed with GDPR principles
- Privacy by design
- Minimal data collection
- No cross-border transfer

## Security Updates

- Monitor GitHub security advisories
- Update dependencies regularly
- Apply security patches promptly
- Test updates before deployment

## Contact

For security issues:
- Email: See repository
- GitHub: Private vulnerability reporting
- Response time: Within 48 hours

---

**Last Updated**: 2026-10-31
