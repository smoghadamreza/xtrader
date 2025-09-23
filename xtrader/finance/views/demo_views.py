from __future__ import annotations

from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from finance.templates import FinanceTemplates
from utils.consts import XtraderResponseKeys
from .base_views import get_user_context


DEFAULT_SYMBOL_ID: str = "IRO1IKCO0001"


def test_volume(request: HttpRequest) -> HttpResponse:
    """
    Render the Test Volume page with a default symbol ID and user context.
    """
    context: Dict[str, str] = {
        XtraderResponseKeys.SYMBOL_ID: DEFAULT_SYMBOL_ID,
        **get_user_context(request),
    }
    return render(request, FinanceTemplates.TEST_VOLUME, context)


def test_api(request: HttpRequest) -> HttpResponse:
    """
    Render the Test API page with a default symbol ID.
    """
    context: Dict[str, str] = {
        XtraderResponseKeys.SYMBOL_ID: DEFAULT_SYMBOL_ID,
    }
    return render(request, FinanceTemplates.TEST_API, context)
