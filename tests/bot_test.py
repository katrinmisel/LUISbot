import sys
import os
import json
import aiounittest
import aiohttp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DefaultConfig
from dialogs import BookingDialog, MainDialog
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper

from botbuilder.dialogs.prompts import TextPrompt

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage
)

from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter

CONFIG = DefaultConfig()

# make a HTTP request and assert that response is "<Response [200]>"

class TestEndpoint(aiounittest.AsyncTestCase):

    async def test_endpoint(self):

        request = {
            "query" : "I want to book a flight from Strasbourg to London from 10/10/2019 to 15/10/2019 for 200 euros"
        }

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': CONFIG.LUIS_API_KEY
        }

        predictionEndpoint = CONFIG.LUIS_API_HOST_NAME
        app_id = CONFIG.LUIS_APP_ID
        slot_name = "Production"
        start_batch_endpoint = f'{predictionEndpoint}luis/v3.0-preview/apps/{app_id}/slots/{slot_name}/predict'

        async with aiohttp.ClientSession() as session:
            async with session.post(start_batch_endpoint, data=str(request), headers=headers) as resp:
                self.assertEqual(resp.status, 200)


# test LuisHelper.execute_luis_query()

class LuisTest(aiounittest.AsyncTestCase):

    async def test_luis_query(self):

        RECOGNIZER = FlightBookingRecognizer(CONFIG)

        async def exec_test(turn_context: TurnContext):
                
            intent, luis_result = await LuisHelper.execute_luis_query(RECOGNIZER, turn_context)

            await turn_context.send_activity(
                json.dumps(
                    {
                        "intent": intent, 
                        "booking_details": None if not hasattr(luis_result, "__dict__") else luis_result.__dict__}))
            
        adapter = TestAdapter(exec_test)

        await adapter.test(
            "Hello I want to book a flight",
            json.dumps(
                {
                    "intent": "BookFlight",
                    "booking_details": {"dst_city": None, "or_city": None, "str_date": None, "end_date": None, "budget": None}
                }
            )
        )


# test BookingDialog and MainDialog

class MainDialogTest(aiounittest.AsyncTestCase):

    async def test_booking_dialog(self):

        async def exec_test_two(turn_context: TurnContext):

            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await main_dialog.intro_step(dialog_context)

            elif results.status == DialogTurnStatus.Complete:
                await main_dialog.act_step(dialog_context)

            await conv_state.save_changes(turn_context)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        booking_dialog = BookingDialog()
        main_dialog = MainDialog(FlightBookingRecognizer(DefaultConfig()), booking_dialog)

        dialogs.add(booking_dialog)

        text_prompt = await main_dialog.find_dialog(TextPrompt.__name__)
        dialogs.add(text_prompt)

        wf_dialog = await main_dialog.find_dialog("WFDialog")
        dialogs.add(wf_dialog)

        adapter = TestAdapter(exec_test_two)

        await adapter.test("Hi!", "Hello, I'm the Flight Booking bot. I can help you book a flight. What would you like to do?")
        await adapter.test("Book a flight", "Where are you travelling from?")
        await adapter.test("Paris", "Where are you travelling to?")
        await adapter.test("London", "On what date would you like to depart?")
        await adapter.test("tomorrow", "On what date would you like to return?")
        await adapter.test("in a week", "What is your budget for this trip?")