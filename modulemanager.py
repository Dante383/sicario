#!/usr/bin/python

import sicario

import os
import importlib

class ModuleManager:
	modules = []
	modules_failed = []

	def load_modules (self, directory="modules/"):
		directories = os.listdir(directory)

		modules = []
		modules_failed = []

		for module in directories:
			if not os.path.isdir('modules/' + module):
				continue 

			if os.path.isfile('modules/' + module + '/' + module + '.py'):
				module_package = importlib.import_module('modules.' + module)
				module_class = getattr(getattr(module_package, module), module.capitalize())()
				module_class.start()
				self.modules.append(module_class)
			else:
				self.modules_failed.append(module)

		return [self.modules, len(self.modules), len(self.modules_failed)]

	def trigger_hook (self, hook_name, *args):
		for module in self.modules:
			module.trigger_hook(hook_name, args)