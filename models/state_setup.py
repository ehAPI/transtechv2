from openerp.osv import fields, osv

class state_setup(osv.osv):

	_inherit="res.country.state"
	_columns = {
	'country_id': fields.many2one('res.country', 'Country',
            required=True,domain="[('code','=','AE')]"),
	}