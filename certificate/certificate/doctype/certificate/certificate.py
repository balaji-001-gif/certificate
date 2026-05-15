import frappe
import qrcode
import io
from frappe.model.document import Document
from frappe.utils.file_manager import save_file


class Certificate(Document):

    def on_submit(self):
        self.db_set("status", "Active")
        self.status = "Active"
        self.generate_qr_code()

    def on_cancel(self):
        self.db_set("status", "Revoked")

    def generate_qr_code(self):
        try:
            site_url = frappe.utils.get_url()
            verify_url = f"{site_url}/verify-certificate?id={self.name}"

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(verify_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Remove old QR file if exists
            if self.qr_code:
                try:
                    old = frappe.get_doc("File", {
                        "file_url": self.qr_code,
                        "attached_to_doctype": "Certificate",
                        "attached_to_name": self.name,
                    })
                    old.delete()
                except Exception:
                    pass

            saved = save_file(
                fname=f"qr_{self.name}.png",
                content=img_bytes.read(),
                dt="Certificate",
                dn=self.name,
                is_private=0,
            )

            self.db_set("qr_code", saved.file_url)
            self.qr_code = saved.file_url
            frappe.msgprint("QR Code generated.", alert=True)

        except Exception:
            frappe.log_error(frappe.get_traceback(), "Certificate QR Generation Failed")
            frappe.msgprint("QR Code generation failed. See error log.", alert=True)


@frappe.whitelist(allow_guest=True)
def get_certificate_details(cert_id):
    """Public API called by the verification page."""
    if not cert_id:
        frappe.throw("Certificate ID is required.")

    try:
        cert = frappe.get_doc("Certificate", cert_id)
    except frappe.DoesNotExistError:
        frappe.throw("Certificate not found.", frappe.DoesNotExistError)

    if cert.docstatus != 1:
        frappe.throw("Certificate is not active.")

    return {
        "name": cert.name,
        "certificate_title": cert.certificate_title,
        "certificate_type": cert.certificate_type,
        "recipient_name": cert.recipient_name or cert.recipient,
        "recipient_type": cert.recipient_type,
        "issuing_authority": cert.issuing_authority,
        "issue_date": frappe.utils.formatdate(cert.issue_date, "dd MMMM yyyy"),
        "expiry_date": frappe.utils.formatdate(cert.expiry_date, "dd MMMM yyyy") if cert.expiry_date else None,
        "valid_until": frappe.utils.formatdate(cert.valid_until, "dd MMMM yyyy") if cert.valid_until else None,
        "from_date": frappe.utils.formatdate(cert.from_date, "dd MMMM yyyy") if cert.from_date else None,
        "to_date": frappe.utils.formatdate(cert.to_date, "dd MMMM yyyy") if cert.to_date else None,
        "hours": cert.hours,
        "status": cert.status,
        "description": cert.description,
        "qr_code": cert.qr_code,
    }


@frappe.whitelist()
def regenerate_qr(docname):
    """Manually regenerate QR code for a submitted certificate."""
    doc = frappe.get_doc("Certificate", docname)
    if doc.docstatus != 1:
        frappe.throw("Only submitted certificates can have QR codes.")
    doc.generate_qr_code()
    return {"qr_code": doc.qr_code}


# Hook functions referenced in hooks.py
def on_submit(doc, method):
    doc.on_submit()

def on_cancel(doc, method):
    doc.on_cancel()
