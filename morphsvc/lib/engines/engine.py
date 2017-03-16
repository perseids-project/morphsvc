import json

class Engine():

    def output_json(self,engine_response):
        return json.dumps(engine_response)

    def output_xml(self,engine_response):
        return "<error>" + engine_response + "</error>"

    def supports_language(self,language):
        return False