import frappe

no_cache = 1

def get_context(context):
    cert_id = frappe.form_dict.get("id", "").strip()
    context.cert_id = cert_id
    context.certificate = None
    context.error = None

    if not cert_id:
        context.error = "No certificate ID provided."
        return

    try:
        cert = frappe.get_doc("Certificate", cert_id)
        if cert.docstatus != 1:
            context.error = "This certificate has not been issued or has been cancelled."
            return

        # Calculate duration
        duration = ""
        if cert.from_date and cert.to_date:
            diff = frappe.utils.date_diff(cert.to_date, cert.from_date)
            weeks = diff // 7
            if weeks > 0:
                duration = f"{weeks} weeks"
            else:
                duration = f"{diff} days"

        context.certificate = frappe._dict({
            "name": cert.name,
            "certificate_title": cert.certificate_title,
            "certificate_type": cert.certificate_type,
            "recipient_name": cert.recipient_name or cert.recipient,
            "recipient_type": cert.recipient_type,
            "issuing_authority": cert.issuing_authority,
            "issue_date": frappe.utils.formatdate(cert.issue_date, "dd-MM-yyyy"),
            "expiry_date": frappe.utils.formatdate(cert.expiry_date, "dd-MM-yyyy") if cert.expiry_date else None,
            "valid_until": frappe.utils.formatdate(cert.valid_until, "dd-MM-yyyy") if cert.valid_until else None,
            "from_date": frappe.utils.formatdate(cert.from_date, "dd-MM-yyyy") if cert.from_date else None,
            "to_date": frappe.utils.formatdate(cert.to_date, "dd-MM-yyyy") if cert.to_date else None,
            "duration": duration,
            "hours": cert.hours,
            "status": cert.status,
            "description": cert.description,
            "qr_code": cert.qr_code,
        })

    except frappe.DoesNotExistError:
        context.error = f"No certificate found with ID: {frappe.escape(cert_id)}"
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Certificate Verification Error")
        context.error = "An unexpected error occurred. Please try again."
