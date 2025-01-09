from dotenv import load_dotenv
import os
from stack_recon_llm import StackReconLLM

load_dotenv()
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

def main():
    stack_recon = StackReconLLM(OPENAI_API_KEY)

    html, headers = stack_recon.fetch_website_html("https://yrprey.com/")
    if html:
        predicted_stack = stack_recon.analyze_with_llm(html, headers)
        stack_recon.display_predicted_stack(predicted_stack)
    else:
        print("Failed to fetch the website or no data available.")
if __name__ == "__main__":
    main()
