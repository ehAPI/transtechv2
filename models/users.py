from openerp.osv import fields, osv

class manage_group(osv.osv):

	_inherit="res.groups"
	
manage_group()


class manage_users(osv.osv):
	_inherit="res.users"
	_columns = {
	'company':fields.many2one('multi_company.default','Company',required=True),
	'customer':fields.boolean('Customer'),
	'is_team_leader':fields.boolean('Is Team Leader??'),
	# 'tuser_id':fields.char('User ID',readonly=True, size=64),
	'contact_num':fields.char('Contact Number',size=32),
	'joining_date':fields.date('Joining Date'),
	'Comments':fields.text('Comments'),
	'team_leader':fields.char('Team Leader',size=32),
	'role':fields.char('Role',size=32),
	'survey_limit':fields.integer('Limit of Surveys'),
	'customer_ids':fields.many2one('customer.info','Allowed Customers'),

	'status': fields.selection([('never_connected','Never Connected'),('activated','Activated')],'Status'),

	}
_defaults={
	'status':'never_connected'
}


	
manage_users()