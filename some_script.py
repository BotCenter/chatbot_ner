from __future__ import print_function
import datetime
from time import sleep

from ner_v1.chatbot.tag_message import run_ner

sleep(30)

entities = ['dish', 'footwear', 'month_list', 'brand', 'budget', 'ciudades_chile', 'nombre_mujer', 'locality', 'day_list', 'restaurant', 'clothes', 'nombre_hombre', 'shopping_size', 'cuisine', 'movie', 'date']
message = 'hola que onda en stgo'

print('Starting script random')
start_time = datetime.datetime.now()
output = run_ner(entities=entities, message=message)
end_time = datetime.datetime.now()
delta_time = end_time - start_time
print('Delta time ' + str(delta_time))
print('Finished %s : %s ' % (message, output))
print(str(output))
