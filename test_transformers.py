from transformers import pipeline

print("Starting test...")
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("Classifier initialized successfully!")
    
    # Test the classifier
    text = "The stock market had a great day with major indices up by 2%"
    result = classifier(text, ["business", "politics", "UPSC"])
    print("\nTest classification result:")
    print(result)
except Exception as e:
    print(f"Error: {str(e)}")
