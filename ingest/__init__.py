from .amazon import start_amazon_ingestion

def run_all_ingesters():
    start_amazon_ingestion()
    # Add other ingesters here as needed

if __name__ == "__main__":
    run_all_ingesters()