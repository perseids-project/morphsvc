from unittest.mock import Mock
from morphsvc.lib.engines.MorpheusLocalEngine import MorpheusLocalEngine
import os, json
from lxml import etree
from tests.base_test import BaseTest
from jsondiff import diff

class AlpheiosRemoteTestCase(BaseTest):

    NSMAP = {'oac': 'http://www.openannotation.org/ns/','cnt':'http://www.w3.org/2008/content#'}

    def setUp(self):
        super(AlpheiosRemoteTestCase, self).setUp()
        self.fixture = os.path.join(os.path.dirname(__file__), 'fixtures','morpheusgrc.xml')
        with open(self.fixture, 'r') as (stream):
            self.data = stream.read()
        self.lexfix = os.path.join(os.path.dirname(__file__), 'fixtures','lexentitygrc.xml')
        with open(self.lexfix, 'r') as (stream):
            self.lexdata = stream.read()
        with open(os.path.join(os.path.dirname(__file__), 'fixtures','morpheusgrc.json'),'r') as stream:
            self.jsondata = json.loads(stream.read(),encoding="UTF-8")
        MorpheusLocalEngine._execute_query = Mock(return_value=self.data)
        MorpheusLocalEngine._execute_lexical_query = Mock(return_value=self.lexdata)

    def tearDown(self):
        super(AlpheiosRemoteTestCase, self).tearDown()

    def test_word_grc_xml(self):
        rv = self.client.get('/analysis/word?word=Μοῦσα&lang=grc&engine=morpheusgrc')
        root = etree.fromstring(rv.data)
        annotation = root.xpath("//oac:Annotation", namespaces=self.NSMAP)
        self.assertEqual(1,len(annotation),"We should have 1 oac:Annotation")
        body = root.xpath("//oac:Annotation/oac:Body", namespaces=self.NSMAP)
        self.assertEqual(2,len(body),"We should have 2 oac:Body")
        uri = root.xpath("//oac:Annotation/oac:Body/cnt:rest/entry", namespaces=self.NSMAP)
        self.assertEqual('http://data.perseus.org/collections/urn:cite:perseus:grclexent.dummy123.1',uri[0].attrib['uri'],"Lexical Entities URI should be present")
        hdwd = root.xpath("//oac:Annotation/oac:Body/cnt:rest/entry/dict/hdwd", namespaces=self.NSMAP)
        self.assertEqual('Μοῦσα',hdwd[0].text,"We should have unicode headwords")
        self.assertEqual('Μοῦσαι',hdwd[1].text,"We should have unicode headwords")

    def test_word_grc_json(self):
        rv = self.client.get('/analysis/word?word=Μοῦσα&lang=grc&engine=morpheusgrc',headers={'Accept':'application/json'})
        dict = json.loads(rv.get_data(as_text=True))
        self.maxDiff = None
        self.assertEqual(self.jsondata['RDF']['Annotation']['about'],dict['RDF']['Annotation']['about'])
        self.assertEqual(self.jsondata['RDF']['Annotation']['hasTarget'],dict['RDF']['Annotation']['hasTarget'])
        self.assertEqual(self.jsondata['RDF']['Annotation']['Body'][0]['rest']['entry'],dict['RDF']['Annotation']['Body'][0]['rest']['entry'])
        self.assertEqual(self.jsondata['RDF']['Annotation']['Body'][1]['rest']['entry'],dict['RDF']['Annotation']['Body'][1]['rest']['entry'])

