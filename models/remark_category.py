from openerp.osv import fields, osv

class remarks_category(osv.osv):

	_name = 'remarks.category'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'description': self.pool.get('ir.sequence').get(cr, uid, 'remarks.category'),
        })
		return super(remarks_category, self).copy(cr, uid, id, default, context=context)

	_rec_name = 'description'
	_description = 'Manage Remark Category'
	_columns = {
	'description' : fields.char('Remark Category ID', readonly=True, size=200),
	'name' : fields.char('Remark Description', required=True),
	}

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'remarks_description': self.pool.get('ir.sequence').get(cr, uid, 'remarks.category'),
        })
		return super(remarks_category, self).copy(cr, uid, id, default, context=context)

	def create(self, cr, uid, vals, context=None):
		if vals.get('description','/')== '/':
			vals['description'] = self.pool.get('ir.sequence').get(cr, uid, 'remarks.category') or '/'
		return super(remarks_category, self).create(cr, uid, vals, context=context)

remarks_category()