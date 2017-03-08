from openerp.osv import fields, osv

class remark_category(osv.osv):

	_name = 'remark.category'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'description': self.pool.get('ir.sequence').get(cr, uid, 'remarks.category'),
        })
		return super(remarks_category, self).copy(cr, uid, id, default, context=context)

	_rec_name = 'remark_description'
	_description = 'Manage Remark Category'
	_columns = {
	'remark_category_id' : fields.char('Remark Category ID', readonly=True, size=200),
	'remark_description' : fields.char('Remark Description', required=True),
	}

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'remark_description': self.pool.get('ir.sequence').get(cr, uid, 'remark.category'),
        })
		return super(remarks_category, self).copy(cr, uid, id, default, context=context)

	def create(self, cr, uid, vals, context=None):
		if vals.get('remark_category_id','/')== '/':
			vals['remark_category_id'] = self.pool.get('ir.sequence').get(cr, uid, 'remark.category') or '/'
		return super(remark_category, self).create(cr, uid, vals, context=context)

remark_category()