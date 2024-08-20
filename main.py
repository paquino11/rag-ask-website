from scrape_website import scrape
from rag import setup_and_run_rag_pipeline

def main():
    # Step 1: Run the web crawler to scrape the website
    url = 'https://docs.crewai.com'
    output_file = 'output.json'
    
    print(f"Starting web crawl for: {url}")
    scrape(start_url=url, output_file=output_file)
    print(f"Web crawl completed. Data saved to {output_file}.\n")
    
    # Step 2: Process the scraped data using the RAG pipeline
    question = "What's an Agent?"
    print("Starting RAG pipeline for question answering...\n")
    answer = setup_and_run_rag_pipeline(
        json_path=output_file,
        question=question,
        model="gpt-4o-mini"
    )
    
    # Step 3: Display the answer
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
