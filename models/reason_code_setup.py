from openerp.osv import fields, osv
class reason_code_setup(osv.osv):
	_name = 'reason.code.setup'
	_rec_name =  'reason_code'
	_description = 'Reason Code'
	_columns = {
	'code' : fields.char('Code', readonly=True, size=60),
	'reason_code' : fields.char('Reason Code', size=240),
	}

	# def create(self, cr, uid, values, context=None):
	# 	code = values.get('code',0)
	# 	code = code + 1
	# 	values.update({'code' : code})

reason_code_setup()
