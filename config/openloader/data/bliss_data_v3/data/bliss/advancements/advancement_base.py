import os, json

namespace = 'bliss'

known_parents = []
known_advancements = ['root']

def fetch(name, icon, parent, targets=None, display_type='task'):
	if not targets:
		targets = [icon]
	if not type(targets) is list:
		if targets.endswith('.txt'):
			with open(targets) as infile:
				targets = infile.readlines()
			targets = [l.strip() for l in targets]
		else:
			targets = [targets]

	criteria = {}
	for t in targets:
		tname = t[(t.index(':') + 1):]
		criteria[tname] = {
			'trigger': 'minecraft:inventory_changed',
			'conditions': {
				'items': [ make_item(t) ]
			}
		}

	return adv(name, icon, criteria, parent, display_type)

def guard(name, parent):
	obj = {
		'parent': parent,
		'display': {},
		'criteria': {
			"has_parent": {
				"trigger": "minecraft:tick",
				"conditions": {
					"player": [
						{
							"condition": "minecraft:entity_properties",
							"entity": "this",
							"predicate": {
								"player": {
									"advancements": {
										parent: True
									}
								}
							}
						}
					]
				}
			}
		}
	}

	known_parents.append(parent)
	known_advancements.append(name)

	make(name, obj, 'guard')

def stub(name, icon, parent):
	criteria = {
		'impossible': {
			'trigger': 'minecraft:impossible'
		}
	}
	adv(name, icon, criteria, parent)

def adv(name, icon, criteria, parent, display_type='task'):
	if name in known_advancements:
		print(name, 'is already an advancement')
		exit(1)

	obj = {
		'parent': parent,
		'display': display(name, icon, display_type),
		'criteria': criteria
	}

	known_parents.append(parent)
	known_advancements.append(name)

	make(name, obj)

def display(name, icon, display_type='task'):
	title = ('advancement.{}.{}'.format(namespace, name))
	description = ('advancement.{}.{}.desc'.format(namespace, name))

	print('"{}": "TODO",'.format(title))
	print('"{}": "TODO",'.format(description))

	hidden = False
	if display_type == 'hidden':
		hidden = True
		display_type = 'challenge'

	return {
		'icon': make_icon(icon),
		'title': {
			'translate': title
		},
		'description': {
			'translate': description
		},
		'frame': display_type,
		'show_toast': True,
		'announce_to_chat': True,
		'hidden': hidden
	}

def make_item(item):
	return { 'tag': item[1:] } if item.startswith('#') else { 'items': [item] }

def make_icon(item):
	return { 'item': item }	

def make(name, obj, filedir=namespace):
	with open(file(name, filedir), 'w') as out:
		json.dump(obj, out, indent = 2, sort_keys = False)

def file(name, filedir=namespace):
	os.makedirs(filedir, exist_ok = True)
	return '{}/{}.json'.format(filedir, name)