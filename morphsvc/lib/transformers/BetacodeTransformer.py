import pkg_resources
from lxml import etree
import requests

class BetacodeTransformer:

   def  __init__(self, config, *args,**kwargs):
      resource_package = __name__
      xslt_in_path = '/' .join(('xslt','alpheios-uni2betacode.xsl'))
      xslt_out_path = '/' .join(('xslt','morph-beta2unicode.xsl'))
      xslt_in = pkg_resources.resource_string(resource_package,xslt_in_path)
      xslt_out = pkg_resources.resource_string(resource_package,xslt_out_path)
      self.xslt_in_transformer = etree.XSLT(etree.XML(xslt_in))
      self.xslt_out_transformer = etree.XSLT(etree.XML(xslt_out))
      self.dummy_xml = etree.XML("<dummy>test</dummy>")

   def transform_input(self,input):
      word_param = etree.XSLT.strparam(input)
      transformed = self.xslt_in_transformer(self.dummy_xml,e_in=word_param)
      return str(transformed)


   def transform_output(self,output):
      try:
         output_xml = etree.fromstring(output)
         transformed = self.xslt_out_transformer(output_xml)
      except:
         transformed = etree.fromstring("<words/>")
      return transformed
