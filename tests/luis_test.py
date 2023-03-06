import sys
import pathlib
import pytest
import aiounittest
import asyncio
import json

current = pathlib.Path(__file__).parent.parent
libpath = current.joinpath("/media/katrin/C0D812DCD812D090/Ingenieur_IA/P10_chatbot/bot")
sys.path.append(str(libpath))

from botbuilder.core import (
    TurnContext,
    ConversationState,
    MemoryStorage
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter

from booking_details import BookingDetails
from dialogs import MainDialog, BookingDialog
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent

from config import DefaultConfig



# Test Luis answer to a first message

class LuisTest(aiounittest.AsyncTestCase):

    async def test_luis(self):

        CONFIG = DefaultConfig()
        RECOGNIZER = FlightBookingRecognizer(CONFIG)

        async def run_test(turn_context):
            
            intent, result = await LuisHelper.execute_luis_query(RECOGNIZER, turn_context)

            await turn_context.send_activity(
                json.dumps(
                    {
                        "intent": intent,
                        "booking_details": None if not hasattr(result, "__dict__") else result.__dict__,
                    }
                )
            )

        adapter = TestAdapter(run_test)

        await adapter.test(
            "Hello",
            json.dumps(
                {
                    "intent": Intent.NONE_INTENT.value,
                    "booking_details": None,
                }
            )
        )

        await adapter.test(

            "I want to book a flight from Paris to Berlin",

            json.dumps(
                {
                    "intent": Intent.BOOK_FLIGHT.value,
                    "booking_details": BookingDetails(
                        dst_city="Berlin", or_city="Paris"
                    ).__dict__,
                }
            )
        )