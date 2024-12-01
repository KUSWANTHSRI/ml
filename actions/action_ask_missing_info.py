from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker

class ActionAskMissingInfo(Action):

    def name(self) -> str:
        return "action_ask_missing_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Check if the slot is None, then ask for the required information
        if tracker.get_slot("mobile") is None:
            dispatcher.utter_message(text="Please provide your mobile number.")
            return [SlotSet("mobile", None)]  # This ensures the slot is still None

        elif tracker.get_slot("gender") is None:
            dispatcher.utter_message(text="Please provide your gender.")
            return [SlotSet("gender", None)] 

        elif tracker.get_slot("married") is None:
            dispatcher.utter_message(text="Are you married? Please answer with 'yes' or 'no'.")
            return [SlotSet("married", None)] 

        elif tracker.get_slot("dependents") is None:
            dispatcher.utter_message(text="How many dependents do you have?")
            return [SlotSet("dependents", None)]

        elif tracker.get_slot("education") is None:
            dispatcher.utter_message(text="What is your education level?")
            return [SlotSet("education", None)]

        elif tracker.get_slot("self_employed") is None:
            dispatcher.utter_message(text="Are you self-employed? Please answer with 'yes' or 'no'.")
            return [SlotSet("self_employed", None)]

        elif tracker.get_slot("property_area") is None:
            dispatcher.utter_message(text="What is your property area type?")
            return [SlotSet("property_area", None)]

        # If all slots are filled, you can take further actions or move to the next step
        dispatcher.utter_message(text="Thank you for providing all the details!")
        return []
