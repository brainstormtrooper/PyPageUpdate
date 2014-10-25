# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import re
import sys
import locale
import argparse
import glob

class PTT:
	""" Class doc """

	
	"""
	configuration:
	"""
	# Define the prefix for editable regions (the class attribute):
	tpl_editable_class_prefix = 'PTT_Editable' #None
	
	# Library items prefix:
	lbi_class_prefix = 'PTT_LibraryItem__'
	
	# Identify template being used:
	tpl_applied_template_prefix = 'PTT_template_used__'
	tpl_file_suffix = '.html'
	
	"""
	
	Where are the files:
		
		images should be in ./www/img/
		stylesheets should be in ./www/css/
		...
		for example
		...	
		
	"""
	
	html_path = './www/html/'
	template_path = './templates/'
	library_path = './library/'
	
	
	
	
		
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def ptt_Get_Lambda(self, soup, target, plural=False):
		"""
		Gets an element (or elements) matching a certain class selector
		
		"""
		
		if plural is True:
			result = []
			telements = soup.find_all(class_ = re.compile(target))
			print '[ii] Wow, I got all these Lambda elements ! : ' + str(telements) + ' for target : ' + target
			for telement in telements:				
				telementclasses = telement.get("class")
				for telementclass in telementclasses:
					if target in telementclass:
						#filename = telementclass.split("__")[1] + ".lbi"
						result.append([telement, telementclass])
					else:
						result.append([telement, None])
		else:
			
			result = [None, None]
			telement = soup.find(class_ = re.compile(target))
			
			if telement is not None:
				telementclasses = telement.get("class")
				for telementclass in telementclasses:
					if target in telementclass:
						#filename = telementclass.split("__")[1] + ".bli"
						result = [telement, telementclass]
					else:
						result = [telement, None]
		
		return result
		
		
							
	def ptt_filterClasses(self, classes, target):
		"""
		Looks for @target in a list of @classes
		"""
		result = None
		telementclasses = telement.get("class").split(' ')
		for telementclass in telementclasses.items():
			if target in telementclass:
				result = telementclass
				
		return result
		


	def ptt_get_lbis(self, soup):
		"""
		Uses ptt_Get_Lambda to return a list of library elements...
	
		"""
		lbis = self.ptt_Get_Lambda(soup, self.lbi_class_prefix, True)
		return lbis
		
	
