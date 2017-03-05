from openerp.osv import fields, osv

class reason_code_setup(osv.osv):
	_name = 'reason.code.setup'
	_rec_name =  'reason_code'
	_description = 'Reason Code'
	_columns = {
	'code' : fields.char('Code', readonly=True, size=60),
	'reason_code' : fields.char('Reason Code', size=240),
	}

	def create(self, cr, uid, vals, context=None):
		if vals.get('code','/')== '/':
			vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'reason.code.setup') or '/'
		code = super(reason_code_setup, self).create(cr, uid, vals, context=context)
		return code

reason_code_setup()
