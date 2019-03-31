from .api_adapter import RestAdapter
from .utils import dget, confirmMatches, getSuggestions
from dateutil.parser import *
from datetime import *
from .arrow import *
from dateutil.relativedelta import *
from .answer import Answer


#ajout du feedback
class WikiDataAnswer(Answer):
    """Answer object from WikiData source"""

    TIME_VALUE = 'http://wikiba.se/ontology#TimeValue'
    QUANTITY_VALUE = 'http://wikiba.se/ontology#QuantityValue'

    def __init__(self, sparql_query, bindings=None, data=None):
        super(WikiDataAnswer, self).__init__()
        self.all_property = []
        self.sparql_desc = {}
        self.suggestions = {'subject' : [], 'prop' : []}
        self.sparql_query = sparql_query

        if bindings:
            self.bindings = bindings
            self.data = self.get_data(bindings)
        else:
            self.data = data

    def to_dict(self):
        d = super(WikiDataAnswer, self).to_dict()
        d['sparql_query'] = self.sparql_query
        d['all_property'] = self.all_property
        d['sparql_desc'] = self.sparql_desc
        d['suggestions'] = self.suggestions
        
        return d

    @staticmethod
    def get_data(bindings):
        """Gets values from the list of results"""
        print(bindings)
        return [WikiDataAnswer.get_value(b) for b in bindings]

    @staticmethod
    def get_value(data):
        """Gets Python type value from WikiData response field"""
        data_type = dget(data, 'type.value')
        value = dget(data, 'valLabel.value')

        if data_type == WikiDataAnswer.TIME_VALUE:
            dt = parse(value)
            dt = dt.replace(tzinfo=None)
            return dt
        elif data_type == WikiDataAnswer.QUANTITY_VALUE:
            if value.isdigit():
                return float(value)
            return value
        else:
            return value


