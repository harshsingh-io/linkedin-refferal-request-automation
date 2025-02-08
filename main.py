import asyncio
import os
from dotenv import load_dotenv
from src.auth import LinkedInAuth
from src.linkedin_api import LinkedInAPI
from src.message_handler import MessageHandler
from config.config import Config
import logging
from rich.console import Console

console = Console()

async def main():
    # Load environment variables
    load_dotenv()
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        filename='logs/main.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Load configuration
        config = Config()
        criteria = config.get_search_criteria()
        credentials = config.get_credentials()

        # Initialize authentication
        auth = LinkedInAuth()
        driver = auth.initialize_driver()
        
        # Login
        if not await auth.login(credentials['email'], credentials['password']):
            console.print("[red]Login failed. Please check your credentials.[/red]")
            return

        # Initialize API and message handler
        api = LinkedInAPI(driver)
        message_handler = MessageHandler()

        # Search for profiles
        console.print("\n[green]Searching for matching profiles...[/green]")
        profiles = api.search_profiles(criteria)
        console.print(f"[blue]Found {len(profiles)} profiles[/blue]")

        if not profiles:
            console.print("[red]No matching profiles found. Check the search criteria in config.yaml[/red]")
            return

        # Process search results and send connection requests
        await api.process_search_results(criteria)

        # Summary
        console.print(f"\n[bold green]Operation completed:[/bold green]")
        console.print(f"Total profiles found: {len(profiles)}")
        console.print(f"Successful requests sent: {api.sent_requests}")

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        console.print(f"[red]An error occurred: {str(e)}[/red]")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    asyncio.run(main()) 