# -*- encoding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp import pooler
from datetime import date, datetime, timedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class doctor_prescription_co(osv.osv):
		_name = "doctor.simplified.prescription"
		_rec_name = 'drugs_id'
		
		_columns = {
				'attentiont_id': fields.many2one('doctor.hc.odontologia', u'Atención', required=True),
				'drugs_id': fields.many2one('doctor.drugs', 'Medicamento', ondelete='restrict'),
				'total_quantity': fields.integer('Cantidad Total',),
				'action_id': fields.selection([
																					('take', 'Tomar'),
																					('inject', 'Inyectar'),
																					('apply', 'Aplicar'),
																					('inhale', 'Inhalar'),
																			], u'Acción'),

				'frequency': fields.integer('Frecuencia (cada)'),
				'frequency_unit_n': fields.selection([
																								 ('minutes', 'Minutos'),
																								 ('hours', 'Horas'),
																								 ('days', 'Dias'),
																								 ('weeks', 'Semanas'),
																								 ('wr', 'Cuando se Requiera'),
																								 ('total', 'Total'),
																						 ], 'Frecuencia'),
				'duration': fields.integer('Duración Tratamiento'),
				'duration_period_n': fields.selection([
																									('minutes', 'Minutos'),
																									('hours', 'Horas'),
																									('days', 'Dias'),
																									('months', 'Meses'),
																									('indefinite', 'Indefinido'),
																							], 'Periodo',),
				'administration_route_id': fields.many2one('doctor.administration.route', u'Ruta Administración',
																									 ondelete='restrict'),
				'indications': fields.text('Indicaciones'),
				'plantilla_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas'),
		}

		_defaults = {
				'action_id': 'Tomar',
				'frequency_unit_n': 'Horas',
				'duration_period_n': 'Dias',
		}

		def name_get(self, cr, uid, ids, context={}):
				if not len(ids):
						return []
				rec_name = 'drugs_id'
				res = [(r['id'], r[rec_name][1])
							 for r in self.read(cr, uid, ids, [rec_name], context)]
				return res

		def onchange_plantillas(self, cr, uid, ids, plantilla_id, context=None):
			res={'value':{}}
			if plantilla_id:
				cuerpo = self.pool.get('doctor.attentions.recomendaciones').browse(cr,uid,plantilla_id,context=context).cuerpo
				res['value']['indications']=cuerpo
			else:
				res['value']['indications']=''
			return res


doctor_prescription_co()