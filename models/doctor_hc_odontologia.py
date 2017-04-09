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


	def tipo_documento(self, tipo):

		nombre_tipo = None

		if tipo == '13':
			nombre_tipo = 'CC'
		elif tipo == '11':
			nombre_tipo = 'RC'
		elif tipo == '12':
			nombre_tipo = 'TI'
		elif tipo == '21':
			nombre_tipo = 'CE'
		elif tipo == '41':
			nombre_tipo = 'Pasaporte'
		elif tipo == 'NU':
			nombre_tipo = 'NU'
		elif tipo == 'AS':
			nombre_tipo = 'AS'
		elif tipo == 'MS':
			nombre_tipo = 'MS'

		return nombre_tipo



	def default_get(self, cr, uid, fields, context=None):
		res = super(doctor_hc_odontologia,self).default_get(cr, uid, fields, context=context)

		if context.get('active_model') == "doctor.patient":
			id_paciente = context.get('default_patient_id')
		else:
			id_paciente = context.get('patient_id')

		if id_paciente:    
			fecha_nacimiento = self.pool.get('doctor.patient').browse(cr,uid,id_paciente,context=context).birth_date
			ref = self.pool.get('doctor.patient').browse(cr,uid,id_paciente,context=context).ref
			tdoc = self.pool.get('doctor.patient').browse(cr,uid,id_paciente,context=context).tdoc
			res['age_attention'] = self.calcular_edad(fecha_nacimiento)
			res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)
			res['ref'] = ref
			_logger.info(tdoc)
			res['tdoc'] = self.tipo_documento(tdoc)

		return res

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
		lista = ['LABIOS', 'LENGUA', 'PALADAR', 'GLAN. SALIVALES', 'FRENILLOS', 'MUCOSA ORAL', 'PISO DE BOCA', 'OROFARINGE', 'MUSCULOS', 'ATM', 'ENCIA']
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

	def _get_default_dientes_permanentes(self, cr, uid, context=None):
		modelo_diente = self.pool.get('doctor.hc.odontologia.diente')
		dientes_ids = modelo_diente.search(cr, uid, [], context=context)
		result= []
		counter = 0
		for lines in dientes_ids:
			line_data = {
				'diente_perma_id' : dientes_ids[counter],
			}
			counter+=1
			result.append((0,0,line_data))
		return result

	def _get_default_dientes_temporales(self, cr, uid, context=None):
		modelo_diente_tempo = self.pool.get('doctor.hc.odontologia.diente_tempo')
		dientes_tempo_ids = modelo_diente_tempo.search(cr, uid, [], context=context)
		result= []
		counter = 0
		for lines in dientes_tempo_ids:
			line_data = {
				'diente_temp_id' : dientes_tempo_ids[counter],
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
		return {'value': values}

	_columns = {
		#Examen fisico
		'enfermedad_actual': fields.text('Enfermedad Actual', required=False, states={'cerrada': [('readonly', True)]}),
		'frecuencia_cardiaca' : fields.integer('Frecuencia cardiaca', states={'cerrada': [('readonly', True)]}),
		'frecuencia_respiratoria' : fields.integer('Frecuencia respiratoria', states={'cerrada': [('readonly', True)]}),
		'sistolica' : fields.integer(u'Sistólica', states={'cerrada': [('readonly', True)]}),
		'diastolica' : fields.integer(u'Diastólica', states={'cerrada': [('readonly', True)]}),
		#Examen Estomatologico
		'examen_estomatologico_ids': fields.one2many('doctor.hc.odontologia.estomatologico', 'hc_odontologia_id','Examen estomatologico', states={'cerrada': [('readonly', True)]} ),
		'clasificacion_angle' : fields.selection([('1', 'I'), ('2', 'II/1'), ('3', 'II/2'), ('4', 'III')], 'Clasificacion de Angle', states={'cerrada': [('readonly', True)]}),
		'indeterminable' : fields.boolean('Indeterminable', states={'cerrada': [('readonly', True)]}),
		'habitos_orales' : fields.text('Habitos orales', states={'cerrada': [('readonly', True)]}),
		'img_odontograma': fields.binary('Odontograma', states={'cerrada': [('readonly', True)]}),
		#Datos basicos
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'patient_photo': fields.related('patient_id', 'photo', type="binary", relation="doctor.patient",  readonly=True),
		'date_attention': fields.datetime(u'Fecha Atención', required=False, states={'cerrada': [('readonly', True)]}),
		'number': fields.char(u'Atención N°', select=1, size=32,
							  help="Number of attention. Keep empty to get the number assigned by a sequence."),
		'motivo_consulta' : fields.char("Motivo de Consulta", size=100, required=False, states={'cerrada': [('readonly', True)]}),
		'origin': fields.char('Source Document', size=64,
							  help="Reference of the document that produced this attentiont.", readonly=True),
		'age_attention': fields.integer('Current age', readonly=True),
		'age_unit': fields.selection([('1', 'Years'), ('2', 'Months'), ('3', 'Days'), ], 'Unit of measure of age',
									 readonly=True),
		'ref': fields.char('Identificacion', readonly=True),
		'tdoc': fields.char('tdoc', readonly=True),
		'peso': fields.float('Peso (kg)', states={'cerrada': [('readonly', True)]}),
		'professional_id': fields.many2one('doctor.professional', 'Médico', required=False, states={'cerrada': [('readonly', True)]}),
		'speciality': fields.related('professional_id', 'speciality_id', type="many2one", relation="doctor.speciality",
									 string='Especialidad', required=False, store=True, states={'cerrada': [('readonly', True)]}),
		'professional_photo': fields.related('professional_id', 'photo', type="binary", relation="doctor.professional",
											 readonly=True, store=False),
		#conclusiones
		'analisis_atencion' : fields.text('Analisis', required=False, states={'cerrada': [('readonly', True)]}),

		# #odontograma
		'diagnosticos_ids' : fields.one2many('doctor.hc.odontologia.odontograma', u'hc_odontologia_id', 'Odontograma Fields', states={'cerrada': [('readonly', True)]}),

		'recomendaciones_ids': fields.one2many('doctor.attentions.recomendaciones', 'attentiont_id', 'Agregar Recomendaciones', states={'cerrada': [('readonly', True)]}),
		'prescripciones_ids' : fields.one2many('doctor.simplified.prescription', 'attentiont_id', u'Prescripción Medicamentos', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'agregar_antecedente_ids': fields.one2many('doctor.hc.odontologia.antecedentes.pasado', 'attentiont_id', 'Agregar antecedente', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'antecedente_ids': fields.function(_get_past, relation="doctor.hc.odontologia.antecedentes.pasado", type="one2many", store=False,readonly=True, method=True, string="Antecedente"),

		'dientes_permanentes_ids': fields.one2many('doctor.hc.odontologia_odonto_per', 'hc_odontologia_id','Dientes Permanentes', states={'cerrada': [('readonly', True)]} ),
		'dientes_temporales_ids': fields.one2many('doctor.hc.odontologia_odonto_temp', 'hc_odontologia_id','Dientes Temporales', states={'cerrada': [('readonly', True)]} ),


		'state': fields.selection([('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 'Estado', readonly=True,	 required=True),
	}

	_constraints = [
		
	]

	_defaults = {
		'patient_id': lambda self, cr, uid, context: context.get('patient_id', False),
		'img_odontograma': _get_default_signature,
		'examen_estomatologico_ids': _get_default_estomatologicos,
		'dientes_permanentes_ids' : _get_default_dientes_permanentes,
		'dientes_temporales_ids': _get_default_dientes_temporales,
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
		'habitos_orales' : 'No registra ...',
		'analisis_atencion' :  'No registra ...',
		'state': 'abierta',
	}


	def import_file(self, cr, uid, ids, context=None):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(data)) 

		# your treatment
		return True

doctor_hc_odontologia()

class Odontograma_dientes_perma(osv.osv):

	_name = 'doctor.hc.odontologia_odonto_per'

	_columns = {
		'hc_odontologia_id' : fields.many2one('doctor.hc.odontologia','Historia Clinica Odontologia'),
		'diente_perma_id': fields.many2one('doctor.hc.odontologia.diente','Diente Permanente'),
		'diagnostico_diente': fields.char('DX'),
	}

Odontograma_dientes_perma()

class Odontograma_dientes_temp(osv.osv):

	_name = 'doctor.hc.odontologia_odonto_temp'

	_columns = {
		'hc_odontologia_id' : fields.many2one('doctor.hc.odontologia','Historia Clinica Odontologia'),
		'diente_temp_id': fields.many2one('doctor.hc.odontologia.diente_tempo','Diente Temporal'),
		'diagnostico_diente': fields.char('DX'),
	}


Odontograma_dientes_temp()


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


	_constraints = [
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
		'diente' : fields.char('Diente', required=True),
		'procedimiento_id' : fields.many2one('product.product', 'Procedimiento', required=False),
		'superficie_diente' : fields.char('Superficie dental'),
		'fecha': fields.datetime('Fecha', readonly=True, store=True),
		'nota' : fields.text('Nota'),
		'plantilla_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas'),
	}

	def onchange_plantillas(self, cr, uid, ids, plantilla_id, context=None):
		res={'value':{}}
		if plantilla_id:
			cuerpo = self.pool.get('doctor.attentions.recomendaciones').browse(cr,uid,plantilla_id,context=context).cuerpo
			res['value']['nota']=cuerpo
		else:
			res['value']['nota']=''
		return res

	_defaults = {
		'fecha': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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

