"""
Lesson 07 - Basic Embeddings
"""

import math
import os

from dotenv import load_dotenv
from langchain_community.embeddings import ZhipuAIEmbeddings

# Load Environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL")

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    dot_product = sum(x*y for x,y in zip(a, b))
    mag_a = math.sqrt(sum(x*x for x in a))
    mag_b = math.sqrt(sum(y*y for y in b))
    return dot_product / (mag_a * mag_b)

def main():
    print("Basic Embeddings Example\n")
    
    # Initialize the embedding
    zhipu_embeddings = ZhipuAIEmbeddings(
        api_key=ZHIPUAI_API_KEY,
        api_base=ZHIPUAI_BASE_URL,
        model="embedding-3"
    )

    # Create embeddings for different texts
    texts = [
        "LangChain makes building AI apps easier",
        "LangChain simplifies AI application development",
        "I love eating pizza for dinner",
        "The weather is sunny today",
    ]
    print("Creating embeddings for text...\n")
    all_embeddings = zhipu_embeddings.embed_documents(texts)
    print(f"Created {len(all_embeddings)} embeddings")
    print(f"  Each embedding has {len(all_embeddings[0])} dimensions\n")

    # Show first embedding details
    print("First embedding (first 10 values):")
    print(all_embeddings[0][:10])
    print("\n" + "="*80 + "\n")

    # Compare Similarities
    print("Similarity Comparisons:\n")
    pairs = [
        (0, 1, "LangChain vs LangChain (similar meaning)"),
        (0, 2, "LangChain vs Pizza (different topics)"),
        (0, 3, "LangChain vs Weather (different topics)"),
        (2, 3, "Pizza vs Weather (both different from LangChain)"),
    ]
    for i, j, description in pairs:
        similarity = cosine_similarity(all_embeddings[i], all_embeddings[j])
        print(f"{description}:")
        print(f"  Score: {similarity:.4f}")
        print(f"  Text: {texts[i]} vs. {texts[j]}\n")

if __name__ == "__main__":
    main()