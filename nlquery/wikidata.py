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
        self.sparql_desc = {}
        self.suggestions = {'subject' : [], 'prop' : [], "subject1" : [], "subject2" : []}
        self.sparql_query = sparql_query

        if bindings:
            self.bindings = bindings
            self.data = self.get_data(bindings)
        else:
            self.data = data

    def to_dict(self):
        d = super(WikiDataAnswer, self).to_dict()
        d['sparql_query'] = self.sparql_query
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
        print("SEARCH SEARVCH DESC: ",search)
        
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
                answer.suggestions["subject"] = getSuggestions(search)
            else :
                answer.feedback["subject"] = "I didn't find the subject : "+ subject.upper()
                answer.feedback["no_result"] = "but I can give you some suggestions in the tab 'DID YOU MEAN'"
                answer.suggestions["subject"] = getSuggestions(search)
            
        return answer


    def _get_id(self, name, _type='item'):
        """Get WikiData ID of a name"""
   
        idsName = None
        suggestions = []
        
        item = self._search_entity(name, _type)
        #print(_type+"-_get_id_",item)
        
        #tableau correspondant aux resultats de la recherche
        search = dget(item, "search") 
        #print("SEARCH SEARVCH ID: ",search)
        
        #la recherche n'a rien donné
        if len(search) == 0 :
            print("search id empty")

        #la recherche a trouvé quelque chose
        else :
            print("search id full")
            #on verifie qu'il a bien trouvé ce qu'on cherche cad subject
            #text_search == subject
            booleanMatches = confirmMatches(search, name)
            print(booleanMatches)
            #il peut y avoir plusieurs matches donc on renvoie tous les matchs
            if True in booleanMatches:
                #le premier match est retourné
                #au lieu de retourner le premier, on doit verifier que les
                #matchs ont la propriete demandée
                idsName = [dget(item, 'search.%d.id'%i) for i in range(len(booleanMatches)) if booleanMatches[i]]
                print("voici les idsname retournés ... ",idsName)
            suggestions = getSuggestions(search)
                
        return idsName, suggestions


    def _get_property(self, subject, prop, prop_id=None):
        """Queries Wikidata to get property"""
        #print("GET PROPERTY")
        
        answer = WikiDataAnswer(sparql_query=None)
        
        subj_id_found = False
        prop_id_found = False
        prop_id_given = False
        
        list_subject_id, sugg_subj = self._get_id(subject, 'item')
        #on verifie au cas ou prop_id n'est pas definie
        if prop_id :
            prop_id_given = True
        else:
            prop_id_given = False
            list_prop_id, sugg_prop = self._get_id(prop, 'property')
            
        if not list_subject_id :
            answer.feedback["subject"] = "I did not find the subject : "+ subject.upper()
            answer.suggestions["subject"] = sugg_subj
            subj_id_found = False
        else :
            answer.feedback["match_subj"] = "I found "+str(len(list_subject_id))+" result(s) related to the subject : "+ subject.upper()
            answer.suggestions["subject"] = sugg_subj
            subj_id_found = True
        
        if prop_id_given :
           answer.feedback["property"] = "The property is already predefined in the system" 
            
        else :
            if not list_prop_id:
                print("unknown prop")
                answer.feedback["property"] = "I did not find the property : " + prop.upper()
                answer.suggestions["prop"] = sugg_prop
                prop_id_found = False
            else :
                answer.feedback["match_property"] = "I found "+str(len(list_prop_id))+" result(s) related to the property : " + prop.upper()
                answer.suggestions["prop"] = sugg_prop
                prop_id_found = True
            

        if subj_id_found and (prop_id_found or prop_id_given) :
            
            #on a une liste d'ids qui ont matché avec le sujet
            #on doit maintenant les filtrer pour savoir lequel a la prop demandée
            if prop_id_given :
                #simple array
                subjHasProp = [self._is_property_of_subj(s,prop_id) for s in list_subject_id]
            
                if True in subjHasProp :
       
                    subject_id = list_subject_id[subjHasProp.index(True)]
                    
                    answer.sparql_desc[subject_id] = subject
                    answer.sparql_desc[prop_id] = prop
                    
                    answer.feedback["link"] = "I found a link between the subject and the property"
                    
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
            #plusieurs propriété à verifier pour une liste de sujets 
            else :
                #array d'array = chaque arret correspond à une propriete testé sur la liste des subjects
                subjsHaveProps = [[self._is_property_of_subj(s,p) for s in list_subject_id] for p in list_prop_id]
                print("tableau prop sub",subjsHaveProps)
                subject_id, prop_id = self._find_couple_property_of_subj(subjsHaveProps,list_subject_id,list_prop_id)
                
                if subject_id and prop_id :
                    answer.sparql_desc[subject_id] = subject
                    answer.sparql_desc[prop_id] = prop
                    print(subject_id,prop_id)
                    
                    answer.feedback["link"] = "I found a link between the subject and the property"
                    
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
                    #print(result)
                    bindings = dget(result, 'results.bindings')
                    
                    if bindings == [] and prop_id == 'P20':
                        return WikiDataAnswer(None, None, data='yes')
            
                    elif (bindings and prop_id == 'P20'):
                        return WikiDataAnswer(None, None, data='no')
                    
                    answer.sparql_query = query
                    answer.bindings = bindings
                    answer.data = WikiDataAnswer.get_data(bindings)

                else :
                    answer.feedback['no_subjects_with_prop'] = "No couple subject / property was found" 
                
        
        #print("the answer returned : ",answer)
        
        return answer
    
    def _find_couple_property_of_subj(self, subjsprops, list_s, list_prop) :
        
        for p in range(len(subjsprops)) :
            for s in range(len(subjsprops[p])) :
                if subjsprops[p][s] :
                    return list_s[s], list_prop[p]
        
        return None,None
    
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
        #print(result)
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
        
        answer = WikiDataAnswer(sparql_query=None)
        
        subj_id_found = False
        
    
        list_subject_id, suggestion = self._get_id(subject, 'item')
        
        
        if not list_subject_id :
            answer.feedback["subject"] = "I did not find the subject : "+ subject.upper()
            answer.suggestions["subject"] = suggestion
            subj_id_found = False
        else :
            answer.feedback["match_subj"] = "I found "+str(len(list_subject_id))+" result(s) related to the subject : "+ subject.upper()
            answer.suggestions["subject"] = suggestion
            subj_id_found = True
        
        #on ne retient que le premier element de la liste des sujets trouvés
        if subj_id_found :
            
            subject_id = list_subject_id[0]
        
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
            
            answer.bindings = bindings
            answer.data = WikiDataAnswer.get_data(bindings)
            answer.sparql_desc[subject_id] = subject
            answer.sparql_query = query
            
        return answer

    def _find_entity(self, qtype, inst, params):
        """Count number of things instance/subclass of inst with props"""
        
        answer = WikiDataAnswer(sparql_query=None)
        
        inst_id_found = False
        
        list_inst_id, sugg_inst = self._get_id(inst, 'item')
        
        if not list_inst_id :
            answer.feedback["inst"] = "I did not find the instance : "+ inst.upper()
            answer.suggestions["subject"] = sugg_inst
            inst_id_found = False
        else :
            answer.feedback["match_inst"] = "I found "+str(len(list_inst_id))+" result(s) related to the instance : "+ inst.upper()
            answer.suggestions["subject"] = sugg_inst
            inst_id_found = True
            

        if inst_id_found :
            
            if qtype == 'how many':
                select = '(count(*) as ?count)'
            elif qtype in ['which', 'who']:
                select = '?valLabel'
            else:
                answer.feedback["unknown qtype"] = "The type of question is unknown"
                return answer
            
            print("params",params,len(params))
            if len(params) == 0 :
                #pas de propriete dans la question
                #on ne peut pas enlever l'ambiguité s'il y a plusieurs sujets possibles
                #donc on considere le premier d'entre eux
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
                        """ % (select, list_inst_id[0], list_inst_id[0])
                query += 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} }'
                    
            else :      
            
                #on doit chercher le sujet qui possède la propriété (prop)
                #on doit parcourir toutes les propriétés
                
                second_part_query = ""
                count_prop = 1
                list_found_prop = []
                
                
                for prop, prop_val, op in params:
                    
                    prop_id_found = False
                    
                    list_prop_id, sugg_prop = self._get_id(prop, 'property')
                        
                    if list_prop_id : 
                        answer.feedback["match_property"+str(count_prop)] = "I found "+str(len(list_prop_id))+" result(s) related to the property "+str(count_prop)+" : " + prop.upper()
                        answer.suggestions["prop"] += sugg_prop
                        prop_id_found = True
                    else :
                        answer.feedback["property"+str(count_prop)] = "I did not find the property " + str(count_prop)+" : " + prop.upper()
                        answer.suggestions["prop"] += sugg_prop
                        prop_id_found = False
                        
                    if prop_id_found :
                    
                        if op in ['>', '<']:
                            
                            #prop_id,sugg= self._get_id(prop,'property')
                            
                            #array d'array = chaque arret correspond à une propriete testé sur la liste des subjects
                            subjsHaveProps = [[self._is_property_of_subj(s,p) for s in list_inst_id] for p in list_prop_id]
                            print("tableau prop sub",subjsHaveProps)
                            inst_id, prop_id = self._find_couple_property_of_subj(subjsHaveProps,list_inst_id,list_prop_id)
                            
                            if inst_id and prop_id :
                                answer.sparql_desc[inst_id] = inst
                                answer.sparql_desc[prop_id] = prop
                                print(inst_id,prop_id)
                    
                                answer.feedback["link"] = "I found a link between the subject and the property"
                                #self.info('Count number of {0} where {1} {2} {3}'.format(inst, prop_id, op, prop_val))
                            
                                second_part_query += """
                                ?val wdt:%s ?value FILTER(?value %s %s) . # Filter by value
                                """ % (prop_id, op, prop_val)
                            else :
                                answer.feedback["link"] = "I did not find a link between the subject and the property"
                                    
                                    
                        elif op in ['in', 'by', 'of', 'from']:
                            if op == 'in' and prop_val.isdigit():
                                iso_time = parse(prop_val).isoformat()
            
                                second_part_query += """
                                ?pos pq:P580 ?startDate . # pos.startDate
                                ?pos pq:P582 ?endDate . # pos.endDate
                                FILTER (?startDate < "%s"^^xsd:dateTime && ?endDate > "%s"^^xsd:dateTime)
                                """ % (iso_time, iso_time)
                            elif op == 'of' and prop_val:
                                #prop_val_id,sugg = self._get_id(prop_val)
            
                                second_part_query += """
                                ?pos pq:P108 wd:%s . # pos.employer
                                """ % (prop_id)
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
                                    second_part_query += '?val wdt:%s wd:%s .\n' % (prop_id, prop_val_id)
                                else:
                                    # Infer property from value (e.g. How many countries are in China?)
                                    # e.g. infer: How many countries with continent China?
                                    prop_id = '*'
                                    second_part_query += """
                                             wd:%s wdt:P31 ?instance . # Get entities that value is an instance of. Ex: ?instance = wd:Q5107 (continent)
                                             ?instance wdt:P1687 ?propEntity . # instance of Entity to property. Ex: ?propEntity = wd:P30 (continent)
                                             ?propEntity wikibase:directClaim ?prop . # wd to wdt. Ex: ?prop = wdt:P30 (continent)
                                             ?val ?prop wd:%s .
                                             """ % (prop_val_id, prop_val_id)
                                self.info('Count number of {0} where {1}={2}'.format(
                                    inst, prop_id, prop_val_id))
                            
                    count_prop += 1  
                    list_found_prop.append(prop_id_found)
                    #fin boucle for
                    
                    
                    
                    
                if False not in list_found_prop and len(list_found_prop) > 0:
                    #fin boucle for
                    #on regroupe les 2 parties de la requetes
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
                            
                    query += second_part_query
            
            
                    query += 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en"} }'
                        
            answer.sparql_query = query
    
            try:
                data = self._query_wdsparql(query)
            except ValueError:
                self.error('Error parsing data')
                return answer
    
            if qtype == 'how many':
                answer.data = dget(data, 'results.bindings.0.count.value')
            elif qtype in ['which', 'who']:
                bindings = dget(data, 'results.bindings')
                answer.bindings = bindings
                answer.data = WikiDataAnswer.get_data(bindings)
                
        else :
            uyguygyug = 0
            
            
        return answer



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
                return bday_ans
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
            #prop_id = 'P2044,P2048'
            prop_id = 'P2048'

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
    
    # Param prop : property à vérifier s'il est connu ou non
    # Return propIds : liste des ids du prop
    def getKnownProp(self,prop):
        sizeWords = ['taller','higher','lower','shorter','smaller','less','bigger']
        lifeWords = ['alive','dead']
        propIds = []
        if prop in sizeWords:
            propIds.append('P2046')
            propIds.append('P2048')
        if prop in lifeWords:
            propIds.append('P20')
        return propIds
    
    # Param name : nom auquel on veut récupérer les ids
    # Return ids : liste des ids du name
    def getIds(self, name, searchType):
        ids = []
        item = self._search_entity(name,_type=searchType)
        search = dget(item,"search")
        for i in search:
            ids.append(i['id'])
        return ids
    
    # Param subject1 : premier sujet en langage naturel
    # Param subject2 : deuxieme sujet en langage naturel
    # Param prop : propriete en langage naturel
    def getAnswer(self,subject1,subject2=None,prop=None):
        
        """
            Dans un premier temps on récupère les ids des paramètres
        """
        
        answer = WikiDataAnswer(sparql_query=None)
        #answer.feedback["type_question"] = "This is a question of the type : Yes/No"
        
        subj1_id_found = False
        subj2_id_found = False
        subj2_given = False
        
        prop_id_found = False
        prop_given = False
        prop_known = True
        
        # retrieving ids of subject1
        #subj1Ids = self.getIds(subject1,"item")
        
        #subj1Ids : seulement les ids qui matchent a 100% avec le subj1
        subj1Ids, suggestions_s1 = self._get_id(subject1, "item")
        
        
        
        if subject2 != None:
            # retrieving ids of subject2
            #subj2Ids = self.getIds(subject2,"item")
            subj2_given = True
            subj2Ids, suggestions_s2 = self._get_id(subject2, "item")
            
        if prop != None:
            prop_given = True
            propIds = self.getKnownProp(prop)
            # if the prop is unknown 
            if len(propIds) == 0:
                prop_known = False
                # retrieving ids of prop
                #propIds = self.getIds(prop,"property")
                propIds, suggestions_prop = self._get_id(prop, "property")
                
                
        if not subj1Ids :
            answer.feedback["subject1"] = "I did not find the 1st subject : "+ subject1.upper()
            answer.suggestions["subject1"] = suggestions_s1
            subj1_id_found = False
        else :
            answer.feedback["match_subj1"] = "I found "+str(len(subj1Ids))+" result(s) related to the 1st subject : "+ subject1.upper()
            answer.suggestions["subject1"] = suggestions_s1
            subj1_id_found = True
        
        if subj2_given :
            if not subj2Ids :
                answer.feedback["subject2"] = "I did not find the 2nd subject : "+ subject2.upper()
                answer.suggestions["subject2"] = suggestions_s2
                subj2_id_found = False
            else :
                answer.feedback["match_subj2"] = "I found "+str(len(subj2Ids))+" result(s) related to the 2nd subject : "+ subject2.upper()
                answer.suggestions["subject2"] = suggestions_s2
                subj2_id_found = True
        #else :
        #    answer.feedback["subject2"] = "There is not subject 2 "

            
        
        if prop_given :    
            if not propIds :
                answer.feedback["property"] = "I did not find the property : " + prop.upper()
                answer.suggestions["prop"] = suggestions_prop
                prop_id_found = False
            else :
                answer.feedback["property"] = "I found "+str(len(propIds))+" result(s) related to the property : " + prop.upper()
                if not prop_known :
                    answer.suggestions["prop"] = suggestions_prop
                prop_id_found = True
                
        else :
            answer.feedback["property"] = "There is not property defined"
        

        """
            Formulation de la requête SPARQL
        """
        if prop == None:
            print("s1 : ",subj1Ids)
            print("s2 : ",subj2Ids)
            # cas subject1 - subject2
            if len(subj1Ids) > 0 and len(subj2Ids) > 0:
                for idS1 in subj1Ids:
                    for idS2 in subj2Ids:
                        query = """
                        ASK { 
                                { wd:%s ?p wd:%s } 
                                UNION 
                                { wd:%s ?p2 wd:%s } 
                        } """ % (idS1,idS2,idS2,idS1)
        
                        result =  self._query_wdsparql(query)
                        answer.sparql_query = query
                        
                        if result['boolean'] == True:
                            answer.sparql_desc[idS1] = subject1
                            answer.sparql_desc[idS2] = subject2
                            answer.data = 'Yes'
                            
                            return answer
                        
                        else:
                            answer.sparql_desc[idS1] = subject1
                            answer.sparql_desc[idS2] = subject2
                            
                            answer.data = 'No'
                            
                            return answer
            
        else:
            # cas subject - prop
            if len(subj1Ids) > 0 and subject2==None:
                for idS in subj1Ids:
                    for idP in propIds:
                        my_query = """
                        ASK { 
                                wd:%s p:%s ?prop 
                        }""" % (idS,idP)
                        
                        result = self._query_wdsparql(my_query)
                        answer.sparql_query = my_query
                        print("aa ",idS,idP)
                        
                        if result['boolean'] == True:
                            answer.sparql_desc[idS] = subject1
                            
                            if prop == 'alive':
                                answer.sparql_desc[idP] = "place of death"
                                answer.data = "No"
                                return answer
                            
                            elif prop == 'dead':
                                answer.sparql_desc[idP] = "place of death"
                                answer.data = "Yes"
                                return answer
                            
                            else:
                                answer.sparql_desc[idP] = prop
                                answer.data = "Yes"
                                return answer
                        else:
                            answer.sparql_desc[idS] = subject1

                            if prop == 'dead':
                                answer.sparql_desc[idP] = "place of death"
                                answer.data = "No"
                                return answer
                            
                            elif prop == 'alive':
                                answer.sparql_desc[idP] = "place of death"
                                answer.data = "Yes"
                                return answer
                            
                            else:
                                answer.sparql_desc[idP] = prop
                                answer.data = "No"
                                return answer
                            
                            
            # cas comparatif : subject1 - prop - subject2
            elif len(subj1Ids) > 0 and len(subj2Ids) > 0 and prop in ['taller','higher','lower','shorter','smaller','less','bigger']:
                #self.getAnswerCompareS1S2P(subj1Ids,subj2Ids,propIds,prop)
                # pour éviter les problèmes d'indices
                liste = [len(subj1Ids),len(subj2Ids)]
                ite = sorted(liste)[0]
                for i in range(len(propIds)):
                    for j in range(ite):
                        left_retrieve = """
                            SELECT ?val
                            WHERE {
                                wd:%s wdt:%s ?val
                            }
                            """ % (subj1Ids[j],propIds[i])
                                
                        result_left_query = self._query_wdsparql(left_retrieve)
                                
                        #print("voiici le res left retri : ",result_left_query['results']['bindings'][0]['val']['value'])
                                
                        right_retrieve = """
                        SELECT ?val
                        WHERE {
                            wd:%s wdt:%s ?val
                        }
                        """ % (subj2Ids[j],propIds[i]) 
                        
                        result_right_query = self._query_wdsparql(right_retrieve)
                        
                        print("---------------------------")
                        print(result_left_query)
                        print(result_right_query)
                        if len(result_left_query['results']['bindings']) != 0 and len(result_right_query['results']['bindings']) != 0:
                            if (float(result_left_query['results']['bindings'][0]['val']['value']) > float(result_right_query['results']['bindings'][0]['val']['value'])):
                                print(float(result_left_query['results']['bindings'][0]['val']['value']))
                                print(float(result_right_query['results']['bindings'][0]['val']['value']))
                                if (prop in ['taller','higher','lower','shorter','smaller','less','bigger']):
                                    print("je dois etre la")
                                    return WikiDataAnswer(None, None, data='Yes')
                                
                                else:
                                    return WikiDataAnswer(None, None, data='No')
                            else:
                                if (prop in ['taller','higher','lower','shorter','smaller','less','bigger']):
                                    return WikiDataAnswer(None, None, data='No')
                                    
                                else:
                                    return WikiDataAnswer(None, None, data='Yes')
            else:
                for idS1 in subject1:
                    for idP in prop:
                        for idS2 in subject2:
                            query = """
                                ASK { { wd:%s p:%s wd:%s } UNION { wd:%s p:%s wd:%s } } """ % (idS1,idP,idS2,idS2,idP,idS1)
                            result = self._query_wdsparql(query)
                            print(result)
                            if len(result) > 0:
                                if result['boolean'] == True:
                                    return WikiDataAnswer(None, None, data='Yes')
                                else:
                                    return WikiDataAnswer(None, None, data='No')
                                
    def getAnswerOrder(self,subject1,prop=None,subject2=None):
        """
            Dans un premier temps on récupère les ids des paramètres
        """
        #self._get_property(subject1,prop)
        subj1Ids = None
        subj2Ids = None
        propIds = None

        
        answer = WikiDataAnswer(sparql_query=None)
        
        subj1_id_found = False
        subj2_id_found = False
        subj1_given = False
        subj2_given = False
        
        prop_id_found = False
        prop_given = False
        prop_known = True
        
        
        if subject1 != None:
            #subj1Ids : seulement les ids qui matchent a 100% avec le subj1
            subj1_given = True
            subj1Ids, suggestions_s1 = self._get_id(subject1, "item")

        if subject2 != None:
            # retrieving ids of subject2
            #subj2Ids = self.getIds(subject2,"item")
            subj2_given = True
            subj2Ids, suggestions_s2 = self._get_id(subject2, "item")
            
        if prop != None:
            prop_given = True
            propIds = self.getKnownProp(prop)
            # if the prop is unknown 
            if len(propIds) == 0:
                prop_known = False
                # retrieving ids of prop
                #propIds = self.getIds(prop,"property")
                propIds, suggestions_prop = self._get_id(prop, "property")
                
        if subj1_given :        
            if not subj1Ids :
                answer.feedback["subject1"] = "I did not find the 1st subject : "+ subject1.upper()
                answer.suggestions["subject1"] = suggestions_s1
                subj1_id_found = False
            else :
                answer.feedback["match_subj1"] = "I found "+str(len(subj1Ids))+" result(s) related to the 1st subject : "+ subject1.upper()
                answer.suggestions["subject1"] = suggestions_s1
                subj1_id_found = True
        
        if subj2_given :
            if not subj2Ids :
                answer.feedback["subject2"] = "I did not find the 2nd subject : "+ subject2.upper()
                answer.suggestions["subject2"] = suggestions_s2
                subj2_id_found = False
            else :
                answer.feedback["match_subj2"] = "I found "+str(len(subj2Ids))+" result(s) related to the 2nd subject : "+ subject2.upper()
                answer.suggestions["subject2"] = suggestions_s2
                subj2_id_found = True
        #else :
        #    answer.feedback["subject2"] = "There is not subject 2 "

            
        
        if prop_given :    
            if not propIds :
                answer.feedback["property"] = "I did not find the property : " + prop.upper()
                answer.suggestions["prop"] = suggestions_prop
                prop_id_found = False
            else :
                answer.feedback["property"] = "I found "+str(len(propIds))+" result(s) related to the property : " + prop.upper()
                if not prop_known :
                    answer.suggestions["prop"] = suggestions_prop
                prop_id_found = True
                
        else :
            answer.feedback["property"] = "There is not property defined"
        
                
        """
            Requête SPARQL + réponse retournée
        """
        
        print("S1 id : ",subj1Ids)
        print("S2 id : ",subj2Ids)
        print("P id : ",propIds)
        
        # cas subject - prop
        # ex : give me the capital of France
        if subj1_id_found and subj2Ids == None and prop_id_found :
            for idS in subj1Ids:
                for idP in propIds:
                    query = """
                        SELECT ?val ?valLabel
                        WHERE  {
                            wd:%s wdt:%s ?val
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en"}
                        }
                        LIMIT 7
                    """ % (idS,idP)
                    
                    result = self._query_wdsparql(query)
                    bindings = dget(result, 'results.bindings')

                    if len(result['results']['bindings']) != 0:
                        answer.bindings = bindings
                        answer.data = WikiDataAnswer.get_data(bindings)
                        answer.sparql_desc[idS] = subject1
                        answer.sparql_desc[idP] = prop
                        answer.sparql_query = query
                        
                        return answer

        elif subj1_id_found and subj2Ids == None and propIds == None:
            for idS in subj1Ids:
                query = """
                        SELECT ?val ?valLabel 
                        WHERE  {
                            ?val ?p wd:%s.
                            ?val rdfs:label ?valLabel.
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en"}
                        }
                        LIMIT 7
                    """ % (idS)
                result = self._query_wdsparql(query)
                bindings = dget(result, 'results.bindings')
                print('ressss : ',result)
                print('bindings : ',bindings)
                if len(result['results']['bindings']) != 0:
                    answer.bindings = bindings
                    answer.data = WikiDataAnswer.get_data(bindings)
                    answer.sparql_desc[idS] = subject1
                    answer.sparql_query = query
                        
                    return answer
                
        elif subj1Ids == None and subj2_id_found and prop_id_found:
            for idS in subj2Ids:
                for idP in propIds:
                    query = """
                        SELECT ?val ?valLabel
                        WHERE  {
                            ?val wdt:%s wd:%s
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en"}
                        }
                        LIMIT 7
                    """ % (idP,idS)
                    result = self._query_wdsparql(query)
                    bindings = dget(result, 'results.bindings')
                    
                    if len(result['results']['bindings']) != 0:
                        answer.bindings = bindings
                        answer.data = WikiDataAnswer.get_data(bindings)
                        answer.sparql_desc[idS] = subject2
                        answer.sparql_desc[idP] = prop
                        answer.sparql_query = query
        else :
            return answer