# Certificate Manager (v15)

Complete setup for issuing certificates with automatic QR code generation and a public verification page, fully compatible with Frappe/ERPNext v15.

## Features

- **Certificate DocType** — Full lifecycle management (Draft → Active → Expired/Revoked).
- **Auto QR Generation** — Automatically generates a QR code on submission that points to the public verification URL.
- **Public Verification Page** — Accessible at `/verify-certificate?id=CERT-XXXXX`, allowing anyone to verify authenticity.
- **Premium Print Format** — Elegant, bordered certificate layout ready for professional use.
- **Frappe v15 Optimized** — Uses `pyproject.toml` and modern asset building.

## Installation

```bash
# 1. Get the app into your bench
bench get-app certificate https://github.com/balaji-001-gif/certificate.git

# 2. Install on your site
bench --site your-site.com install-app certificate

# 3. Build assets (v15 requirement)
bench build --app certificate

# 4. Migrate and restart
bench --site your-site.com migrate
bench restart
```

## Usage

1.  Navigate to **Certificate** in the Awesome Bar.
2.  Create a new Certificate record.
3.  Fill in the details (Recipient, Issuing Authority, etc.).
4.  **Submit** the document. This triggers the QR code generation.
5.  Use the **Print** view to see the final certificate with the QR code.
6.  Scanning the QR code will lead to the public verification page on your site.

## Configuration

- **Naming Series**: Default is `CERT-.YYYY.-.#####`. You can customize this in the DocType settings.
- **Verification URL**: The URL is automatically constructed using your site's base URL.

## License

MIT
