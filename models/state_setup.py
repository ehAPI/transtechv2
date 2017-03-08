from openerp.osv import fields, osv

class state_setup(osv.osv):

	_inherit="res.country.state"
	_columns = {
	'country_id': fields.many2one('res.country', 'Country',
            required=True,domain="[('code','=','AE')]"),
	}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
	'country_id':_default_country,
	}

state_setup()
