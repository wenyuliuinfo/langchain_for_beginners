"""
Lesson 07 - Comparing Chunk Overlap
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    print("Chunk Overlap Comparison\n")

    text="""
The mitochondria is often called the powerhouse of the cell. This organelle
is responsible for producing ATP, the energy currency that powers cellular
processes. Mitochondria have their own DNA, separate from the cell's nuclear
DNA, which supports the theory that they were once independent organisms.
Through a process called cellular respiration, mitochondria convert nutrients
into usable energy. This process involves several complex steps including
glycolysis, the Krebs cycle, and the electron transport chain.
    """.strip()

    print("Original text:")
    print("-" * 80)
    print(text)
    print("\n" + "=" * 80)

    # Splitter with no overlap
    print("\n1. Splitting with NO overlap:\n")
    no_overlap = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=0,
    )
    chunks_1 = no_overlap.create_documents([text])
    for i, doc in enumerate(chunks_1):
        print(f"Chunk {i+1}: '{doc.page_content}'\n")
    print("Notice: Context may be lost between chunks!\n")

    # Splitter with overlap
    print("=" * 80)
    print("\n2. Splitting with overlap (30 characters):\n")
    with_overlap = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
    )
    chunks_2 = with_overlap.create_documents([text])
    for i, doc in enumerate(chunks_2):
        print(f"Chunk {i+1}: '{doc.page_content}'\n")
        if i > 0:
            overlap = doc.page_content[:30]
            print(f"  Overlaps with: {overlap}...\n")

    print("Notice: Overlapping text preserves context!\n")

if __name__ == "__main__":
    main()