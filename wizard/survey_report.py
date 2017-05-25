from openerp.osv import fields, osv
from openerp.tools.translate import _
import time



class survey_report(osv.osv):

    _name = "survey.report"

    _columns = {
    "from_date": fields.date("From Date"),
    "to_date": fields.date("To Date"),
    "Bank/Customer": fields.many2one("customer.info","Bank/Customer"),
    }
    
    def action_survey_details(self,cr,uid,ids,context=None):

        data = self.read(cr, uid, ids)[0]
        survey_ids = self.pool.get("survey.info").search(cr,uid,[("visit_tm",">=",data["from_date"]),("visit_tm","<=",data["to_date"])])       
        print survey_ids
        models_data = self.pool.get("ir.model.data")
        survey_report_tree = models_data._get_id(cr, uid, "atm", "view_survey_details_info_tree")
        return{"name":"Survey Info","view_type":"form","view_mode":"tree,form","res_model":"survey.info","type": "ir.actions.act_window",
		"search_view_id": survey_report_tree,'domain':"[('id', 'in',%s)]" %(survey_ids),

		}

		# return {
	 #    "name": "Survey Info",
		# "view_type": "form",
		# "view_mode": "tree,form",
		# "res_model": "survey.details",
		# "type": "ir.actions.act_window",
		# "search_view_id": survey_report_tree,
		# "domain":"[("id", "in",%s)]" %(survey_ids),
		# }
        
	 
 
survey_report()  
