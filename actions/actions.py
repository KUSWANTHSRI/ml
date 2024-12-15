from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import joblib
from rasa_sdk import Tracker
from typing import Any, Text, Dict, List
import requests

# Load your spam detection model
#spam_model = joblib.load("spam_model.pkl")


class ActionDetectSpam(Action):
    def name(self) -> str:
        return "action_classifier_predict"

    def detect_spam(self, message: str) -> str:
        """Classify a message as spam or not using Hugging Face API."""
        hf_api_key = os.getenv("HF_API_KEY")  # Make sure Hugging Face API key is set in environment variables
        model_url = "https://api-inference.huggingface.co/models/BW7898/spam_message_classification"  # Spam message classification model URL

        headers = {
            "Authorization": f"Bearer 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"
        }

        payload = {
            "inputs": message
        }
        print(payload)
        try:
            # Send the request to the Hugging Face API
            response = requests.post(model_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for invalid responses

            # Extract result from the response
            result = response.json()

            if result:
                    label = response.json()[0][0]["label"]
                    print(response.json())
                    
                        
                  # Extract the classification result from Hugging Face response
                    return f"Message classified as: {label}"  # Either SPAM or NOT_SPAM
            else:
                return "Unable to classify the message."
        except requests.exceptions.RequestException as e:
            return f"Error occurred during spam detection: {e}"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get("text")
        print(user_message)
        
        if not user_message:
            dispatcher.utter_message(text="No message found to classify.")
            return []

        # Detect spam using Hugging Face API
        result = self.detect_spam(user_message)
        dispatcher.utter_message(text=result)
        
        return []


# Loan eligibility action
class ActionLoanEligibility(Action):
    def name(self):
        return "action_loan_eligibility"
    print("i am working ")
    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        gender = tracker.get_slot('gender')
        salary = tracker.get_slot('salary')
        age = tracker.get_slot('age')
        credit_score = tracker.get_slot('credit_score')
        loan_amount = tracker.get_slot('loan_amount')

        # Loan eligibility logic (simplified)
        salary=100000
        credit_score=800
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
import openai
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

class ActionChatGPTFAQ(Action):
    def name(self) -> str:
        return "action_chatgpt_faq"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get("text")
        
        # Check for specific banking queries
        if "open account" in user_message.lower():
            reply = "To open a bank account, visit the nearest branch with ID proof and address proof."
        elif "block my card" in user_message.lower():
            reply = "To block your card, call our customer support or use the mobile app to block your card instantly."
        else:
            # Default response using GPT for other queries
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a banking assistant who answers questions about bank services."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            reply = response['choices'][0]['message']['content'].strip()

        dispatcher.utter_message(text=reply)
        return []
       