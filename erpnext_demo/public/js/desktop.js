$(document).on("desktop-render", function() {
	if (user !== "Administrator") {
		frappe.desktop.show_all_modules = function() {
			msgprint(__("此功能已针对示例客户禁用."));
		}
	}
});