#  
#  name: unknown
#  @param
#  @return
#  
	
	def ptt_updateLbiFromPage(self, target, lbi):
		pass
	
	def ptt_Main_lbis_update(self, soup):
		"""
		This function should update the library items in the given page (soup). 
		It should find library items identified bu their class and replace them with the contents of the appropriate file. 
		The contents of any editable areas should be withheld beforehand. 
		"""
		lbis = self.ptt_get_lbis(soup)
		for lbi, lbiclass in lbis:
			
			#
			# Get the lbi name
			# Read the file into soup
			# Update the page
			#			
		
			telementclasses = lbi.get("class")
			for telementclass in telementclasses:
				if self.lbi_class_prefix in telementclass:
					lbifile = self.library_path + telementclass.split("__")[1] + ".lbi"
					lbisoup = self.ptt_openElementFile(lbifile).html.body.contents[0]
					print '[ii] Got lbi soup : ' + str(lbisoup)
					print '[ii] Got target lbi : ' + str(soup.find_all(True, {"class" : telementclass }))
					lbieditables = self.ptt_holdEditables(soup)
					for l in soup.find_all(True,{ "class" : telementclass }):
						l.replace_with(lbisoup)
						#soup = soup.find_all(True,{ "class" : telementclass }).replace_with(lbisoup)
					# soup = soup(attrs={"class" : telementclass }).replace_with(lbisoup)
					newSoup = self.ptt_writeEditables(soup, lbieditables)
		return newSoup
		
	def ptt_lbi_update_in_folder(self, lbi, folder):
		pass
			
	
	def ptt_Has_Template(self, soup):
		
		templatetag = self.ptt_Get_Lambda(soup, self.tpl_applied_template_prefix)
		if None in templatetag:
			print '[ww] No template found'
			return False
		else:
			print '[ii] found telmplate tag ' + str(templatetag[1])
			return templatetag[1].split("__")[1] + self.tpl_file_suffix
			
	
	def ptt_Make_Template(self, target):
		pass
	
	def ptt_Main_Apply_Template(self, template, target):
		"""
		Replace the code outside editable blocks with the updated template code
		
		@Param:
		template -- the template file name (from has_template)
		target -- the soup of the current content file
		
		@Return:
		result -- the new soup
		 
		"""
		
		templatepath = self.template_path + template
		self.templatesoup = self.ptt_openElementFile(templatepath)
		self.targetsoup = target
		# 
		# Should get editables from content page (target)
		#
		print '============================ \n # 1) [ii] Apply Template : getting editables from content page...'
		editableareas = self.ptt_holdEditables(target)
		
		#
		# Now we should be able to write the editables (content from old page) into the now updated template...
		#
		print '============================ \n # 2) [ii] Apply Template : rewriting content (editables) to new template page (first run to get lbis into page)...'
		newsoup = self.ptt_writeEditables(self.templatesoup, editableareas)
		print '[dd] Apply Template : First run at applying editables gave : \n **********\n' + str(newsoup) + '\n ***********'
		
		
		
		#
		# Now that we have the editables for the actual page, we'll get the new parts and apply them to the TEMPLATE in use
		#
		#print '============================ \n # 2) [ii] Apply Template : Updating library items in template...'
		#self.templatesoup = self.ptt_Main_lbis_update(self.templatesoup)
		
	
		#
		# Now that we have the editables for the actual page, we'll get the new parts and apply them to the TEMPLATE in use
		#
		print '============================ \n # 3) [ii] Apply Template : Updating library items in whole page...'
		newsoup = self.ptt_Main_lbis_update(newsoup)
		
		#
		# Try running this twice to get the lbis in the contentarea AND their contents...
		#
		print '============================ \n # 4) [ii] Apply Template : rewriting content (editables) to new template page (final run to get contents into lbis)...'
		newsoup = self.ptt_writeEditables(newsoup, editableareas)
		
		return str(newsoup)
		
	def ptt_writeEditables(self, soup, editables):
		if editables:
			if soup:
				# for editableclass, editable in editables.items():
				for editableid, editable in editables.items():
					# 
					# Replace stuff
					#
			
					# destination = soup.select("."+editableclass)[0]
					destination = soup.find(id=editableid)
					print '[dd] ??? destination ??? : trying to replace ' + str(destination) + ' with ' + str(editable)
					if destination:
						destination.replace_with(editable)
					else:
						print '[ww] !!! write editables : No destination for editable : ' + editableid
			return soup
	
	def ptt_holdEditables(self,soup):
		""" 
		Collect the contents of editable regions for safe keeping while the page is updated. 
		
		"""
		
		editables = self.ptt_Get_Lambda(soup, self.tpl_editable_class_prefix, True)
		if editables:
			editablescontainer = {}
			for editable in editables:
				
				try:
					# ename = editable[1].split("__")[1]
					print '[dd] holdEditables : editable "' + editable[0]["id"] + '"  is : ' + str(editable[0])
					eid = editable[0]["id"]
					editablescontainer[eid] = editable[0]
				except:
					e = sys.exc_info()[0]
					print "[EE] Error : %s" % e
				
			print '[ii] got editables to hold : ' + str(editablescontainer)
		else:
			editablescontainer = None
		return editablescontainer
		
	def ptt_uid_is_unique(self, uid):
		pass

	
	def ptt_Main_Update_Template(self, template, target):
		"""
		Same as apply template (just REapplies the template)
		"""
		pass	
		
		
	def ptt_Main_Remove_Template(self, target):
		pass
	
	def ptt_Update_Templates_In_Folder(self, template, Folder):
		pass
	
	def ptt_openElementFile(self, elementFile):
		soup = BeautifulSoup(open(elementFile, 'r'))
		return soup
	
	
	
te = PTT()

"""
parser = argparse.ArgumentParser(description='Process some pages.')
parser.add_argument('targetpage', metavar='targetpage', type=str,
                   help='target page to acto on by default')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
"""

import glob
path = te.html_path + "*.html"
for filename in glob.glob(path):

	print '********' + filename + '*****************'
	fpath = te.html_path + filename
	if ".directory" not in filename:
		with open(filename, 'r') as html_file:
			soup = BeautifulSoup(html_file)
			
			#
			# find the template
			#
			template = te.ptt_Has_Template(soup)
			if template:
				print 'got a file with a template! : ' + template
				
				result = te.ptt_Main_Apply_Template(template, soup)
				print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
				print result
				print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
				#templatefile = 
			else:
				print 'Bummer, no template...'
			
			
			#
			# find the library items
			#
			
			
			
			
			#
			# update the library items
			#
			
			#
			# update template
			#
			
			#if soup.html.body.find(**, {"class" : "articlearecuperer"}) is not None:

