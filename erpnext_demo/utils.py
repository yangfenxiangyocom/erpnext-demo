#coding=utf-8
# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
import erpnext_demo.make_demo

def on_login(login_manager):
	from frappe.utils import validate_email_add
	if "demo_notify_url" in frappe.conf:
		if frappe.form_dict.lead_email and validate_email_add(frappe.form_dict.lead_email):
			import requests
			url = frappe.conf.demo_notify_url
			cmd = frappe.conf.demo_notify_cmd or "erpnext.templates.utils.send_message"
			r = requests.post(url, data={
				"cmd": cmd,
				"subject":"登陆进示例网站",
				"sender": frappe.form_dict.lead_email,
				"message": "经由demo@erpboost.com"
			})

def get_startup_js():
	return """frappe.ui.toolbar.show_banner('您在使用ERP Boost的示例程序. '
		+'有任何疑问?, <a style="color:red" href="http://qiao.baidu.com/v3/?module=default&amp;controller=im&amp;action=index&amp;ucid=7872376&amp;type=n&amp;siteid=5697239" '
		+'target="_blank">在线咨询</a>');"""

def check_if_not_setup():
	if frappe.db.sql("""select name from tabCompany"""):
		raise Exception("Demo App must only be installed on a blank database!")

def make_demo():
	frappe.flags.mute_emails = 1
	make_demo_user()
	make_demo_login_page()
	erpnext_demo.make_demo.make()

def make_demo_user():
	from frappe.auth import _update_password

	roles = ["Accounts Manager", "Analytics", "Expense Approver", "Accounts User",
		"Leave Approver", "Blogger", "Customer", "Sales Manager", "Employee", "Support Manager",
		"HR Manager", "HR User", "Maintenance Manager", "Maintenance User", "Material Manager",
		"Material Master Manager", "Material User", "Manufacturing Manager",
		"Manufacturing User", "Projects User", "Purchase Manager", "Purchase Master Manager",
		"Purchase User", "Quality Manager", "Report Manager", "Sales Master Manager",
		"Sales User", "Supplier", "Support Team"]

	def add_roles(doc):
		for role in roles:
			doc.append("user_roles", {
				"doctype": "UserRole",
				"role": role
			})

	# make demo user
	if frappe.db.exists("User", "demo@erpboost.com"):
		frappe.delete_doc("User", "demo@erpboost.com")

	# add User Type property setter
	user_types = frappe.get_meta("User").get_field("user_type").options
	frappe.make_property_setter({
		"doctype_or_field": "DocField",
		"doctype": "User",
		"fieldname": "user_type",
		"property": "options",
		"value": (user_types or "") + "\nERP Boost Demo",
		"property_type": "Text"
	})

	p = frappe.new_doc("User")
	p.email = "demo@erpboost.com"
	p.first_name = "Demo"
	p.last_name = "User"
	p.enabled = 1
	p.user_type = "ERP Boost Demo"
	p.insert()
	add_roles(p)
	p.save()
	_update_password("demo@erpboost.com", "demo")

	# only read for newsletter
	frappe.db.sql("""update `tabDocPerm` set `write`=0, `create`=0, `cancel`=0
		where parent='Newsletter'""")
	frappe.db.sql("""update `tabDocPerm` set `write`=0, `create`=0, `cancel`=0
		where parent='User' and role='All'""")

	frappe.db.commit()

def make_demo_login_page():
	import frappe.installer

	frappe.installer.add_to_installed_apps("erpnext_demo")

	website_settings = frappe.get_doc("Website Settings", "Website Settings")
	website_settings.home_page = "start"
	website_settings.disable_signup = 1
	website_settings.save()
	frappe.db.commit()

def validate_reset_password(doc, method):
	if doc.name == "demo@erpboost.com":
		throw(_("不能为其重设密码: {0}").format(doc.first_name + " " + doc.last_name))
