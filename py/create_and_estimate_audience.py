#
# Create a reach estimate for an audience and save the resulting audience. 
# This example creates and audience of the form "(A OR B) AND C" where A,B, and C are chosen dynamically as follows:
#
# A = first node from the Lotame standard hierarchy, using only first party data
# B = second node from the Lotame standard hierarchy, using first and third party data
# C = first node from the first branded hierarchy returned by the API.
#
# The audience defaults to "Enrich", which means overlap with the clients inventory. Use the argument -extend to build
# the audience on "Extend".
#
# Note: the ids used in this example may not be accessible to all user accounts.
# 
import datetime, time, sys, json, argparse, lotame_utils

# force everything to play nice for shell redirects, etc...
reload(sys)
sys.setdefaultencoding("utf-8")

parser = argparse.ArgumentParser()

parser.add_argument('-user', help='API username', required=True)
parser.add_argument('-pw', help='API password', required=True)
parser.add_argument('-clientid', help='ID of client for which to scope all API calls', required=True)
parser.add_argument('-extend', help='Build the audiences on extend instead of enrich', action='store_true')
args = parser.parse_args()

# Get hierarchies
hierarchyList = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/hierarchies?view=LAB&client_id=" + args.clientid).json()

# Find the nodes we want to use. The standard hierarchies are identified by default=true, while
# a branded hierarchy has a hierarchyType of "BRANDED", and the ownerClientId represents the client from which data is purchased
nodeA = None
nodeB = None
nodeC = None
for hierarchy in hierarchyList["hierarchies"]:
	if nodeA == None and hierarchy["default"] == True:
		# This is the standard hierarchy, grab the first two nodes for our A or B expression that we'll build later		
		hierarchyMeta = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/hierarchies/" + hierarchy["id"] + "?depth=2&universe_id=1&client_id=" + args.clientid).json()
		if hierarchyMeta["purchasable"] == True:
			nodes = hierarchyMeta["nodes"]
			if nodes != None:
				nodeA = {"clientId":hierarchyMeta["ownerClientId"],"node":nodes[0]}
				nodeB = {"clientId":hierarchyMeta["ownerClientId"],"node":nodes[1]}
	elif nodeC == None and hierarchy["hierarchyType"] == "BRANDED":
		# this is the branded hierarchy, grab the first purchasable node for the C part of our expression.
		hierarchyMeta = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/hierarchies/" + hierarchy["id"] + "?depth=2&universe_id=1&client_id=" + args.clientid).json()
		if hierarchyMeta["purchasable"] == True:
			for node in hierarchyMeta["nodes"]:
				if node["purchasable"] == True:
					nodeC = {"clientId":hierarchyMeta["ownerClientId"],"node":node}
					break;

	if nodeA != None and nodeB != None and nodeC != None:	
		break

if nodeB == None:
	print "You do not have access to any purchasble nodes in the standard categories"
elif nodeC == None:
	print "You do not have access to any purchasble branded nodes"	
else:
	# Build the expression that will define our audience

	# We will use only first party data for A, so we only need the behavior id and name that powers our chosen node.
	A = {}
	A["behavior"] = {}
	A["behavior"]["id"] = nodeA["node"]["behaviorId"]
	A["behavior"]["name"] = nodeA["node"]["name"]

	# We will use all available first and 3rd party data for B, so we add the purchased flag and who we are purchasing from (which is the owner of the node)
	B = {}
	B["behavior"] = {}
	B["behavior"]["id"] = nodeB["node"]["behaviorId"]
	B["behavior"]["name"] = nodeB["node"]["name"]
	B["cpm"] = nodeB["node"]["cpm"]
	B["purchased"] = "true"
	B["purchasableClientId"] = nodeB["clientId"]

	# Build the (A or B) component of the full audience expression. 
	# A component is a combination of "complexAudienceBehavior" objects, or other components, combined with an OR or AND operator
	AorB = {}
	AorB["component"] = []
	AorB["component"].append({"complexAudienceBehavior":A})
	AorB["component"].append({"complexAudienceBehavior":B, "operator":"OR"})

	# Build the branded data we are purchasing for this audience, this works the same way as the purchased standard category data.
	C = {}
	C["behavior"] = {}
	C["behavior"]["id"] = nodeC["node"]["behaviorId"]
	C["behavior"]["name"] = nodeC["node"]["name"]
	C["cpm"] = nodeC["node"]["cpm"]
	C["purchased"] = "true"
	C["purchasableClientId"] = nodeC["clientId"]

	# Combine our (A or B) subexpression to get our final '(A OR B) and C' expression by building another component
	definition = {}
	definition["component"] = [AorB, {"complexAudienceBehavior":C, "operator":"AND"}]

	# Put it all together into an audience object, which requires a client to own it and a name. We optionally define it as enrich
	# vs. extend by either including or excluding the overlap parameter, respectively.
	audience = {}
	audience["clientId"] = args.clientid
	audience["name"] = "Example Estimate - " + str(datetime.datetime.now())
	audience["definition"] = definition
	if not args.extend:
		audience["overlap"] = True
	
	# submit an estimate request
	print "Submit estimate with this json [y/n]?"
	print json.dumps(audience)
	if sys.stdin.readline().rstrip() == "y":
		response = lotame_utils.postRequest(args.user, args.pw, "https://api.lotame.com/2/audiences/reachEstimates", json.dumps(audience)).json()
		estimateId = response["id"]

		# You could optionally wait at this point for the estimate to complete and retrieve the results
		print "Wait for estimate " + estimateId + "? [y/n]"
		if sys.stdin.readline().rstrip() == "y":
			
			estimate = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/audiences/reachEstimates/" + str(estimateId)).json()
			while estimate["status"] != "COMPLETE":
				print "Waiting for estimate to complete..."
				time.sleep(60)
				estimate = lotame_utils.getRequest(args.user, args.pw, "https://api.lotame.com/2/audiences/reachEstimates/" + str(estimateId)).json()

			# find universe 1 estimate, universe 1 represents all traffic
			for result in estimate["results"]["ReachEstimateResult"]:
				if result["universeId"] == "1":
						print "Estimate: " + str(int(round(float(result["sampleMatches"])/float(result["sampleSize"])*float(estimate["populationSize"]))))

	# save the audience
	print "Save the audience? [y/n]"
	if sys.stdin.readline().rstrip() == "y":
		response = lotame_utils.postRequest(args.user, args.pw, "https://api.lotame.com/2/audiences", json.dumps(audience)).json()
		print "Saved with id = " + response["id"]
	