# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests
import logging
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)


class ActionGreeter(Action):
    def name(self) -> Text:
        return "action_greeter"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Добрый день!")
        return []


class ChuckFact(Action):
    def name(self) -> Text:
        return 'action_chuck_fact'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url=url)
        chuck_joke = response.json()['value']
        logger.debug("The fun joke was recieved! {}".format(response.json()))

        dispatcher.utter_message(
            "Я знаю кое-то про Чака: {}".format(chuck_joke))
        return []


class FormBeer(FormAction):
    def name(self):
        return "beer_form"

    @staticmethod
    def required_slots(tracker):
        return ["is_organic", "has_label", "style_id"]

    def submit(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Органическое пиво: {0}, с этикеткой: {1}, тип: {2}".format(
            tracker.get_slot('is_organic'),
            tracker.get_slot('has_label'),
            tracker.get_slot('style_id')))
        return []
    
    def slot_mappings(self):
        return {
            "is_organic": [
                self.from_entity("is_organic"),
                # self.from_intent(intent="affirm", value=True),
                # self.from_intent(intent="deny", value=False)
                ],
            "has_label": [
                self.from_entity("has_label"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "style_id": [
                self.from_entity("style_id"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ]
        }
