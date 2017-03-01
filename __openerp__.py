{
	"name" : "ATM Survey Management",
	"version": "1.0",
	"author":"ehAPI Technologies LLC",
	"website":"http://www.techanipr.com",
	"category":"Tools",
	"depends":["base",'board','mail'],
	"description":"Transtech ATM Survey Management",

	"data": ["wizard/atm_move_view.xml",
			 "wizard/survey_report_view_wizard.xml",
			 "wizard/survey_report_view.xml",
	         "wizard/upload_images_view.xml",
			 "views/schedule_tasks_view.xml",
			 "views/tasks_status_view.xml",
			 "views/jsmap.xml",
			 # "static/src/xml/base.xml",
			 "views/alerts_foru_view.xml",
			 "views/tasks_inqueue_view.xml",
			 "security/transtech_atm_updater_security_view.xml",
			 "views/site_inspection_view.xml",
			 "views/survey_details_view.xml",
			 "views/view_plan_tasks_view.xml",
			 "views/users_view.xml",
			 "views/customer_details_view.xml",
			 "views/atm_details_view.xml",
			 "views/cust_alerts_view.xml",
			 "views/internal_alerts_view.xml",
			 "views/public_holidays_view.xml",
			 "views/reason_code_setup_view.xml",
			 "views/state_setup_view.xml",
			 "security/ir.model.access.csv",
			 "views/remark_category_view.xml"],

    'qweb': ['static/src/xml/base.xml',],

	
          
     
	"installable": True

}