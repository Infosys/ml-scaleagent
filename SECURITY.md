# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The following versions are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of ML-Scaler seriously. If you discover a security vulnerability, please follow these steps:

### Please Do Not

- **Do not** open a public GitHub issue for security vulnerabilities
- **Do not** disclose the vulnerability publicly until it has been addressed

### Please Do

1. **Report privately** - Send details to the project maintainers via email or private message
2. **Include details** - Provide as much information as possible:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if you have one)
3. **Allow time** - Give maintainers reasonable time to address the issue before public disclosure

### What to Expect

- **Acknowledgment** - We will acknowledge your report within 48 hours
- **Updates** - We will keep you informed about our progress
- **Credit** - We will credit you in the security advisory (unless you prefer to remain anonymous)
- **Timeline** - We aim to address critical vulnerabilities within 7 days

## Security Best Practices

When deploying ML-Scaler, please follow these security best practices:

### Credentials Management

- Never commit `.env` files or credentials to version control
- Use environment variables for sensitive information
- Rotate credentials regularly
- Use Azure Key Vault or similar services for production deployments

### Database Security

- Use strong passwords for database connections
- Enable SSL/TLS for database connections
- Restrict database access to authorized networks only
- Regularly backup your database

### Kubernetes Security

- Use RBAC to limit access to Kubernetes resources
- Enable network policies to restrict pod-to-pod communication
- Scan Docker images for vulnerabilities before deployment
- Keep Kubernetes cluster and components up to date

### API Security

- Use HTTPS in production environments
- Implement rate limiting to prevent abuse
- Enable authentication and authorization
- Validate all input data
- Keep dependencies up to date

### Azure Security

- Use Managed Identities where possible instead of service principals
- Apply least privilege principle for service principal permissions
- Enable Azure AD authentication
- Monitor and audit access logs

## Security Updates

Security updates will be announced through:
- GitHub Security Advisories
- Release notes
- Repository notifications

## Dependencies

We regularly monitor and update dependencies to address known vulnerabilities. You can help by:
- Reporting outdated dependencies
- Submitting PRs to update vulnerable packages
- Running security scans on your deployments

## Compliance

This project handles deployment configurations that may include:
- Database connection strings
- API keys and tokens
- Cloud service credentials

Users are responsible for ensuring their deployment meets their organization's compliance requirements.

Thank you for helping keep ML-Scaler secure!
