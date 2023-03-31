import csv


# GLOBAL VARIABLES
VALID_PROPERTY_LIST = [
	"alarmEvalEnabled",
	"alarms",
	"clampMode",
	"datasource",
	"dataType",
	"deadband",
	"deadbandMode",
	"deriveExpressionGetter",
	"deriveExpressionSetter",
	"documentation",
	"enabled",
	"engHigh",
	"engLimitMode",
	"engLow",
	"engUnit",
	"eventScripts",
	"executionMode",
	"expression",
	"formatString",
	"historicalDeadband",
	"historicalDeadbandMode",
	"historicalDeadbandStyle",
	"historyEnabled",
	"historyMaxAge",
	"historyMaxAgeUnits",
	"historyProvider",
	"historySampleRate",
	"historySampleRateUnits",
	"historyTagGroup",
	"historyTimeDeadband",
	"historyTimeDeadbandUnits",
	"name",
	"opcItemPath",
	"opcServer",
	"query",
	"queryType",
	"rawHigh",
	"rawLow",
	"readOnly",
	"readPermissions",
	"sampleMode",
	"scaledHigh",
	"scaledLow",
	"scaleFactor",
	"scaleMode",
	"sourceTagPath",
	"tagGroup",
	"tagType",
	"tooltip",
	"typeId",
	"value",
	"valueSource",
	"writePermissions"]


# Global Local Functions

# Find the parent folder from tag path
def _parentFolder (inString):
	index = inString.rfind('/')
	return inString[:index]


# Find point name from tag path
def _pointName (inString):
	index = inString.rfind('/')
	return inString[index+1:]

# Property/tag import tool
def writeTags(validateProperties = True):
	"""CSV Tag Write Script.
	
	Script takes tags and properties from a .csv file and updates tag browser with
		new values. If a folder path or tag does not exist it will be created. Properties
	 	will be overwritten if tag is in a UDT instance. 
	 The First column must be labelled "name".
	 Can add any number of properties (columns) and tags (rows) to the CSV.
	
	Args:
		validateProperties: Check whether the property exist before adding to tag. Disable
			to add/modify custom properties.
	
	CSV File Structure Example:
	1		name			|	Property1	|	Property2	|	Property3....
		-------------------------------------------------------------------------
	2		Tag Path		| 	value1		|	value2		|	value3
	
	CSV Example:
	1		name			|	dataType	| 	valueSource	|	engUnit
		-------------------------------------------------------------------------
	2		Test/Tag 1		| 	Float8		|	opc			|	L/s
	3		Test/Tag 2		| 	Int4		| 	derived		|	mm
	
	"""	
	importPath = system.file.openFile('csv', 'C:')
	
	if importPath is None:
	    print 'File not selected'
	    exit()
	
	with open(importPath,'r') as importFile:
		dataReader = csv.DictReader(importFile)
		
		# display properties that will be modified
		print ("----------------------------")
		print "Modifying the following properties:"
		for field in dataReader.fieldnames:
			if validateProperties:
				if field in VALID_PROPERTY_LIST and field != "name": print field
			elif field != "name":
				print field
		config = {}
		print ("----------------------------")
		print ("Writing Tags...")
		
		for row in dataReader:
			# read row 'Name'. Grab parent folder path and point name
			path = _parentFolder(row['name'])
			tagName = _pointName(row['name'])
			row['name'] = tagName
			
			# If validate properties is enabled, check property actually exist before adding to config
			if validateProperties: config = {k:v for(k, v) in row.items() if k in VALID_PROPERTY_LIST}
			else: config = row
			
			# configure tag
			print system.tag.configure(path,[config],"m")
