# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionWeather(Action):

    def name(self) -> Text:
         return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.19&longitude=-3.61&current_weather=true"

        request = requests.get(url)
        response = request.json()
        temperature = response["current_weather"]["temperature"]

        dispatcher.utter_message(text=f"En Granada hacen {temperature} grados.")

        return []
