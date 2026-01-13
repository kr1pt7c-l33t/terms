import html2text
import requests
from llamaland import LlamaLand

class Summarisor:
	def __init__(self):
		print("Init Summarisor")

	def from_file(self, file_path):
		with open(file_path, "r") as f:
			content = f.read()
			return content

	def from_url(self, url):
		response = requests.get(url)
		converter = html2text.HTML2Text()
		converter.ignore_links = True  # Optional
		text = converter.handle(response.text)
		summary = self.summarise(text)
		return summary

	def summarise(self, pol):
		summary = {
			"data_collected": "",
			"concerns": "",
			"third_parties": "",
			"user_rights": ""
		}

		llamaland = LlamaLand(pol)
		
		
		resp = llamaland.send_message(f"""You are a privacy expert. You have a skeptic's eye for any claims made by companies in their terms and policies. 
						 You advise consumers on various privacy related matters, especially ones pertaining to their interactions with big tech 
						 platforms. I am one of those consumers, here to consult you regarding a reference document. Here is the REFERENCE DOCUMENT: '{pol}'
						 The following are your tasks:
						 1. Create an executive summary that gives the user an idea of what the company looks like it is trying to do.
						 2. Extract ALL types of data this organization mentions it collects and processes in the document. For each type, explain how it will be used. Be specific and 
						 cite relevant sections.
						 3. Extract clauses that should be of concern to me.
						 4. List all third parties and subprocessors mentioned.
						 5. Summarize user rights and how to exercise them, include links where available(N/A if not available).

						 Answer by filling out the following. Provide ONLY the JSON in response. Headings to be used in the JSON:
							 "exec_summary"
							 "data_types"
							 "concerning_clauses"
							 "third_parties"
							 "user_rights"
						 """)

		# Combine into final report
		print(resp)

if __name__ == "__main__":
	summarisor = Summarisor()
	summarisor.from_url("https://www.anthropic.com/legal/privacy")
