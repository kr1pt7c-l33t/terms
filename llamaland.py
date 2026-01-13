import requests
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "deepseek-r1:7b"
MODEL_NAME = "llama3.2"

class LlamaLand:
	def __init__(self, policy_text, url=OLLAMA_URL, model=MODEL_NAME):
		self.url = url
		self.model = model
		self.context = None  # Initialize context storage
		self.conversation_history = []  # Optional: track conversation history
	
	def send_message(self, prompt):
		payload = {
			"model": self.model,
			"prompt": prompt,
			"stream": True
		}
		
		# Add context if it exists (crucial for multi-turn conversations)
		if self.context:
			payload["context"] = self.context
		
		try:
			response = requests.post(
				self.url,
				json=payload,
				stream=True
			)
			response.raise_for_status()

			full_response = ""
			print("\nResponse: ", end="", flush=True)

			# Process each line of the streaming response
			for line in response.iter_lines():
				if line:
					try:
						json_line = json.loads(line)

						# Get the response chunk
						chunk = json_line.get("response", "")
						full_response += chunk
						print(chunk, end="", flush=True)

						# Check if this is the final chunk
						if json_line.get("done", False):
							# Store context for next call
							self.context = json_line.get("context")
							# Optional: store conversation history
							self.conversation_history.append({
								"prompt": prompt,
								"response": full_response
							})
							break

					except json.JSONDecodeError as e:
						print(f"\nError decoding JSON line: {e}")
						continue

			print("\n")  # Add newline after response
			return full_response

		except requests.exceptions.RequestException as e:
			print(f"Error communicating with LLM: {e}")
			return ""
	
	def reset_context(self):
		"""Reset the conversation context"""
		self.context = None
		self.conversation_history = []
		print("Context has been reset.")