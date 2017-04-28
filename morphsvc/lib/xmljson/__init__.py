# -*- coding: utf-8 -*-

import sys
from collections import Counter, OrderedDict
from lxml import etree as et
from lxml.etree import Element

__author__ = 'S Anand'
__email__ = 'root.node@gmail.com'
__version__ = '0.1.7'

# Python 3: define unicode() as str()
if sys.version_info[0] == 3:
    unicode = str
    basestring = str


class XMLData(object):
    def __init__(self, xml_fromstring=True, xml_tostring=True, element=None, dict_type=None,
                 list_type=None, attr_prefix=None, text_content=None, simple_text=False, ignore_ns=False):
        # xml_fromstring == False(y) => '1' -> '1'
        # xml_fromstring == True     => '1' -> 1
        # xml_fromstring == fn       => '1' -> fn(1)
        if callable(xml_fromstring):
            self._fromstring = xml_fromstring
        elif not xml_fromstring:
            self._fromstring = lambda v: v
        # custom conversion function to convert data string to XML string
        if callable(xml_tostring):
            self._tostring = xml_tostring
        # custom etree.Element to use
        self.element = Element if element is None else element
        # dict constructor (e.g. OrderedDict, defaultdict)
        self.dict = OrderedDict if dict_type is None else dict_type
        # list constructor (e.g. UserList)
        self.list = list if list_type is None else list_type
        # Prefix attributes with a string (e.g. '$')
        self.attr_prefix = attr_prefix
        # Key that stores text content (e.g. '$t')
        self.text_content = text_content
        # simple_text == False or None or 0 => '<x>a</x>' = {'x': {'a': {}}}
        # simple_text == True               => '<x>a</x>' = {'x': 'a'}
        self.simple_text = simple_text
        # flag to ignore namespaces on tags
        self.ignore_ns = ignore_ns

    @staticmethod
    def _tostring(value):
        '''Convert value to XML compatible string'''
        if value is True:
            value = 'true'
        elif value is False:
            value = 'false'
        return unicode(value)       # noqa: convert to whatever native unicode repr

    @staticmethod
    def _fromstring(value):
        '''Convert XML string value to None, boolean, int or float'''
        if not value:
            return None
        std_value = value.strip().lower()
        if std_value == 'true':
            return True
        elif std_value == 'false':
            return False
        try:
            return int(std_value)
        except ValueError:
            pass
        try:
            return float(std_value)
        except ValueError:
            pass
        return value

    def etree(self, data, root=None):
        '''Convert data structure into a list of etree.Element'''
        result = self.list() if root is None else root
        if isinstance(data, (self.dict, dict)):
            for key, value in data.items():
                value_is_list = isinstance(value, (self.list, list))
                value_is_dict = isinstance(value, (self.dict, dict))
                # Add attributes and text to result (if root)
                if root is not None:
                    # Handle attribute prefixes (BadgerFish)
                    if self.attr_prefix is not None:
                        if key.startswith(self.attr_prefix):
                            key = key.lstrip(self.attr_prefix)
                            # @xmlns: {$: xxx, svg: yyy} becomes xmlns="xxx" xmlns:svg="yyy"
                            if value_is_dict:
                                raise ValueError('XML namespaces not yet supported')
                            else:
                                result.set(key, self._tostring(value))
                            continue
                    # Handle text content (BadgerFish, GData)
                    if self.text_content is not None:
                        if key == self.text_content:
                            result.text = self._tostring(value)
                            continue
                    # Treat scalars as text content, not children (GData)
                    if self.attr_prefix is None and self.text_content is not None:
                        if not value_is_dict and not value_is_list:
                            result.set(key, self._tostring(value))
                            continue
                # Add other keys as one or more children
                values = value if value_is_list else [value]
                for value in values:
                    elem = self.element(key)
                    result.append(elem)
                    # Treat scalars as text content, not children (Parker)
                    if not isinstance(value, (self.dict, dict, self.list, list)):
                        if self.text_content:
                            value = {self.text_content: value}
                    self.etree(value, root=elem)
        else:
            if self.text_content is None and root is not None:
                root.text = self._tostring(data)
            else:
                result.append(self.element(self._tostring(data)))
        return result

    def data(self, root):
        '''Convert etree.Element into a dictionary'''
        value = self.dict()
        children = [node for node in root if isinstance(node.tag, basestring)]
        for attr, attrval in root.attrib.items():
            if self.ignore_ns:
                tag = et.QName(attr)
                attr = tag.localname
            attr = attr if self.attr_prefix is None else self.attr_prefix + attr
            value[attr] = self._fromstring(attrval)
        if root.text and self.text_content is not None:
            text = root.text.strip()
            if text:
                if self.simple_text and len(children) == len(root.attrib) == 0:
                    value = self._fromstring(text)
                else:
                    value[self.text_content] = self._fromstring(text)
        count = Counter(child.tag for child in children)
        for child in children:
            if count[child.tag] == 1:
                value.update(self.data(child))
            else:
                if self.ignore_ns:
                  tag = et.QName(child.tag)
                  result = value.setdefault(tag.localname, self.list())
                else:
                    result = value.setdefault(child.tag, self.list())
                result += self.data(child).values()
        if (self.ignore_ns):
            tag = et.QName(root)
            return self.dict([(tag.localname, value)])
        else:
            return self.dict([(root.tag, value)])


class Legacy(XMLData):
    '''Converts between XML and data in a manner mostly compatiable with the BSP Morphology Service converter
       mostly the same as BadgerFish excemp that attributes are not prefixed and all namespaces are ignored
       remaining difference is that the legacy algorithm treated text content differently if the element did not
       have any attributes, in which case it made it a flat value rather than an object.
    '''

    def __init__(self, **kwargs):
        super(Legacy, self).__init__(attr_prefix=None, text_content='$', ignore_ns=True, **kwargs)

class BadgerFish(XMLData):
    '''Converts between XML and data using the BadgerFish convention'''
    def __init__(self, **kwargs):
        super(BadgerFish, self).__init__(attr_prefix='@', text_content='$', **kwargs)


class GData(XMLData):
    '''Converts between XML and data using the GData convention'''
    def __init__(self, **kwargs):
        super(GData, self).__init__(text_content='$t', **kwargs)


class Yahoo(XMLData):
    '''Converts between XML and data using the Yahoo convention'''
    def __init__(self, **kwargs):
        kwargs.setdefault('xml_fromstring', False)
        super(Yahoo, self).__init__(text_content='content', simple_text=True, **kwargs)


class Parker(XMLData):
    '''Converts between XML and data using the Parker convention'''
    def __init__(self, **kwargs):
        super(Parker, self).__init__(**kwargs)

    def data(self, root):
        'Convert etree.Element into a dictionary'
        # If no children, just return the text
        children = [node for node in root if isinstance(node.tag, basestring)]
        if len(children) == 0:
            return self._fromstring(root.text)

        # Element names become object properties
        count = Counter(child.tag for child in children)
        result = self.dict()
        for child in children:
            if count[child.tag] == 1:
                if self.ignore_ns:
                    tag = et.QName(child)
                    result[tag.localname] = self.data(child)
                else:
                    result[child.tag] = self.data(child)
            else:
                if self.ignore_ns:
                    tag = et.QName(child)
                    result.setdefault(tag.localname, self.list()).append(self.data(child))
                else:
                    result.setdefault(child.tag, self.list()).append(self.data(child))

        return result

badgerfish = BadgerFish()
gdata = GData()
parker = Parker()
yahoo = Yahoo()
legacy = Legacy()
