# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields

class Professio(ModelSQL, ModelView):
    """Professio per una persona dins l'arbre Garreta.
    """
    _name = 'professio'
    _description = __doc__
    _rec_name = 'nom'

    nom = fields.Char('Nom')
    descripcio = fields.Text('Descripcio')

Professio()

class Persona(ModelSQL, ModelView):
    """Persona dins de l'arbre Garreta.
    """
    _name = 'persona'
    _description = __doc__

    def get_fills(self, ids, name):
        """Retorna els fills on pare o mare apuntin
        """
        field_dict = {'H': 'pare', 'D': 'mare'}
        res = {}
        for persona in self.browse(ids):
            field_search = field_dict[persona.sexe]
            res[persona.id] = self.search([(field_search, '=', persona.id)])
        return res

    def get_matrimonis(self, ids, name):
        """Retorna els matrimonis.
	"""
	res = {}
	matrimoni_obj = self.pool.get('matrimoni')
	for persona in self.browse(ids):
	    search_params = [['OR', [('persona1.id', '=', persona.id)],
	                            [('persona2.id', '=', persona.id)]
			    ]]
	    res[persona.id] = matrimoni_obj.search(search_params)
	return res

    def set_matrimonis(self, ids, name, value):
        matrimoni_obj = self.pool.get('matrimoni')
        if not value:
            return
        for act in value:
            print act
            if act[0] == 'create':
                act[1]['persona1'] = ids[0]
                matrimoni_obj.create(act[1])
            elif act[0] == 'write':
                matrimoni_obj.write(act[1], act[2])
            elif act[0] in ('delete', 'unlink'):
                matrimoni_obj.delete(act[1])


    def get_conjugue_actual(self, ids, name):
        res = {}
	matrimoni_obj = self.pool.get('matrimoni')
	for persona in self.browse(ids):
	    search_params = [['OR', [('persona1.id', '=', persona.id)],
	                            [('persona2.id', '=', persona.id)],
		             ],
			     ('data_final', '=', False)]
	    results = matrimoni_obj.search(search_params, limit=1, 
	                                   order=[('data_inici', 'DESC')])
	    if results:
		matrimoni = matrimoni_obj.browse(results[0])
                if matrimoni.persona1.id != persona.id:		
	            res[persona.id] = matrimoni.persona1.id
                else:
                    res[persona.id] = matrimoni.persona2.id
            else:
	        res[persona.id] = False
        return res


    def get_nom_complet(self, ids, name):
        """Retorna el nom complet.
        """
	res = {}
	for persona in self.browse(ids):
	    res[persona.id] = '%s %s, %s' % (persona.cognom1, persona.cognom2,
	                                     persona.nom)
	return res

    def search_nom_complet(self, name, clause):
        return []

    name = fields.Function(fields.Char('Nom complet'), 'get_nom_complet')
    nom = fields.Char('Nom')
    cognom1 = fields.Char('Primer Cognom')
    cognom2 = fields.Char('Segon Cognom')
    pare = fields.Many2One('persona', 'Pare', ondelete='RESTRICT')
    mare = fields.Many2One('persona', 'Mare', ondelete='RESTRICT')
    data_naixement = fields.Date('Data Naixement')
    lloc_naixement = fields.Char('Lloc de Naixement')
    sexe = fields.Selection([('H', 'Home'), ('D', 'Dona')], 'Sexe', required=True)
    fills = fields.Function(fields.One2Many('persona', None, 'Fills',
        order=[('data_naixement', 'ASC')]), 'get_fills')
    data_obit = fields.Date(u'Data Òbit')
    lloc_obit = fields.Char(u'Lloc Òbit')
    professio = fields.Many2One('professio', u'Professió', ondelete='RESTRICT')
    notes = fields.Text('Notes')
    conjugue_actual = fields.Function(fields.Many2One('persona', u'Cònjugue actual'),
        'get_conjugue_actual')
    matrimonis = fields.Function(fields.One2Many('matrimoni', None, 'Matrimonis',
        order=[('data_final', 'DESC')]), 'get_matrimonis', setter='set_matrimonis')
                                       

Persona()

class Matrimoni(ModelSQL, ModelView):
    """Unio entre dues persones.
    """
    _name = 'matrimoni'
    _description = __doc__

    persona1 = fields.Many2One('persona', u'Cònjugue 1')
    persona2 = fields.Many2One('persona', u'Cònjugue 2')
    data_inici = fields.Date('Data inici')
    data_final = fields.Date('Data final')
    notes = fields.Text('Notes')

Matrimoni()
