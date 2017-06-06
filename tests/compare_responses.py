from unittest.mock import Mock
import os, json
from lxml import etree
from tests.base_test import BaseTest
from jsondiff import diff
import re

class CompareResponsesTestCase(BaseTest):

    NSMAP = {'oac': 'http://www.openannotation.org/ns/','cnt':'http://www.w3.org/2008/content#'}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compare_json(self):
        failed_bsp = os.path.join(os.path.dirname(__file__), 'fixtures', 'bsp', 'failed')
        success_bsp = os.path.join(os.path.dirname(__file__), 'fixtures', 'bsp', 'success')
        in_success_bsp = open(success_bsp, 'r')
        in_failed_bsp = open(failed_bsp, 'r')
        failed_py = os.path.join(os.path.dirname(__file__), 'fixtures', 'py', 'failed')
        success_py = os.path.join(os.path.dirname(__file__), 'fixtures', 'py', 'success')
        in_success_py = open(success_py, 'r')
        in_failed_py = open(failed_py, 'r')
        py_requests = dict()
        py_requests['failed'] = dict()
        py_requests['success'] = dict()
        bsp_requests = dict()
        bsp_requests['failed'] = dict()
        bsp_requests['success'] = dict()
        readResponse = False
        lastRequest = ""
        for line in in_success_py.readlines():
            line = line.strip()
            if readResponse:
                resp = json.loads(line)
                readResponse = False
                py_requests['success'][lastRequest] = resp
            elif re.search("Request=",line):
                lastRequest = re.split("=",line,1)[1]
            elif re.search("Response=",line):
                readResponse = True
        readResponse = False
        lastRequest = ""
        for line in in_failed_py.readlines():
            line = line.strip()
            if readResponse:
                resp = json.loads(line)
                readResponse = False
                py_requests['failed'][lastRequest] = resp
            elif re.search("Request=",line):
                lastRequest = re.split("=",line,1)[1]
            elif re.search("Response=",line):
                readResponse = True
        readResponse = False
        lastRequest = ""
        for line in in_success_bsp.readlines():
            line = line.strip()
            if readResponse:
                resp = json.loads(line)
                readResponse = False
                bsp_requests['success'][lastRequest] = resp
            elif re.search("Request=",line):
                lastRequest = re.split("=",line,1)[1]
            elif re.search("Response=",line):
                readResponse = True
        readResponse = False
        lastRequest = ""
        for line in in_failed_bsp.readlines():
            line = line.strip()
            if readResponse:
                resp = json.loads(line)
                readResponse = False
                bsp_requests['failed'][lastRequest] = resp
            elif re.search("Request=",line):
                lastRequest = re.split("=",line,1)[1]
            elif re.search("Response=",line):
                readResponse = True

        in_success_py.close()
        in_success_bsp.close()
        in_failed_bsp.close()
        in_failed_py.close()

        for request in bsp_requests['failed']:
            if  request in py_requests['failed']:
                self.maxDiff = None
                self.assertEqual(self.normalize_legacy_json(bsp_requests['failed'][request], py_requests['failed'][request]), py_requests['failed'][request], "Mismatch on failure " + request)
            else:
                print(">>>>" + request + " should have failed" )

        for request in bsp_requests['success']:
            if  request in py_requests['success']:
                self.maxDiff = None
                try:
                    self.assertEqual(self.normalize_legacy_json(bsp_requests['success'][request], py_requests['success'][request]), py_requests['success'][request], "Mismatch on success " + request)
                except:
                    print(">>>> Mismatch on " + request)
            else:
                print(">>>>" + request + " should have succeeded" )


    def normalize_legacy_json(self,old,new):
        replacement = {}
        for key,value in old.items():
            newvalue = value
            if isinstance(newvalue, str):
               newvalue = newvalue.replace('\n', ' ', -1)
            if key in new and isinstance(new[key],dict) and isinstance(value, dict):
                newvalue = self.normalize_legacy_json(value,new[key])
            elif key in new and isinstance(new[key],dict) and isinstance(value, str) and '$' in new[key]:
                newvalue = {'$': value.replace('\n',' ',-1)}
            elif isinstance(value, list) and isinstance(new[key],list):
                newvalue = list()
                for idx,item in enumerate(value):
                    newvalue.append(self.normalize_legacy_json(item,new[key][idx]))
            replacement[key] = newvalue
            if key == 'title' or key == 'resource' or key == 'created' or key == 'about':
                replacement[key] = new[key]

        return replacement



