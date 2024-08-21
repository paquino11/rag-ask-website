from scrape_website import scrape
from rag import setup_and_run_rag_pipeline

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def main():
    # Step 1: Run the web crawler to scrape the website
    url = 'https://docs.crewai.com'
    scrape(start_url=url)
    
    # Step 2: Process the scraped data using the RAG pipeline
    question = "How can I start a new crewAI project?"
    answer = setup_and_run_rag_pipeline(
        question=question,
    )
    
    print(f"{RED}Question: {question}{RESET}")
    print(f"{GREEN}Answer: {answer}{RESET}")

if __name__ == "__main__":
    main()
