from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LectureSummarizer:
    def __init__(self):
        """Explicitly loads the tokenizer and the model."""
        print("Loading NLP Summarization Model (DistilBART)...")
        self.model_name = "sshleifer/distilbart-cnn-12-6"
        
        # 1. Load the Tokenizer (Text -> Numbers)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # 2. Load the Model (The AI Brain)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def summarize(self, text):
        """Takes a transcript, tokenizes it, and generates a summary."""
        if not text or len(text.strip()) == 0:
            return "Error: No text provided to summarize."
            
        print("\nSummarizing transcript... (This might take a moment on CPU)")
        
        try:
            # 1. Tokenize the input text
            # truncation=True ensures we don't crash if the text is over 1024 tokens
            inputs = self.tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
            
            # 2. Generate the summary
            # num_beams=4 means the AI explores 4 different phrasing paths before picking the best one
            summary_ids = self.model.generate(
                inputs["input_ids"], 
                max_length=130, 
                min_length=30, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True
            )
            
            # 3. Decode the output (Numbers -> Text)
            summary_text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary_text
            
        except Exception as e:
             return f"Summarization failed: {e}"