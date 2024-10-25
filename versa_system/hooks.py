app_name = "versa_system"
app_title = "Versa System"
app_publisher = "efeone"
app_description = "Frappe app to manage operations in manufacturing industry"
app_email = "info@efeone.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/versa_system/css/versa_system.css"
# app_include_js = "/assets/versa_system/js/versa_system.js"

# include js, css files in header of web template
# web_include_css = "/assets/versa_system/css/versa_system.css"
# web_include_js = "/assets/versa_system/js/versa_system.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "versa_system/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Lead" : "public/js/lead.js","Quotation" : "public/js/quotation.js","Sales Order": "public/js/sales_order.js"}


# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "versa_system/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "versa_system.utils.jinja_methods",
# 	"filters": "versa_system.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "versa_system.install.before_install"
after_install = "versa_system.setup.after_install"

after_migrate = "versa_system.setup.after_migrate"

# Uninstallation
# ------------

before_uninstall = "versa_system.setup.before_uninstall"
# after_uninstall = "versa_system.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "versa_system.utils.before_app_install"
# after_app_install = "versa_system.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "versa_system.utils.before_app_uninstall"
# after_app_uninstall = "versa_system.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "versa_system.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
# hooks.py
doc_events = {
   "Sales Order": {
       "on_submit": "versa_system.versa_system.custom_scripts.work_order.create_work_order_from_sales_order"
   }
}




>>>>>>> 33f425b (feat : Changing status automatically)
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"versa_system.tasks.all"
# 	],
# 	"daily": [
# 		"versa_system.tasks.daily"
# 	],
# 	"hourly": [
# 		"versa_system.tasks.hourly"
# 	],
# 	"weekly": [
# 		"versa_system.tasks.weekly"
# 	],
# 	"monthly": [
# 		"versa_system.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "versa_system.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "versa_system.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "versa_system.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["versa_system.utils.before_request"]
# after_request = ["versa_system.utils.after_request"]

# Job Events
# ----------
# before_job = ["versa_system.utils.before_job"]
# after_job = ["versa_system.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"versa_system.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {
        "dt": "Workflow",
        "filters": [
            ["name", "in", ["Feasibility Check", "Mockup Design","Quotation","Final Design Approval"]]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            ["name", "in", ["Pending", "Approved", "Rejected","Sent to Customer","Review Request"]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["name", "in", ["Approve", "Reject", "Rivision Requested","Sent to Customer","Review"]]
        ]
    }
]
doc_events = {
    "Lead": {
        "before_save": "versa_system.versa_system.custom_scripts.lead.update_lead_status_on_save"
    }
   
}
