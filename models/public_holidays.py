from openerp.osv import fields, osv
from datetime import date
from openerp.tools.translate import _
# from osv import osv, fields

class public_holidays(osv.osv):
	_name = 'public.holidays'
	_rec_name = 'cal_year'
	_description = 'Public Holidays'
	_columns = {
	'cal_year' : fields.char('Calendar Year', required=True),
	'public_holiday' : fields.one2many('public.holiday.days','dn','Public Holidays'),
	}
	_sql_constraints = [
		('year_unique', 'UNIQUE(cal_year)', _('Duplicate cal_year!')),
	]
	_order = "cal_year desc"

	def is_public_holiday(self, cr, uid, dt, context=None):
		ph_obj = self.pool.get('public.holidays')
		ph_ids = ph_obj.search(cr, uid, [
			('cal_year', '=', dt.year),
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
		ph_ids = self.search(cr, uid, [('cal_year', '=', year)], context=context)
		if len(ph_ids) == 0:
			return res
		[res.append(l.date)
		 for l in self.browse(cr, uid, ph_ids[0], context=context).line_ids]
		return res


public_holidays()

class public_holiday_days(osv.osv):
	_name = 'public.holiday.days'
	_description = 'Public Holidays Lines'
	_columns = {
	'dn' : fields.integer('Day', required= True),
	'date' : fields.date('Date', required= True),
	'name' : fields.char('Name', required= True),
	'date_may_change' : fields.boolean('Date May Change'),
	}

	_order = "date, name desc"