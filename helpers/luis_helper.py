# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict, Tuple
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext
from dateparser.search import search_dates
from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    CANCEL = "Cancel"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> Tuple[Intent, object]:
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                
                result = BookingDetails()

                if recognizer_result.entities.get("or_city") is not None:
                    result.or_city = recognizer_result.entities.get("or_city")[0].capitalize()
                else: result.or_city = None                

                if recognizer_result.entities.get("dst_city") is not None:
                    result.dst_city = recognizer_result.entities.get("dst_city")[0].capitalize()
                else: result.dst_city = None

                if recognizer_result.entities.get("budget") is not None:
                    result.budget = recognizer_result.entities.get("budget")[0]
                else: result.budget = None

                if recognizer_result.entities.get("str_date") is not None:
                    if recognizer_result.entities.get("end_date") is None:
                        result.str_date = recognizer_result.entities.get("datetime")[0].get("timex")[0]
                        result.end_date = None
                    elif recognizer_result.entities.get("end_date") is not None:
                        if recognizer_result.entities.get("datetime")[0].get("type") == "daterange":
                            result.str_date = recognizer_result.entities.get("datetime")[0].get('timex')[0].split(',')[0].replace('(','')
                            result.end_date = recognizer_result.entities.get("datetime")[0].get('timex')[0].split(',')[1].replace(')','')
                
                if recognizer_result.entities.get("end_date") is not None:
                    if recognizer_result.entities.get("str_date") is None:
                        if recognizer_result.entities.get("datetime")[0].get("type") == "daterange":
                            result.str_date = recognizer_result.entities.get("datetime")[0].get('timex')[0].split(',')[0].replace('(','')
                            result.end_date = recognizer_result.entities.get("datetime")[0].get('timex')[0].split(',')[1].replace(')','')
                        else:
                            result.end_date = recognizer_result.entities.get("datetime")[0].get("timex")[0]
                            result.str_date = None

                if len(recognizer_result.entities.get("datetime")) > 1:
                    dateone = recognizer_result.entities.get("datetime")[0].get("timex")[0]
                    datetwo = recognizer_result.entities.get("datetime")[1].get("timex")[0]
                    if dateone > datetwo:
                        result.str_date = datetwo
                        result.end_date = dateone
                    else:
                        result.str_date = dateone
                        result.end_date = datetwo
            

        except Exception as exception:
            print(exception)

        return intent, result