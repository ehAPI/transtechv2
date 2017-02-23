from openerp.osv import fields, osv
class remark_category(osv.osv):
	_name = 'remark.category'
	_rec_name = 'remark_description'
	_description = 'Manage Remark Category'
	_columns = {
	'remark_category_id' : fields.char('Remark Category ID', readonly=True, size=200),
	'remark_description' : fields.char('Remark Description', required=True),
	}

	def create(self, cr, uid, vals, context=None):
		if vals.get('description','/')== '/':
			vals['description'] = self.pool.get('ir.sequence').get(cr, uid, 'remark.category') or '/'
		return super(remark_category, self).create(cr, uid, vals, context=context)


remark_category()