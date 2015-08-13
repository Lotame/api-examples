#
# Print to the console all available hierarchy nodes and the number of 3rd party uniques for each. The output is in csv format and intended for later import into a spreadsheet for easier viewing.
# 
import sys, json, argparse, lotame_utils
# force everything to play nice for shell redirects, etc...
reload(sys)
sys.setdefaultencoding("utf-8")

parser = argparse.ArgumentParser()

parser.add_argument('-user', help='API username', required=True)
parser.add_argument('-pw', help='API password', required=True)
parser.add_argument('-clientid', help='ID of client for which to scope all API calls', required=True)

args = parser.parse_args()

# Output the name, path, behaviorId, and 3rd party uniques for the supplied node within the supplied hierarchy, in csv format.
def outputNode(hierarchy, node):
	uniques = 0
	stats = node["statsSet"]
	if stats != None:
		thirdPartyOverlap = stats["thirdPartyOverlapStats"]
		if thirdPartyOverlap != None:
			uniques = thirdPartyOverlap["uniques"]
	path = node["pathToRoot"]

	# nodes in an "ORIGINAL" hierarchy do not include their "root" in the pathToRoot attribute, but all other hierarchies do. The root is just the name of the hierarchy.
	# "ORIGINAL" corresponds to what is displayed in the Audience Builder UI as "Standard"
	if hierarchy["hierarchyType"] == "ORIGINAL":
		path = hierarchy["name"] + "^" + path

	print "\"" + node["name"] + "\",\"" + path + "\"," + node["behaviorId"] + "," + str(uniques)
	outputChildren(hierarchy, node)

# recursively output child nodes of the supplied node within the supplied hierarchy
def outputChildren(hierarchy, node):
	children = node["childNodes"]
	if children != None:
		for childNode in children:
			outputNode(hierarchy, childNode)

# main
hierarchyList = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/hierarchies?view=LAB&client_id=" + args.clientid).json()
for hierarchy in hierarchyList["hierarchies"]:
	hierarchyMeta = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/hierarchies/" + hierarchy["id"] + "?depth=2&universe_id=1&client_id=" + args.clientid).json()
	nodes = hierarchyMeta["nodes"]
	if nodes != None:
		for node in nodes:
			outputNode(hierarchy, node)
			