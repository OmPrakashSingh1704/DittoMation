# Security Policy

## Supported Versions

The latest released version of DittoMation is actively supported. We recommend always using the most recent version available on PyPI.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly by:

- **Opening a private GitHub Security Advisory** at https://github.com/OmPrakashSingh1704/DittoMation/security/advisories/new, or
- **Emailing the maintainer directly** (see GitHub profile for contact information)

### What to Include in Your Report

Please include as much information as possible:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)

### Response Timeline

We will acknowledge reports within 72 hours and aim to provide a fix or mitigation plan within 30 days for confirmed vulnerabilities.

## Security Best Practices

When using DittoMation:

1. **Keep dependencies updated**: Regularly update to the latest version
2. **Validate user inputs**: If using DittoMation in automated systems, validate and sanitize any user-provided commands or workflows
3. **Secure ADB access**: Ensure ADB debugging is only enabled when needed and on trusted networks
4. **Review workflow files**: Inspect JSON workflow files before executing them, especially from untrusted sources

## Known Security Considerations

DittoMation interacts with Android devices via ADB (Android Debug Bridge). This requires:

- USB debugging to be enabled on the target device
- Proper permissions and device authorization
- Network security when using ADB over network

These are standard requirements for Android automation tools and do not represent vulnerabilities in DittoMation itself.

## Security Audit Status

As of the latest release:
- No known CVEs or security vulnerabilities
- Dependencies audited with `pip-audit`
- Code scanned with `bandit` security linter
- Regular dependency updates via automated tools

For any security concerns or questions, please open a GitHub issue or contact the maintainers directly.
