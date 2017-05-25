from openerp.osv import fields, osv

class reason_code_setup(osv.osv):
	_name = 'reason.code'
	_rec_name =  'reason_code'
	_description = 'Reason Code'
	_columns = {
	'reason_code' : fields.char('Code', readonly=True, size=60),
	'name' : fields.char('Reason Code', size=240),
	}

	def create(self, cr, uid, vals, context=None):
		if vals.get('reason_code','/')== '/':
			vals['reason_code'] = self.pool.get('ir.sequence').get(cr, uid, 'reason.code') or '/'
		reason_code = super(reason_code_setup, self).create(cr, uid, vals, context=context)
		return reason_code

reason_code_setup()
