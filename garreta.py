# -*- coding: utf-8 -*-

from trytond.model import ModelView, ModelSQL, fields

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

    def get_nom_complet(self, ids, name):
        """Retorna el nom complet.
        """
	res = {}
	for persona in self.browse(ids):
	    res[persona.id] = '%s %s, %s' % (persona.cognom1, persona.cognom2,
	                                     persona.nom)
	return res

    name = fields.Function(fields.Char('Nom complet'), 'get_nom_complet')
    nom = fields.Char('Nom')
    cognom1 = fields.Char('Primer Cognom')
    cognom2 = fields.Char('Segon Cognom')
    pare = fields.Many2One('persona', 'Pare', ondelete='RESTRICT')
    mare = fields.Many2One('persona', 'Mare', ondelete='RESTRICT')
    data_naixement = fields.Date('Data Naixement')
    lloc_naixement = fields.Char('Lloc de Naixement')
    sexe = fields.Selection([('H', 'Home'), ('D', 'Dona')], 'Sexe')
    fills = fields.Function(fields.One2Many('persona', None, 'Fills'),
                            'get_fills')
    data_obit = fields.Date('Data Obit')
    lloc_obit = fields.Char('Lloc Obit')
    notes = fields.Text('Notes')
    

Persona()

class Professio(ModelSQL, ModelView):
    """Professio per una persona dins l'arbre Garreta.
    """
    _name = 'professio'
    _description = __doc__

    nom = fields.Char('Nom')
    descripcio = fields.Text('Descripcio')

Professio()

class Matrimoni(ModelSQL, ModelView):
    """Unio entre dues persones.
    """
    _name = 'matrimoni'
    _description = __doc__

    persona1 = fields.Many2One('persona', 'Conjugue 1')
    persona2 = fields.Many2One('persona', 'Conjugue 2')
    data_inici = fields.Date('Data inici')
    data_final = fields.Date('Data final')
    notes = fields.Text('Notes')

Matrimoni()
