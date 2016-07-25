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
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)
import base64
import sys, os


class doctor_hc_odontologia(osv.osv):
	"""doctor_hc_odontologia"""
	_name = 'doctor.hc.odontologia'
	_description = 'doctor hc de odontologia'

	def create(self, cr, uid, vals, context=None):
		# Set number if empty
		if not vals.get('number'):
			vals['number'] = self.pool.get('ir.sequence').get(cr, uid, 'attention.sequence')
		return super(doctor_hc_odontologia, self).create(cr, uid, vals, context=context)

	# def default_get(self, cr, uid, fields, context=None):
	# 	res = super(doctor_hc_odontologia,self).default_get(cr, uid, fields, context=context)
		

	# 	if context.get('active_model') == "doctor.patient":
	# 		id_paciente = context.get('default_patient_id')
	# 	else:
	# 		id_paciente = context.get('patient_id')

	# 	if id_paciente:    
	# 		fecha_nacimiento = self.pool.get('doctor.patient').browse(cr,uid,id_paciente,context=context).birth_date
	# 		res['age_attention'] = self.calcular_edad(fecha_nacimiento)
	# 		res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)

	# 	return res

	def finalizar_atencion(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'cerrada'}, context=context)

	def calcular_edad(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_attention = age,
			age_unit = '3'

		elif age > 30 and age < 365:
			age = age / 30
			age = int(age)
			age_attention = age,
			age_unit = '2'

		elif age >= 365:
			age = int((current_date.year-st_birth_date.year-1) + (1 if (current_date.month, current_date.day) >= (st_birth_date.month, st_birth_date.day) else 0))
			age_attention = age,
			age_unit = '1'
		
		return age

	def calcular_age_unit(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_unit = '3'
		elif age > 30 and age < 365:
			age_unit = '2'

		elif age >= 365:
			age_unit = '1'

		return age_unit

	def _fun_calcular_edad(self, cr, uid, ids, field_name, args, context=None):
		res = {}
		for datos in self.browse(cr,uid,ids):
			_logger.info(context)

	def _get_default_signature(self, cr, uid, context=None):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, 'Odontograma.png')
		f = open(filename, 'rb')
		image = base64.encodestring(f.read())
		f.close()
		return image

	def _get_default_estomatologicos(self, cr, uid, context=None):
		lista = ['LABIOS', 'LENGUA', 'PALADAR', 'GLAN. SALIVALES', 'FRENILLOS', 'MUCOSA ORAL', 'PISO DE BOCA', 'OROFARINGE', 'MUSCULOS', 'ATM']
		result= []
		counter = 0
		for lines in lista:
			line_data = {
					'estructura' : lista[counter],
					'normal' : True
			}
			counter+=1
			result.append((0,0,line_data))
		return result

	def on_change_indeterminable(self, cr, uid, ids, clasificacion_angle, context=None):
		if context is None: context = {}
	
		res = {}
		if clasificacion_angle:
			res['clasificacion_angle'] = False
		return {'value': res}

	def on_change_clasificacionangle(self, cr, uid, ids, indeterminable, context=None):
		if context is None: context = {}
	
		res = {}
		if indeterminable:
			res['indeterminable'] = False
		return {'value': res}

	def _previous(self, cr, uid, patient_id, type_past, attentiont_id=None):
		condition = [('patient_id', '=', patient_id.id)]
		if attentiont_id != None:
			condition.append(('attentiont_id', '<=', attentiont_id))
		if type_past == 'past':
			return self.pool.get('doctor.hc.odontologia.antecedentes.pasado').search(cr, uid, condition, order='id desc')

	def _get_past(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for datos in self.browse(cr, uid, ids):
			res[datos.id] = self._previous(cr, uid, datos.patient_id, 'past', datos.id)
		return res

	def onchange_patient(self, cr, uid, ids, patient_id, context=None):
		values = {}
		if not patient_id:
			return values
		past = self.pool.get('doctor.hc.odontologia.antecedentes.pasado').search(cr, uid, [('patient_id', '=', patient_id)],
															  order='id asc')
		
		patient_data = self.pool.get('doctor.patient').browse(cr, uid, patient_id, context=context)
		photo_patient = patient_data.photo

		values.update({
			'patient_photo': photo_patient,
			'antecedente_ids': past,
		})
		return {'value': values}

	def onchange_professional(self, cr, uid, ids, professional_id, context=None):
		values = {}
		if not professional_id:
			return values
		professional_data = self.pool.get('doctor.professional').browse(cr, uid, professional_id, context=context)
		professional_img = professional_data.photo
		if professional_data.speciality_id.id:
			professional_speciality = professional_data.speciality_id.id
			values.update({
				'speciality': professional_speciality,
			})

		values.update({
			'professional_photo': professional_img,
		})
		_logger.info(values)
		return {'value': values}

	_columns = {
		#Examen fisico
		'peso': fields.float('Peso (kg)'),
		'frecuencia_cardiaca' : fields.integer('Frecuencia cardiaca'),
		'frecuencia_respiratoria' : fields.integer('Frecuencia respiratoria'),
		'sistolica' : fields.integer(u'Sistólica'),
		'diastolica' : fields.integer(u'Diastólica'),
		#Examen Estomatologico
		'examen_estomatologico_ids': fields.one2many('doctor.hc.odontologia.estomatologico', 'hc_odontologia_id','Examen estomatologico'),
		'clasificacion_angle' : fields.selection([('1', 'I'), ('2', 'II/1'), ('3', 'II/2'), ('4', 'III')], 'Clasificacion de Angle'),
		'indeterminable' : fields.boolean('Indeterminable'),
		'habitos_orales' : fields.text('Habitos orales'),
		'img_odontograma': fields.binary('Odontograma', readonly=True),
		#Datos basicos
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict'),
		'patient_photo': fields.related('patient_id', 'photo', type="binary", relation="doctor.patient"),
		'date_attention': fields.datetime(u'Fecha Atención', required=False),
		'number': fields.char(u'Atención N°', select=1, size=32,
							  help="Number of attention. Keep empty to get the number assigned by a sequence."),
		'origin': fields.char('Source Document', size=64,
							  help="Reference of the document that produced this attentiont.", readonly=True),
		'age_attention': fields.integer('Current age', readonly=True),
		'age_unit': fields.selection([('1', 'Years'), ('2', 'Months'), ('3', 'Days'), ], 'Unit of measure of age',
									 readonly=True),
		'professional_id': fields.many2one('doctor.professional', 'Médico', required=False),
		'speciality': fields.related('professional_id', 'speciality_id', type="many2one", relation="doctor.speciality",
									 string='Especialidad', required=False, store=True),
		'professional_photo': fields.related('professional_id', 'photo', type="binary", relation="doctor.professional",
											 readonly=True, store=False),
		#conclusiones
		'analisis_atencion' : fields.text('Analisis', required=False),

		# #odontograma
		'diagnosticos_ids' : fields.one2many('doctor.hc.odontologia.odontograma', u'hc_odontologia_id', 'Odontograma Fields'),

		'recomendaciones_ids': fields.one2many('doctor.attentions.recomendaciones', 'attentiont_id', 'Agregar Recomendaciones'),
		'prescripciones_ids' : fields.one2many('doctor.prescription', 'attentiont_id', u'Prescripción Medicamentos', ondelete='restrict'),
		'agregar_antecedente_ids': fields.one2many('doctor.hc.odontologia.antecedentes.pasado', 'attentiont_id', 'Agregar antecedente', ondelete='restrict'),
		'antecedente_ids': fields.function(_get_past, relation="doctor.hc.odontologia.antecedentes.pasado", type="one2many", store=False,readonly=True, method=True, string="Antecedente"),

		'state': fields.selection([('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 'Estado', readonly=True, required=True),
	}

	def _get_professional_id(self, cr, uid, user_id):
		try:
			professional_id= self.pool.get('doctor.professional').browse(cr, uid, self.pool.get('doctor.professional').search(cr, uid, [( 'user_id',  '=', uid)]))[0].id
			return professional_id
		except Exception as e:
			raise osv.except_osv(_('Error!'),
								 _('El usuario del sistema no es profesional de la salud.'))

	_constraints = [
		
	]

	# _defaults = {
	# 	'patient_id': lambda self, cr, uid, context: context.get('patient_id', False),
	# 	'professional_id': _get_professional_id,
	# 	'img_odontograma': _get_default_signature,
	# 	'examen_estomatologico_ids': _get_default_estomatologicos,
	# 	'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
	# 	'habitos_orales' : 'No registra ...',
	# 	'analisis_atencion' :  'No registra ...',
	# 	'state': 'abierta',
	# }


doctor_hc_odontologia()

class doctor_hc_odontologia_estomatologico(osv.osv):
	"""examen estomatologico  de hc odontologia"""
	_name = 'doctor.hc.odontologia.estomatologico'
	_description = "Examen estomatologico"

	_columns = {
		'hc_odontologia_id' : fields.many2one('doctor.hc.odontologia','Historia Clinica Odontologia'),
		'estructura': fields.char('Estructura'),
		'normal'  : fields.boolean('Normal'),
		'anormal' : fields.boolean('Anormal'),
	}

	#Valida que no haya una evaluacion normal y anormal al mismo tiempo.
	def _validar_estadoestructura(self, cr, uid, ids, context=None):
		for record in self.browse(cr, uid, ids):
			if record.normal and record.anormal:
				return False
			return True

	_constraints = [
		(_validar_estadoestructura, u'\n\nDESCRIPCIÓN DETALLADA\nHay una estructura con estado normal y anormal al mismo tiempo', [u'examen estomatológico'])	
	]


	_defaults = {
		'normal': True,
	}

doctor_hc_odontologia_estomatologico()

class odontograma(osv.osv):
	"""examen de dientes con base en odontograma"""
	_name = 'doctor.hc.odontologia.odontograma'
	_description = 'Examen de dientes con base en odontograma'

	_columns = {
		'hc_odontologia_id' : fields.many2one('doctor.hc.odontologia','Historia Clinica Odontologia'),
		'diagnostico_odontologico_id' : fields.many2one('doctor.diseases', u'Diagnósticos', required=False),
		'dientes_id' : fields.many2one('doctor.hc.odontologia.diente','Diente', required=True),
		'procedimiento_id' : fields.many2one('product.product', 'Procedimiento', required=False),
		'superficie_diente' : fields.selection([('lingual', 'Lingual'), ('vestibular', 'Vestibular'), ('mesial', 'Mesial'), ('distal', 'Distal'), ('oclusal', 'Oclusal')], 'Superficie dental'),
	}

odontograma()

class doctor_hc_odontologia_past(osv.osv):
	"""examen estomatologico  de hc odontologia"""
	_name = 'doctor.hc.odontologia.antecedentes.pasado'
	_description = "Antecedentes pasados de odontologia"

	_columns = {
		'attentiont_id': fields.many2one('doctor.hc.odontologia', u'Atención Odontológica', ondelete='restrict'),
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict'),
		'categoria_antecedente': fields.many2one('doctor.past.category', u'Categoría', required=True, ondelete='restrict'),
		'antecedente': fields.text('Antecedente', required=True),
	}

	_defaults = {
		'patient_id': lambda self, cr, uid, context: context.get('patient_id', False),
	}

doctor_hc_odontologia_past()

