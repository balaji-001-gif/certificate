frappe.ui.form.on("Certificate", {
    refresh(frm) {
        const status_colors = { Draft: "gray", Active: "green", Expired: "orange", Revoked: "red" };
        if (frm.doc.status) {
            frm.page.set_indicator(frm.doc.status, status_colors[frm.doc.status] || "gray");
        }
        if (frm.doc.docstatus === 1) {
            const verify_url = `${window.location.origin}/verify-certificate?id=${frm.doc.name}`;
            frm.add_custom_button(__("Open Verification Page"), () => {
                window.open(verify_url, "_blank");
            }, __("Actions"));
            frm.add_custom_button(__("Copy Verification URL"), () => {
                frappe.utils.copy_to_clipboard(verify_url);
                frappe.show_alert({ message: __("Verification URL copied!"), indicator: "green" });
            }, __("Actions"));
            frm.add_custom_button(__("Regenerate QR Code"), () => {
                frappe.confirm(__("Regenerate the QR code for this certificate?"), () => {
                    frappe.call({
                        method: "certificate.doctype.certificate.certificate.regenerate_qr",
                        args: { docname: frm.doc.name },
                        callback(r) {
                            if (!r.exc) {
                                frappe.show_alert({ message: __("QR Code regenerated!"), indicator: "green" });
                                frm.reload_doc();
                            }
                        }
                    });
                });
            }, __("Actions"));
        }
    },

    recipient_type(frm) {
        frm.set_value("recipient", "");
        frm.set_value("recipient_name", "");
    },

    recipient(frm) {
        if (!frm.doc.recipient || !frm.doc.recipient_type) return;

        const name_fields = {
            Employee: "employee_name",
            Customer: "customer_name",
            Supplier: "supplier_name",
            Student:  "first_name",
            Member:   "member_name",
            Other:    "name"
        };

        const field = name_fields[frm.doc.recipient_type] || "name";

        frappe.db.get_value(frm.doc.recipient_type, frm.doc.recipient, field)
            .then(r => {
                if (r.message && r.message[field]) {
                    frm.set_value("recipient_name", r.message[field]);
                }
            });
    }
});
