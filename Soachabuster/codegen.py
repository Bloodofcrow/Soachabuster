from os import mkdir
from os.path import exists, dirname, join
import jinja2
from entity_test import get_entity_mm

def main(debug=False):

	this_folder = dirname(__file__)

	entity_mm = get_entity_mm(debug)

	person_model = entity_mm.model_from_file(join(this_folder, 'entidades.ent'))

	def javatype(s):
		return {
				'integer' : 'int',
				'string' : 'String'
		}.get(s.name, s.name)

	srcgen_folder = join(this_folder, 'SoachaBusterWeb')
	if not exists(srcgen_folder):
		mkdir(srcgen_folder)

	jinja_env = jinja2.Environment(
		loader = jinja2.FileSystemLoader(this_folder),
		trim_blocks = True,
		lstrip_blocks = True)

	#Primero se carga el template.
	template = jinja_env.get_template('agregar.template')
	#Se ejecuta un for para generar todas las entidades.
	for entity in person_model.entities:
		with open(join(srcgen_folder, "agregar%s.html" % entity.name.capitalize()), 'w') as f:
			f.write(template.render(entity = entity))

	template = jinja_env.get_template('consultar.template')
	for entity in person_model.entities:
		with open(join(srcgen_folder, "consultar%s.html" % entity.name.capitalize()), 'w') as f:
			f.write(template.render(entity = entity))

	template = jinja_env.get_template('listar.template')
	for entity in person_model.entities:
		with open(join(srcgen_folder, "listar%s.html" % entity.name.capitalize()), 'w') as f:
			f.write(template.render(entity = entity))

if __name__ == "__main__":
    main()
