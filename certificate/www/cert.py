import frappe

def get_context(context):
    context.no_cache = 1  # Force server to re-render every time
    
    cert_id = frappe.form_dict.get("id")
    if not cert_id:
        context.error = "No Certificate ID provided."
        return

    cert_id = cert_id.strip()
    
    try:
        # Using get_doc for most reliable data and permission bypass via ignore_permissions
        doc = frappe.get_doc("Certificate", cert_id)
        
        if doc.docstatus != 1:
            context.warning = "This certificate has not been officially issued yet."

        context.doc = doc
        context.title = f"Certificate: {doc.certificate_title}"
        
        # Pre-format dates for the template
        context.f_issue_date = frappe.utils.formatdate(doc.issue_date, "dd MMMM yyyy") if doc.issue_date else ""
        context.f_from_date = frappe.utils.formatdate(doc.from_date, "dd MMMM yyyy") if doc.from_date else ""
        context.f_to_date = frappe.utils.formatdate(doc.to_date, "dd MMMM yyyy") if doc.to_date else ""
        context.f_expiry_date = frappe.utils.formatdate(doc.expiry_date, "dd MMMM yyyy") if doc.expiry_date else ""
    
    except frappe.DoesNotExistError:
        context.error = f"Certificate {cert_id} was not found in the database."
    except Exception as e:
        context.error = f"An error occurred: {str(e)}"