class WikiData(RestAdapter):
    """REST Adapter for WikiData API endpoint"""
    WIKIDATA_URL = 'https://www.wikidata.org/w/api.php'
    WDSPARQL_URL = 'https://query.wikidata.org/sparql'

    def _query_wdsparql(self, query):
   
        params = {
            'format': 'json',
            'query': query
        }
        
        return self.get(self.WDSPARQL_URL, params=params)

    def _query_wikidata(self, params):

        return self.get(self.WIKIDATA_URL, params=params)

    def _search_entity(self, name, _type='item'):
        """Search for an entity from string"""

        if _type not in ['item', 'property']:
            return None

        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'search': name,
            'language': 'en',
            'type': _type,
        }

        data = self._query_wikidata(params)
        return data


    def _get_desc(self, subject):
        """Get WikiData description of subject"""
        #reponse
        answer = WikiDataAnswer(sparql_query=None)
        answer.feedback["property"] = "I did not find property in the query"
    
        #resultat de la recherche en json
        data = self._search_entity(subject)
        print("DATA-_get_desc_",data)
        #tableau correspondant aux resultats de la recherche
        search = dget(data, "search")
        print(search)
        
        #la recherche n'a rien donné
        if len(search) == 0 :
            print("search desc empty")
            answer.feedback["subject"] = "I did not find the subject : "+ subject.upper()
            answer.feedback["no_result"] = subject + " is probably misspelled"
                    
        #la recherche a trouvé quelque chose
        else :
            print("search desc full")
            #on verifie qu'il a bien trouvé ce qu'on cherche cad subject
            booleanMatches = confirmMatches(search,subject)
            print(booleanMatches)
            if True in booleanMatches:
                #le premier resultat de la recherche est retourné
                desc = dget(data, 'search.%d.description'%booleanMatches.index(True))
                subj_id = dget(data, 'search.%d.id'%booleanMatches.index(True))
                answer.data = desc
                answer.feedback["subject"] = "I found the subject : "+ subject.upper()
                answer.feedback["answer"] = "I give you the description of "+ subject.upper()
                answer.all_property = self._get_all_property_of_subj(subj_id)
                answer.suggestions["subject"] = getSuggestions(search)
            else :
                answer.feedback["subject"] = "I didn't find the subject : "+ subject.upper()
                answer.feedback["no_result"] = "but I can give you some suggestions in the tab 'DID YOU MEAN'"
                answer.suggestions["subject"] = getSuggestions(search)
            
        return answer


    def _get_id(self, name, _type='item'):
        """Get WikiData ID of a name"""
   
        idName = None
        suggestions = []
        
        item = self._search_entity(name, _type)
        print("ITEM-_get_id_",item)
        
        #tableau correspondant aux resultats de la recherche
        search = dget(item, "search")
        
        print(search)
        
        #la recherche n'a rien donné
        if len(search) == 0 :
            print("search id empty")

        #la recherche a trouvé quelque chose
        else :
            print("search id full")
            #on verifie qu'il a bien trouvé ce qu'on cherche cad subject
            booleanMatches = confirmMatches(search, name)
            print(booleanMatches)
            if True in booleanMatches:
                #le premier resultat de la recherche est retourné
                idName = dget(item, 'search.%d.id'%booleanMatches.index(True))
                print("voici l'idname retourné ... ",idName)
            suggestions = getSuggestions(search)
                
        return idName, suggestions


    def _get_property(self, subject, prop, prop_id=None):
        """Queries Wikidata to get property"""
        print("GET PROPERTY")
        
        answer = WikiDataAnswer(sparql_query=None)
        subj_id_found = False
        prop_id_found = False
        sugg_prop = []
        
        #on verifie au cas ou prop_id n'est pas definie
        subject_id, sugg_subj = self._get_id(subject, 'item')
        if not prop_id:
            prop_id, sugg_prop = self._get_id(prop, 'property')
        
        if not subject_id :
            answer.feedback["subject"] = "I did not find the subject : "+ subject.upper()
            answer.suggestions["subject"] = sugg_subj
            subj_id_found = False
        else :
            answer.feedback["subject"] = "I found the subject : "+ subject.upper()
            answer.sparql_desc[subject_id] = subject
            answer.suggestions["subject"] = sugg_subj
            subj_id_found = True

        if not prop_id:
            answer.feedback["property"] = "I did not find the property : " + prop.upper()
            answer.suggestions["prop"] = sugg_prop
            prop_id_found = False
        else :
            answer.feedback["property"] = "I found the property : " + prop.upper()
            answer.sparql_desc[prop_id] = prop
            answer.suggestions["prop"] = sugg_prop
            prop_id_found = True
            

        if subj_id_found and prop_id_found :
            if self._is_property_of_subj(subject_id, prop_id) :

                query = """
                SELECT ?valLabel ?type
                WHERE {
                """
                sub_queries = []
                for pid in prop_id.split(','):
                    sub_query = """{
                        wd:%s p:%s ?prop . 
                        ?prop ps:%s ?val .
                        OPTIONAL {
                            ?prop psv:%s ?propVal .
                            ?propVal rdf:type ?type .
                        }
                    }""" % (subject_id, pid, pid, pid) 
                    sub_queries.append(sub_query)
                query += ' UNION '.join(sub_queries)
                query += """
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} 
                }
                """
        
                result =  self._query_wdsparql(query)
                print(result)
                bindings = dget(result, 'results.bindings')
                
                if bindings == [] and prop_id == 'P20':
                    return WikiDataAnswer(None, None, data='yes')
        
                elif (bindings and prop_id == 'P20'):
                    return WikiDataAnswer(None, None, data='no')
                
                answer.sparql_query = query
                answer.bindings = bindings
                answer.data = WikiDataAnswer.get_data(bindings)
            else:
                answer.feedback['property_not_exist'] = "The subject does not have the property : " + prop.upper() 
        
        return answer
    
    def _is_property_of_subj(self, subj_id, prop_id) :
        """Determine if the subject has the property"""
        query = "ASK {wd:%s p:%s ?o}" %(subj_id,prop_id)
        
        #{'head': {}, 'boolean': False}
        result = self._query_wdsparql(query)
      
        isPropOfSubj = result['boolean']
        
        return isPropOfSubj

    def _get_all_property_of_subj(self, subj_id):
        """Get all property of an entity"""
        query = """SELECT DISTINCT ?wdLabel WHERE {
                  wd:%s ?p ?statement .
                  ?wd wikibase:claim ?p.
                  
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
                } ORDER BY ?wdLabel""" % subj_id
        
        result = self._query_wdsparql(query)
        print(result)
        bindings = dget(result, 'results.bindings')
        #on ne garde que les proprietes qui ne contiennent pas "ID" car pas très utiles
        allproperty = []
        for b in bindings :
            wdLabel = dget(b,"wdLabel") 
            value = dget(wdLabel,"value")
            if "ID" not in value :
                allproperty.append(value)
        
        return allproperty

    def _get_aliases(self, subject):
        """Get all aliases of an entity"""
        #self.debug('Get alias {0}'.format(subject))

        subject_id = self._get_id(subject, 'item')
        query = """
        SELECT ?valLabel
        WHERE {
            { wd:%s skos:altLabel ?val FILTER (LANG (?val) = "en") }
            UNION
            { wd:%s rdfs:label ?val FILTER (LANG (?val) = "en") }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} 
        }""" % (subject_id, subject_id)

        result =  self._query_wdsparql(query)
        bindings = dget(result, 'results.bindings')
        return WikiDataAnswer(sparql_query=query, bindings=bindings)

    def _find_entity(self, qtype, inst, params):
        """Count number of things instance/subclass of inst with props"""
        #self.info('Get instances of {0} that are {1}'.format(inst, params))
        print("GET ENTITY")

        inst_id,sugg = self._get_id(inst)

        if not inst_id:
            noAnswer = WikiDataAnswer("")
            noAnswer.feedback["subject"] = "I don't find the subject : "+ inst
            return noAnswer

        if qtype == 'how many':
            select = '(count(*) as ?count)'
        elif qtype in ['which', 'who']:
            select = '?valLabel'
        else:
            self.warn('Qtype {0} not known'.format(qtype))
            return None

        query = """
                SELECT %s
                WHERE {
                { ?val p:P39 ?pos . # position held
                    ?pos ps:P39 wd:%s . # pos = inst
                    ?val wdt:P31 wd:Q5 . # as a human
                } UNION 
                {
                  ?val wdt:P31 wd:%s . # instance of 
                }
                """ % (select, inst_id, inst_id)

        for prop, prop_val, op in params:
            if op in ['>', '<']:
                prop_id,sugg = self._get_id(prop, 'property')
                self.info('Count number of {0} where {1} {2} {3}'.format(
                    inst, prop_id, op, prop_val))
                query += """
                        ?val wdt:%s ?value FILTER(?value %s %s) . # Filter by value
                        """ % (prop_id, op, prop_val)
            elif op in ['in', 'by', 'of', 'from']:
                if op == 'in' and prop_val.isdigit():
                    iso_time = parse(prop_val).isoformat()

                    query += """
                    ?pos pq:P580 ?startDate . # pos.startDate
                    ?pos pq:P582 ?endDate . # pos.endDate
                    FILTER (?startDate < "%s"^^xsd:dateTime && ?endDate > "%s"^^xsd:dateTime)
                    """ % (iso_time, iso_time)
                elif op == 'of' and prop_val:
                    prop_val_id,sugg = self._get_id(prop_val)

                    query += """
                    ?pos pq:P108 wd:%s . # pos.employer
                    """ % (prop_val_id)
                else:
                    # Get value entity
                    prop_val_id,sugg = self._get_id(prop_val)

                    if prop:
                        # Get property id
                        if prop in ['died', 'killed'] and op in ['from', 'by', 'of']:
                            # slight hack because lookup for died defaults to place of death
                            # cause of death
                            prop_id = 'P509'
                        else:
                            prop_id,sugg = self._get_id(prop, 'property')
                        query += '?val wdt:%s wd:%s .\n' % (prop_id, prop_val_id)
                    else:
                        # Infer property from value (e.g. How many countries are in China?)
                        # e.g. infer: How many countries with continent China?
                        prop_id = '*'
                        query += """
                                 wd:%s wdt:P31 ?instance . # Get entities that value is an instance of. Ex: ?instance = wd:Q5107 (continent)
                                 ?instance wdt:P1687 ?propEntity . # instance of Entity to property. Ex: ?propEntity = wd:P30 (continent)
                                 ?propEntity wikibase:directClaim ?prop . # wd to wdt. Ex: ?prop = wdt:P30 (continent)
                                 ?val ?prop wd:%s .
                                 """ % (prop_val_id, prop_val_id)
                    self.info('Count number of {0} where {1}={2}'.format(
                        inst, prop_id, prop_val_id))

        query += 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} }'
        result = {
            'sparql_query': query,
        }

        try:
            data = self._query_wdsparql(query)
        except ValueError:
            self.error('Error parsing data')
            return WikiDataAnswer(**result)

        if qtype == 'how many':
            result['data'] = dget(data, 'results.bindings.0.count.value')
        elif qtype in ['which', 'who']:
            result['bindings'] = dget(data, 'results.bindings')
            
        return WikiDataAnswer(**result)



    def get_property(self, qtype, subject, prop):
        """Gets property of subject from Wikidata

        Args:
            qtype: Type of question (which, how many)
            subject: Name of entity to get property of
            prop: Property to get of subject

        Returns:
            WikiDataAnswer: Answer from result
        """

        prop_id = None

        if prop is None:
            return self._get_desc(subject)

        if prop == 'age':
            bday_ans = self._get_property(subject, 'date of birth', 'P569')
            #le resultat est conservé dans la clé 'plain' du dict
            if bday_ans.to_dict()['plain'] == 'None':
                return None
            birthday = bday_ans.data[0]
            # datetime is a subclass of date. So both must be datetime type
            years = relativedelta(datetime.now(), birthday).years
            bday_ans.data = years
            return bday_ans

        if prop == 'born':
            if qtype == 'where':
                prop_id = 'P19'
            elif qtype == 'when':
                prop_id = 'P569'

        if prop == 'height':
            prop_id = 'P2044,P2048'

        if prop == 'alive':
            prop_id = 'P20'

        if prop in ['nickname', 'known as', 'alias', 'called']:
            return self._get_aliases(subject)

        return self._get_property(subject, prop, prop_id=prop_id)


    def find_entity(self, qtype, inst, props):
        """Count number of things instance/subclass of inst with prop = prop_val

        Args:
            qtype: Type of question (which, how many)
            inst: Instances of object we are querying
            params: Array of property-value-operator tuples to query
                [(property, value, op)]
                property - property to match value
                value - value that property should be
                op - One of  '=', '<' or '>'
                If property is None, then property will be inferred by instance of value

        Returns:
            WikiDataAnswer: Answer from result
        """
        if inst.lower() in ['the president', 'president', 'the prime minister', 'prime minister']:
            for index, tup in enumerate(props):
                prop, prop_val, op = tup
                if op == 'of':
                    inst = '{0} {1} {2}'.format(inst, op, prop_val)
                    props.pop(index)

        ans = self._find_entity(qtype, inst, props)

        return ans
    
    def _get_id_for_yes_no(self, name, _type='item'):
        """Get WikiData ID of a name"""
        item = self._search_entity(name, _type)
        print("itemmmmmmmmmm : ",item)
        return dget(item, 'search.0.id')
    
    def yes_no_get_property(self, subject, subject2=None, prop=None):
        
        prop_id = None
        
        if prop == 'alive':
            prop_id = 'P20'
            
        if prop == 'taller':
            prop_id = 'P2048'
            
        print("dejkdjfe : ",prop_id)    
        print("sub : ",subject)
        print("sub2 : ",subject2)
        
        return self._yes_no_get_property(subject, subject2, prop, prop_id=prop_id)
    
    def _yes_no_get_property(self, subject, subject2=None, prop=None, prop_id=None):
        
        print("je sios dans _yes_no_getçproperty")
        
        """Queries Wikidata to get property"""
        self.debug('{0}, {1}', subject, prop)
        
        subject_id = self._get_id_for_yes_no(subject, 'item')
        subject2_id = self._get_id_for_yes_no(subject2, 'item')
        
        print("this is the subj id 1 : ",subject_id)
        
        print("this is the subj id 2 : ",subject2_id)
        
        if not prop_id:
            prop_id = self._get_id_for_yes_no(prop, 'property')

        print("from get_property, subject id : ",subject_id)
        print("from get_property, subject id2 : ",subject2_id)
        print("from get_property pro id : ", prop_id)

        # test predicat 'place of death'
        if prop_id == 'P20':
            
            my_query = """
                ASK { wd:%s p:%s ?prop }""" % (subject_id,prop_id)
                
            result_query = self._query_wdsparql(my_query)
        
            return WikiDataAnswer(sparql_query=my_query, data = not(result_query['boolean']))
        
        if prop_id == None:
            
            my_query = """
                ASK { wd:%s ?p wd:%s}""" % (subject_id,subject2_id)
        
            result_query = self._query_wdsparql(my_query)
        
            return WikiDataAnswer(sparql_query=my_query, data = result_query['boolean'])
        
        if prop == 'developed':
            
            query = """
                SELECT ?valLabel ?type
                WHERE {
                """
            sub_queries = []
            for pid in prop_id.split(','):
                sub_query = """{
                    wd:%s p:%s ?prop . 
                    ?prop ps:%s ?val .
                    OPTIONAL {
                        ?prop psv:%s ?propVal .
                        ?propVal rdf:type ?type .
                    }
                }""" % (subject_id, pid, pid, pid) 
                sub_queries.append(sub_query)
            query += ' UNION '.join(sub_queries)
            query += """
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} 
            }
            """

            result =  self._query_wdsparql(query)
            bindings = dget(result, 'results.bindings')
            
            for i in range(len(bindings)):
                for key, item in bindings[i].items():
                    if bindings[i][key]['value'].lower() == subject2:
                        return WikiDataAnswer(None, None, data='yes')

            return WikiDataAnswer(None, None, data='no')
        
        
        return WikiDataAnswer(sparql_query=query, bindings=bindings)