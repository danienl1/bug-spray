import requests
from bs4 import BeautifulSoup
from openai import OpenAI

class StackReconLLM:
    def __init__(self, openai_api_key):
        self.model = 'gpt-4o' #'gpt-3.5-turbo'
        self.client = OpenAI(api_key=openai_api_key)

    def fetch_website_html(self, url):
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            return response.text, response.headers
        except requests.exceptions.SSLError:
            print("SSL verification failed. Trying HTTP fallback...") # testing known bad sites
            if url.startswith("https://"):
                url = url.replace("https://", "http://")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.text, response.headers
            except requests.RequestException as e:
                print(f"Error fetching the website: {e}")
                return None, None
        except requests.RequestException as e:
            print(f"Error fetching the website: {e}")
            return None, None

    def preprocess_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        meta_tags = soup.find_all("meta")
        scripts = soup.find_all("script", src=True)
        links = soup.find_all("link", rel=True)

        relevant_data = {
            "meta": [str(tag) for tag in meta_tags],
            "scripts": [script["src"] for script in scripts if "src" in script.attrs],
            "links": [link["href"] for link in links if "href" in link.attrs],
        }

        return relevant_data

    def analyze_with_llm(self, html, headers):
        preprocessed_data = self.preprocess_html(html)
        prompt = f"""
                    Analyze the following HTML metadata and infer the technology stack of the website. Provide detailed predictions of the CMS, frameworks, analytics tools, and other technologies being used:

                    Metadata:
                    {preprocessed_data['meta']}

                    Scripts:
                    {preprocessed_data['scripts']}

                    Links:
                    {preprocessed_data['links']}

                    Headers:
                    {headers}
                """
        try:
            chat__completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ])
            response_text = chat__completion.choices[0].message.content.strip()
            return response_text
        except Exception as e:
            return None

    def display_predicted_stack(self, predicted_stack):
        if not predicted_stack:
            print("No technologies detected.")
            return

        print("Predicted Technology Stack:")
        print(predicted_stack)

