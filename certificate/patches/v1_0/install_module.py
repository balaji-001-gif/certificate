import frappe


def execute():
    """Ensure Certificate module exists after install."""
    if not frappe.db.exists("Module Def", "Certificate"):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Certificate",
            "app_name": "certificate",
        }).insert(ignore_permissions=True)
        frappe.db.commit()
