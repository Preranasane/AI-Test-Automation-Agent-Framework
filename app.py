import asyncio
from workflow import agent
from browser_manager import manager
from report_generator import generate_html_report

async def main():
    await manager.start()

    response = await agent.ainvoke({
        "messages": [
            (
                "user",
                """
                use tool : open_url and pass URL given to that langchain tool- open a url "https://practicetestautomation.com/practice-test-login/"                
                wait for sometime then definitely Call tool fill(selector="//input[@name='username']", text="student")   
                wait for sometime then definitely Call tool fill(selector="//input[@name='password']", text="Password123")
                make sure to use this tool : click - click on selector "<button id="submit" class="btn">Submit</button> aka get_by_role("button", name="Submit")"
                
                """
            )
        ]
    })

    print(response)

    # Generate the report after execution
    generate_html_report()

    await manager.stop()


asyncio.run(main())