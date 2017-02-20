from openerp.osv import fields, osv
class remark_category(osv.osv):
	_name = 'remark.category'
	_rec_name = 'remark_description'
	_description = 'Manage Remark Category'
	_columns = {
	'remark_category_id' : fields.char('Remark Category ID', readonly=True, size=200),
	'remark_description' : fields.char('Remark Description', required=True),
	}

remark_category()