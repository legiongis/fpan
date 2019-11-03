from django.conf import settings
from arches.app.models.models import Node, GraphModel
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.search import elasticsearch_dsl_builder as edb
from fpan.search.elasticsearch_dsl_builder import Type

from .accounts import check_anonymous, check_scout_access, check_state_access

def apply_advanced_docs_permissions(dsl, request):

    ## allow superuser admins to get full access to everything
    if request.user.is_superuser:
        return dsl

    docs_perms = settings.RESOURCE_MODEL_USER_RESTRICTIONS
    doc_types = get_doc_type(request)

    for doc in doc_types:
        
        print "DETERMINING FILTER:", doc
    
        ## skip if there is no advanced permissions set for this doc type
        if not doc in docs_perms:
            print "skipping because no perms in settings.py"
            continue

        ## standard, basic check to apply restrictions to public users
        if check_anonymous(request.user):
            filter = docs_perms[doc]['public']

        ## alternative, FPAN-specific scenarios
        elif check_scout_access(request.user):
            filter = docs_perms[doc]['scout']

        elif check_state_access(request.user):
            filter = docs_perms[doc]['state']
        
        # now interpret the filter. if no access is granted it's very easy
        if filter['access_level'] == "no_access":
            dsl = add_doc_specific_criterion(dsl, doc, doc_types, no_access=True)
        
        # if a node value match (resource instance filtering) is required, a bit more
        # logic is required to determine what that node value is
        elif filter['access_level'] == "match_node_value":
        
            criterion = {'node_name': filter['match_config']['node_name']}
            
            if filter['match_config']['match_to'] == "<username>":
                criterion['value'] = request.user.username
            
            # here's where the complex, FPAN state filtering is acquired
            elif check_state_access(request.user):
                criterion['value'] = get_state_node_match(request.user)
            
            # generic allowance for specific, non-user-derived values to be passed in
            else:
                criterion['value'] = filter['match_config']['match_to']
            
            print criterion
            # apply criterion to dsl
            dsl = add_doc_specific_criterion(dsl, doc, doc_types, criterion=criterion)

    return dsl

def get_state_node_match(user, doc_perms):
    return "asdf"
    

def get_term_perm_details(user, doc_perms):

    filter = None

    if check_anonymous(user):
        filter = doc_perms['default']['level']

    elif check_scout_access(user):
        filter = doc_perms['Scout']['term_filter']
        filter['value'] = user.username

    elif check_state_access(user):
    
        print "this is a state USER"
    
        ## figure out what state group the user belongs to
        for sg in STATE_GROUP_NAMES:
            if user.groups.filter(name=sg).exists():
                state_group_name = sg
                break
        print "state group name:"
        print state_group_name

        ## return false for a few of the state agencies that get full access
        if state_group_name in ["FMSF","FL_BAR"]:
            return None
        else:
            filter = doc_perms['State']['term_filter']
        ## get full agency name to match with node value otherwise
        if state_group_name == "StatePark":
            filter['value'] = 'FL Dept. of Environmental Protection, Div. of Recreation and Parks'
        elif state_group_name == "FL_AquaticPreserve":
            filter['value'] = 'FL Dept. of Environmental Protection, Florida Coastal Office'
        elif state_group_name == "FL_Forestry":
            filter['value'] = 'FL Dept. of Agriculture and Consumer Services, Florida Forest Service'
        elif state_group_name == "FWC":
            filter['value'] = 'FL Fish and Wildlife Conservation Commission'
        else:
            print state_group_name + " not handled properly"

    return filter

def add_doc_specific_criterion(dsl, spec_type, all_types, no_access=False, criterion=False):

    print "adding criterion:"
    print criterion

    paramount = edb.Bool()
    for doc_type in all_types:

        ## add special string filter for specified node in type
        if doc_type == spec_type:

            ## if no_access is the permission level for the user, exclude doc
            if no_access is True:
                print "restricting access"
                paramount.must_not(Type(type=doc_type))
                continue

            elif criterion is not False:
                node = Node.objects.filter(graph_id=spec_type,name=criterion['node_name'])
                if len(node) == 1:
                    nodegroup = str(node[0].nodegroup_id)
                else:
                    nodegroup = ""
                    print "error finding specified node '{}', criterion ignored".format(criterion['node_name'])
                    continue

                new_string_filter = edb.Bool()
                new_string_filter.must(edb.Match(field='strings.string', query=criterion['value'], type='phrase'))
                new_string_filter.filter(edb.Terms(field='strings.nodegroup_id', terms=[nodegroup]))
                # new_string_filter.should(Type(type="73889292-d536-11e7-b3b3-94659cf754d0"))
                nested = edb.Nested(path='strings', query=new_string_filter)

                ## manual test to see if any criteria have been added to the query yet
                f = dsl._dsl['query']['bool']['filter']
                m = dsl._dsl['query']['bool']['must']
                mn = dsl._dsl['query']['bool']['must_not']
                s = dsl._dsl['query']['bool']['should']

                ## if they have, then the new statement needs to be MUST
                if f or m or mn or s:
                    paramount.must(nested)

                ## otherwise, use SHOULD
                else:
                    paramount.should(nested)

        ## add good types
        else:
            paramount.should(Type(type=doc_type))

    dsl.add_query(paramount)
    print dsl
    return dsl

def get_doc_type(request):

    type_filter = request.GET.get('typeFilter', '')
    use_ids = []

    if type_filter != '':
        type_filters = JSONDeserializer().deserialize(type_filter)

        ## add all positive filters to the list of good ids
        pos_filters = [i['graphid'] for i in type_filters if not i['inverted']]
        for pf in pos_filters:
            use_ids.append(pf)

        ## if there are negative filters, make a list of all possible ids and
        ## subtract the negative filter ids from it.
        neg_filters = [i['graphid'] for i in type_filters if i['inverted']]
        if len(neg_filters) > 0:
            all_rm_ids = GraphModel.objects.filter(isresource=True).values_list('graphid', flat=True)
            use_ids = [str(i) for i in all_rm_ids if not str(i) in neg_filters]

    else:
        resource_models = GraphModel.objects.filter(isresource=True).values_list('graphid', flat=True)
        use_ids = [str(i) for i in resource_models]

    if len(use_ids) == 0:
        ret = []
    else:
        ret = list(set(use_ids))
    return ret
