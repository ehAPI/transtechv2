from openerp.osv import fields, osv
from datetime import date
from openerp.tools.translate import _
# from osv import osv, fields

class hr_holidays(osv.osv):
	_name = 'hr.holidays.public'
	_rec_name = 'year'
	_description = 'Public Holidays'
	_columns = {
	'year' : fields.char('Calendar Year', required=True),
	'line_ids' : fields.one2many('hr.holidays.public.line','holidays_id','Holiday Dates'),
	}
	_sql_constraints = [
		('year_unique', 'UNIQUE(year)', _('Duplicate year!')),
	]
	_order = "year"

	def is_public_holiday(self, cr, uid, dt, context=None):
		ph_obj = self.pool.get('hr.holidays.public')
		ph_ids = ph_obj.search(cr, uid, [
			('year', '=', dt.year),
		],
			context=context)
		if len(ph_ids) == 0:
			return False

		for line in ph_obj.browse(cr, uid, ph_ids[0], context=context).line_ids:
			if date.strftime(dt, "%Y-%m-%d") == line.date:
				return True

		return False

	def get_holidays_list(self, cr, uid, year, context=None):

		res = []
		ph_ids = self.search(cr, uid, [('year', '=', year)], context=context)
		if len(ph_ids) == 0:
			return res
		[res.append(l.date)
		 for l in self.browse(cr, uid, ph_ids[0], context=context).line_ids]
		return res


hr_holidays()

class hr_holidays_line(osv.osv):
	_name = 'hr.holidays.public.line'
	_description = 'Public Holidays Lines'
	_columns = {
	'date' : fields.date('Date', required= True),
	'name' : fields.char('Name', required= True),
    'holidays_id': fields.many2one('hr.holidays.public', 'Holiday Calendar Year'),
	'variable' : fields.boolean('Date May Change'),
	}

	_order = "date, name desc"