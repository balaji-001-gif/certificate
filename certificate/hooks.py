app_name = "certificate"
app_title = "Certificate Manager"
app_publisher = "Seria Applied Research Pvt Ltd."
app_description = "Issue, track and verify certificates with QR code verification"
app_email = "admin@example.com"
app_license = "MIT"
app_version = "1.0.0"

required_apps = ["frappe", "erpnext"]

# DocType class controller
doc_events = {
    "Certificate": {
        "on_submit": "certificate.certificate.doctype.certificate.certificate.on_submit",
        "on_cancel": "certificate.certificate.doctype.certificate.certificate.on_cancel",
    }
}

# Fixtures loaded on bench migrate / install-app
fixtures = [
    {
        "doctype": "Module Def",
        "filters": [["module_name", "in", ["Certificate"]]]
    },
    {
        "doctype": "DocType",
        "filters": [["name", "in", ["Certificate"]]]
    },
    {
        "doctype": "Print Format",
        "filters": [["name", "in", ["Certificate"]]]
    },
]
app_include_js = []

doctype_js = {
    "Certificate": "public/js/certificate.js"
}
# Website
# Default discovery handles /verify-certificate
