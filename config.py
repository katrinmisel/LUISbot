#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    #APP_ID = ""
    #APP_PASSWORD = ""
    APP_ID = os.environ.get("MicrosoftAppId", "792b65c2-8a6d-4332-adbb-683221ab6e93")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "a3W8Q~UeA7Kflkmy7lLtIYcg.qQaa4ARW676PapT")
    LUIS_APP_ID = os.environ.get("LuisAppId", "9a2e59b9-686d-492b-959b-8ceff62b8494")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "31031bdf48c943c5a836b722abe99440")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://flymeresource.cognitiveservices.azure.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", ""
    )