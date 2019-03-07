import json
import urllib

import tornado.web
import tornado.ioloop

from unidecode import unidecode

from ner_v1.chatbot.tag_message import run_ner

general_log = tornado.log.gen_log


class NerHandler(tornado.web.RequestHandler):

    async def get_entity_data(self, message, entities):

        entities = ['ciudades_chile', 'restaurant']

        message = urllib.parse.unquote(message)


        output = await run_ner(entities=entities, message=message)
        self.finish(output)

    def get(self):
        message = self.get_argument('message', '')

        if message == '':
            raise tornado.web.HTTPError(400)


        entities = self.get_argument('entities', '')
        if entities != '':
            entities = json.loads(entities)

        return self.get_entity_data(unidecode(message), entities)
