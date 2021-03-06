import requests
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from services import ChuckService, BeerService
from deprecated import deprecated


@deprecated
class ActionGreeter(Action):
    """
    Deprecated: use utter_greeting
    Action that can say you 'Good afternoon!' in Russian
    """

    def name(self) -> Text:
        return "action_greeter"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Добрый день!")
        return []


class ChuckFact(Action):
    """
    Action that returning some funny fact aboun Chuck Norris
    """

    def name(self) -> Text:
        return 'action_chuck_fact'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        chuck_joke = ChuckService.get_fact()
        dispatcher.utter_message(
            "Я знаю кое-то про Чака: {}".format(chuck_joke))
        return []


class FormBeer(FormAction):
    """
    Form that take beer params and advise random Beer
    """

    def name(self) -> Text:
        return "beer_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["is_organic", "has_label", "style"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List:
        dispatcher.utter_message("Органическое пиво: {0}, с этикеткой: {1}, тип: {2}".format(
            tracker.get_slot('is_organic'),
            tracker.get_slot('has_label'),
            tracker.get_slot('style')))

        dispatcher.utter_message("Я нашел кое что для тебя!")
        recomended_beer = BeerService.get_random_beer(
            tracker.get_slot('is_organic'),
            tracker.get_slot('has_label'),
            tracker.get_slot('style'))

        dispatcher.utter_message("Название: {0}\nОписание: {1}".format(
            recomended_beer.name, recomended_beer.desc))

        return []

    def slot_mappings(self) -> List[Dict[Text, Any]]:
        return {
            "is_organic": [
                self.from_entity("is_organic")
            ],
            "has_label": [
                self.from_entity("has_label"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "style": [
                self.from_entity("style")
            ]
        }
