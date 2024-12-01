from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import joblib
from rasa_sdk import Tracker
from typing import Any, Text, Dict, List

# Load your spam detection model
spam_model = joblib.load("spam_model.pkl")

class ActionSpamDetection(Action):
    def name(self):
        return "action_spam_detection"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        # Preprocess the user message and predict using the model
        prediction = spam_model.predict([user_message])
        if prediction == "spam":
            dispatcher.utter_message(text="This message looks suspicious. It's marked as spam.")
            return [SlotSet("spam_or_ham", "spam")]
        else:
            dispatcher.utter_message(text="This message seems to be safe. It's marked as ham.")
            return [SlotSet("spam_or_ham", "ham")]


# Loan eligibility action
class ActionLoanEligibility(Action):
    def name(self):
        return "action_loan_eligibility"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        gender = tracker.get_slot('gender')
        salary = tracker.get_slot('salary')
        age = tracker.get_slot('age')
        credit_score = tracker.get_slot('credit_score')
        loan_amount = tracker.get_slot('loan_amount')

        # Loan eligibility logic (simplified)
        if salary > 30000 and credit_score > 650:
            dispatcher.utter_message(text="You are eligible for a loan.")
        else:
            dispatcher.utter_message(text="Sorry, you are not eligible for a loan.")
        return []
class ActionSayData(Action):

    def name(self) -> Text:
        return "action_say_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve slots
        name = tracker.get_slot("name")
        mobile = tracker.get_slot("mobile")
        gender = tracker.get_slot("gender")
        married = tracker.get_slot("married")
        dependents = tracker.get_slot("dependents")
        education = tracker.get_slot("education")  # Fixed typo: "educations" -> "education"
        self_employed = tracker.get_slot("self_employed")
        property_area = tracker.get_slot("property_area")  # Fixed typo: "property_value" -> "property_area"

        # Create a response message
        response = (
            f"Here is the information you provided:\n"
            f"Name: {name}\n"
            f"Mobile: {mobile}\n"
            f"Gender: {gender}\n"
            f"Married: {married}\n"
            f"Dependents: {dependents}\n"
            f"Education: {education}\n"
            f"Self-Employed: {self_employed}\n"
            f"Property Area: {property_area}"
        )

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []