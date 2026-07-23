from langchain.tools import tool
from browser_manager import manager
from report_manager import report
import os
from datetime import datetime

async def capture_step():
    """
    Capture screenshot and log it.
    """

    os.makedirs("reports/screenshots", exist_ok=True)

    filename = f"reports/screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"

    await manager.page.screenshot(
        path=filename,
        full_page=True
    )

    report.log(
        action="Screenshot",
        status="PASS",
        screenshot=filename
    )

    return filename

@tool
async def open_url(url: str):

    """
    open a website

    """
    await manager.page.goto(url)
    report.log(
        action=f"Open URL {url}",
        status="PASS"
    )

@tool
async def click(selector: str):

    """
    click on selector

    """
    try:
        locator = manager.page.locator(selector)
        await locator.wait_for(state="visible")
        await locator.scroll_into_view_if_needed()
        await locator.click(timeout=10000)
        await capture_step()
        report.log(
            action=f"Click {selector}",
            status="PASS"
        )
        return "clicked"
    except Exception as e:

        report.log(
            action=f"Click {selector}",
            status="FAIL",
            details=str(e)
        )

        raise

@tool
def hello(name: str) -> str:
    """
    Say hello to a person.
    """
    print(f"Tool invoked with: {name}")
    return f"Hello {name}!"

@tool
async def fill(selector: str, text: str) -> str:
    """
    Fill text into an input field.

    Args:
        selector: XPath or CSS selector of the input element.
        text: Text to enter into the input field.

    Returns:
        Confirmation message.
    """
    try:
        locator = manager.page.locator(selector)
        await locator.wait_for(state="visible")
        await locator.scroll_into_view_if_needed()
        await locator.fill(text)
        await capture_step()
        report.log(
            action=f"fill {selector}",
            status="PASS"
        )
        return f"Filled '{text}' into element: {selector}"
    except Exception as e:

        report.log(
            action=f"fill {selector}",
            status="FAIL",
            details=str(e)
        )

        raise

