# ------------------------------------------------------------------------------------------------
# Script name: Delete_Extra_Domains.py
# Created on: March 15, 2015
# Author: Hayden Elza
# Purpose: This script is meant to delete incorrect (non-default) domains from our Bordner project
# 			geodatabases. To do this, the script first removes all domains from the fields so
#			that the domain can be deleted. This itereates over all feature classes and fields
#			within those feature classes.
# Version: 1.0
# History:
# -------------------------------------------------------------------------------------------------

import arcpy


# Enviromental Variables
# Prompt user for the geodatabase location
gdb = raw_input("Enter workspace, example: \\MLADENOFF9020\share\Bordner\Users\Ryan\bordner_townships_attributed_1.gdb >>> ")
arcpy.env.workspace = gdb
# Hard coding for use in sublime text 2
#arcpy.env.workspace = r'\\MLADENOFF9020\share\Bordner\Users\Ryan\bordner_townships_attributed_1.gdb' #Database to iterate over
#gdb = arcpy.env.workspace


#---------------------------------------
# Define Functions
#---------------------------------------

# Function used to remove domains from fields so that the domains can be deleted
def removeDomainsFromFields():
	# Build list of feature classes within database
	featureClasses = arcpy.ListFeatureClasses()

	# Iterate over feature classes
	for fc in featureClasses:
		# Show progress, i.e., what feature class of the total feature classes
		print "\n" + str(featureClasses.index(fc)+1) + " of " + str(len(featureClasses)) + ": " + fc
		# Build list of fields witin feature class
		fieldNames = [foo.name for foo in arcpy.ListFields(fc)]
		# Iterate over fields
		for fn in fieldNames:
			print fn
			try:
				# Remove Domain From Field
				arcpy.RemoveDomainFromField_management(fc, fn)
			# Gracefully capture errors
			except Exception as e:
				# Print error messages
				print e.message
				# Use AddError to report message when using script tool
				arcpy.AddError(e.message)

# Function to delete the extra domains that do not belong
def deleteDomains(gdb):
	# Define list of the default domains (edit to fit your application), these are the domains that should not be deleted
	defaultDomains = [
		"DensityNum",
		"CoverType",
		"JudgementShort",
		"MinimumDiameter",
		"MaximumDiameter",
		"CoverNum"
		]
	# Build list of domains
	domains = [foo.name for foo in arcpy.da.ListDomains()]

	# Delete domains that are not in default domains list
	for domain in domains:
		if domain not in defaultDomains:
			# Delete domain from geodatabase
			arcpy.DeleteDomain_management(gdb,domain)
			print domain,"deleted"


#---------------------------------------
# Main
#---------------------------------------

# Remove domains from fields
print "Starting to remove domains from fields..."
removeDomainsFromFields()

# Delete non-default domains
print "Sarting to delete domains that are not default..."
deleteDomains(gdb)

print "Done."
