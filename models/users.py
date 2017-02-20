from openerp.osv import fields, osv

class manage_group(osv.osv):

	_inherit="res.groups"
<<<<<<< HEAD
	_columns={ 
	'share_group': fields.boolean('Share Group'),
	'portal' : fields.boolean('Portal'),
=======
	_columns={ 'share_group': fields.boolean('Share Group'),
				'portal' : fields.boolean('Portal'),
>>>>>>> 5102f8d9270ca85cbcf3e3aab4312ca87f6738ba
	}
	
manage_group()


class manage_users(osv.osv):
	
	_inherit="res.users"

	_columns = {
	'company':fields.many2one('multi_company.default','Company',required=True),
	'customer':fields.boolean('Customer'),
	'is_team_leader':fields.boolean('Is Team Leader??'),
	# 'tuser_id':fields.char('User ID',readonly=True, size=64),
<<<<<<< HEAD
	'contact_num':fields.char('Contact Number',size=32),
	'joining_date':fields.date('Joining Date'),
	'comments':fields.text('Comments'),
	'team_leader':fields.char('Team Leader',size=32),
=======
	'contact_num':fields.integer('Contact Number'),
	'joining_date':fields.date('Joining Date'),
	'comments':fields.text('Comments'),
	'team_leader':fields.char('Team Leader'),
>>>>>>> 5102f8d9270ca85cbcf3e3aab4312ca87f6738ba
	'role':fields.char('Role',size=32),
	'survey_limit':fields.integer('Limit of Surveys'),
	'customer_ids':fields.many2one('customer.info','Allowed Customers'),
	'password1' : fields.char('Password', invisible=True,required=True,size=64),
<<<<<<< HEAD
=======
	'sharing' : fields.selection([('false','False'),('user_id','User')],'Sharing'),
>>>>>>> 5102f8d9270ca85cbcf3e3aab4312ca87f6738ba
	}

manage_users()