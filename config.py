#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os

class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "8395514b-224f-435e-944d-134b00913f0d")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "hFW8Q~kzQnV1EPtOxi4km_MaRO7wTybDohsiwaO5")
    LUIS_APP_ID = os.environ.get("LuisAppId", "db70b5ef-3103-46a0-aa92-7cbfd39c1439")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "86630a0d4ffa4c56a2a80714dce8714c")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://luisp10.cognitiveservices.azure.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "61449954-e098-49e5-b651-4d70250e38d8"
    )