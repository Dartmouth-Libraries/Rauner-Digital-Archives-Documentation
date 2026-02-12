"""
Dartmouth Vietnam Project - Oral History Transcript Summarizer

This script generates summaries of oral history interview transcripts using LLMs.
It supports both OpenAI API and Dartmouth Chat API, with Dartmouth Chat being
prioritized if both API keys are provided.

Usage:
    python dvp_summarizer.py

Environment Variables (set in secrets.env):
    - DARTMOUTH_CHAT_API_KEY: Your Dartmouth Chat API key (prioritized if both provided)
    - OPENAI_API_KEY: Your OpenAI API key

Model Configuration:
    - DARTMOUTH_MODEL: Model ID for Dartmouth Chat (default: anthropic.claude-3-5-haiku-20241022)
    - OPENAI_MODEL: Model ID for OpenAI (default: gpt-4o-2024-08-06)
"""

from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import List, Optional

from openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader

# Load environment variables from secrets.env
load_dotenv("secrets.env")

# Configuration
DARTMOUTH_CHAT_API_KEY = os.getenv("DARTMOUTH_CHAT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default models - can be overridden via environment variables
DEFAULT_DARTMOUTH_MODEL = "anthropic.claude-3-5-haiku-20241022"
DEFAULT_OPENAI_MODEL = "gpt-4o-2024-08-06"

DARTMOUTH_MODEL = os.getenv("DARTMOUTH_MODEL", DEFAULT_DARTMOUTH_MODEL)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)

# Dartmouth Chat API base URL
DARTMOUTH_BASE_URL = "https://chat.dartmouth.edu/api"


class LLMClient:
    """
    Unified LLM client that works with both Dartmouth Chat API and OpenAI API.
    Uses the OpenAI SDK directly for better compatibility with various models.
    """

    def __init__(self):
        if DARTMOUTH_CHAT_API_KEY:
            print(f"Using Dartmouth Chat API with model: {DARTMOUTH_MODEL}")
            self.client = OpenAI(
                api_key=DARTMOUTH_CHAT_API_KEY,
                base_url=DARTMOUTH_BASE_URL,
            )
            self.model = DARTMOUTH_MODEL
            self.provider = "dartmouth"
        elif OPENAI_API_KEY:
            print(f"Using OpenAI API with model: {OPENAI_MODEL}")
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
            )
            self.model = OPENAI_MODEL
            self.provider = "openai"
        else:
            raise ValueError(
                "No API key configured. Please set either DARTMOUTH_CHAT_API_KEY "
                "or OPENAI_API_KEY in your secrets.env file."
            )

    def invoke(self, messages: List) -> str:
        """
        Send messages to the LLM and return the response content.

        Args:
            messages: List of message objects with 'role' and 'content' attributes,
                     or tuples of (role, content).

        Returns:
            The text content of the LLM's response.
        """
        # Convert messages to the format expected by OpenAI API
        formatted_messages = []
        for msg in messages:
            if hasattr(msg, 'content') and hasattr(msg, 'type'):
                # LangChain message object
                role = "system" if "system" in msg.type.lower() else "user"
                if "human" in msg.type.lower():
                    role = "user"
                formatted_messages.append({"role": role, "content": msg.content})
            elif isinstance(msg, tuple):
                formatted_messages.append({"role": msg[0], "content": msg[1]})
            elif isinstance(msg, dict):
                formatted_messages.append(msg)
            else:
                # Fallback: try to extract content
                formatted_messages.append({"role": "user", "content": str(msg)})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.0,
            )

            # Debug: print response structure if there's an issue
            if not response.choices:
                raise RuntimeError(f"API returned no choices. Response: {response}")

            message = response.choices[0].message
            if message is None:
                raise RuntimeError(f"API returned None message. Response: {response}")

            content = message.content
            if content is None:
                # Some models might return content in a different field
                raise RuntimeError(f"API returned None content. Message: {message}")

            return content
        except Exception as e:
            raise RuntimeError(f"API call failed: {e}")

    def get_model_name(self) -> str:
        """Return the model name being used."""
        return self.model


def get_llm() -> LLMClient:
    """Initialize and return the LLM client."""
    return LLMClient()


def get_model_name() -> str:
    """Return the model name being used for record-keeping."""
    if DARTMOUTH_CHAT_API_KEY:
        return DARTMOUTH_MODEL
    elif OPENAI_API_KEY:
        return OPENAI_MODEL
    return "unknown"


# Validate that at least one API key is available
if not DARTMOUTH_CHAT_API_KEY and not OPENAI_API_KEY:
    raise ValueError(
        "No API key found. Please set either DARTMOUTH_CHAT_API_KEY or "
        "OPENAI_API_KEY in your secrets.env file."
    )

# Initialize the LLM and test connection
llm = get_llm()

# Quick test to verify API is working
print("Testing API connection...")
try:
    test_response = llm.invoke([
        {"role": "user", "content": "Say 'ok' if you can read this."}
    ])
    print(f"API test successful. Response: {test_response[:50]}...")
except Exception as e:
    print(f"WARNING: API test failed: {e}")
    print("The script will continue but may encounter errors during processing.")
    print("Consider trying a different model in your secrets.env file.")

# Directory paths
docs_dir = Path("ConvertedTranscripts")
abstracts_dir = Path("ConvertedAbstractsBulletPoints")

# Load documents
print("Loading transcripts...")
doc_loader = DirectoryLoader(docs_dir, show_progress=True)
docs = doc_loader.load()

print("Loading abstracts/bullet points...")
abstract_loader = DirectoryLoader(abstracts_dir, show_progress=True)
abstracts = abstract_loader.load()

# System instructions for the summarization task
SYSTEM_PROMPT = """You are a digital archivist. Your job is to write summaries of oral history interview transcripts.
Your job is to describe the contents of the interview, not write a biography of the interviewee.
Do not summarize everything that was said. Focus on describing the interviewee's report of their experience during the Vietnam War era.
Use indirect speech as much as possible.
Here are some examples:
---
Avoid: "His decision to study math at Dartmouth was influenced by the societal push"
Use: "He describes how his decision to study math at Dartmouth was influenced by the societal push"
Avoid: "After an injury led to a long recovery, he decided to leave the Navy."
Use: "He relates his decision to leave the navy following an injury."
---
Here is a good example of the kind of oral history abstract you are tasked with writing:
---
Oral history interview with Michael W. Parker, Class of 1964, for the Dartmouth Vietnam Project. Parker describes his time at Dartmouth and his involvement with the Navy ROTC [Reserve Officers' Training Corps]. He discusses how he participated in the Navy ROTC program throughout the summer and how he was able to walk on to the Dartmouth ski team. Parker tells of his decision to postpone dental school to join the Navy and his experience being sent to Vietnam. Parker describes working on the staff of Admiral Elmo R. Zumwalt Jr. and Admiral Zumwalt's leadership as well as the ways in which he believed Zumwalt had transformed the Navy. He discusses his work to control the Mekong Delta in Vietnam while aboard the USS Frigate Bird, performing mine countermeasures and swimmer defense operations. Parker details how the Navy developed riverine warfare during Vietnam. After his time in Vietnam, Parker explains how he attended dental school at Tufts University School of Dental Medicine and remained in the U.S. Navy Reserve's. He describes being offended by the anti-war acts that his fellow classmates participated in rather than attending class while a student at Tufts. Parker shares how he was sent back to the USS Frigate Bird after he completed dental school. He discusses his career after dental school which included teaching for three years with the Navy Officer Candidate School, four years in Scotland, and 11 years teaching for the Naval Postgraduate Dental School.
---
"""


def build_messages(transcript: str, bullet_points: Optional[str] = None) -> List[dict]:
    """
    Build the message list for the LLM API call.

    Args:
        transcript: The interview transcript text.
        bullet_points: Optional bullet points to guide the summary.

    Returns:
        List of message dictionaries.
    """
    if bullet_points:
        user_content = f"Summarize the following transcript in 250 words or less, organizing the summary around the following bullet points: \n\n {transcript} \n\n {bullet_points}"
    else:
        user_content = f"Summarize the following transcript: \n\n {transcript}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def get_interviewee_name(doc):
    """Extract interviewee name from document metadata."""
    return "_".join(Path(doc.metadata["source"]).stem.split("_")[:2])


def find_matching_abstract(interviewee, abstracts):
    """Find the abstract that matches the given interviewee."""
    for abstract in abstracts:
        if Path(abstract.metadata["source"]).stem.startswith(interviewee):
            return abstract.page_content
    return None


def run_summarization(
    target_interviewee=None,
    use_abstracts=True,
    output_file="dvp_summaries.csv",
):
    """
    Run the summarization process on all transcripts.

    Args:
        target_interviewee: Optional; If provided, only process transcripts
                           for this interviewee (e.g., "cox_robert").
        use_abstracts: Whether to use abstracts/bullet points in prompts.
                      Default is True.
        output_file: Path to the output CSV file. Default is "dvp_summaries.csv".

    Returns:
        DataFrame containing the summaries.
    """
    # Check if the CSV already exists
    try:
        df = pd.read_csv(output_file)
    except FileNotFoundError:
        df = None

    summarylist = []
    model_name = llm.get_model_name()

    for doc in docs:
        # Skip if targeting a specific interviewee
        if target_interviewee and target_interviewee not in doc.metadata["source"]:
            continue

        # Find matching abstract if using abstracts
        bullet_points = None
        if use_abstracts:
            interviewee = get_interviewee_name(doc)
            bullet_points = find_matching_abstract(interviewee, abstracts)

        # Generate the appropriate prompt
        messages = build_messages(doc.page_content, bullet_points)
        bullet_used = bullet_points is not None

        # Extract prompt text for record-keeping (truncate to first 400 characters)
        prompt_text = SYSTEM_PROMPT[:400]

        # Generate summary using the LLM
        print(f"Processing: {doc.metadata['source']}")
        try:
            summary_content = llm.invoke(messages)
        except Exception as e:
            print(f"Error processing {doc.metadata['source']}: {e}")
            continue

        summarylist.append(
            {
                "source": doc.metadata["source"],
                "summary": summary_content,
                "prompt": prompt_text,
                "Bullet Used": bullet_used,
            }
        )

    if not summarylist:
        print("No summaries generated.")
        return df

    # Create DataFrame with new records
    new_records = pd.DataFrame.from_records(summarylist)

    # Add metadata columns
    new_records["LLM Model"] = model_name
    new_records["Date"] = datetime.now().strftime("%Y-%m-%d")
    new_records["Time"] = datetime.now().strftime("%H:%M:%S")

    # Combine with existing data if available
    if df is None:
        df = new_records
    else:
        df = pd.concat([df, new_records])

    # Save to CSV
    df.to_csv(output_file, index=None)
    print(f"Summaries saved to {output_file}")

    return df


if __name__ == "__main__":
    # Configuration - modify these as needed
    TARGET_INTERVIEWEE = None  # Set to e.g., "cox_robert" to process only that interviewee
    USE_ABSTRACTS = True  # Set to False to not use abstracts/bullet points
    OUTPUT_FILE = "dvp_summaries.csv"

    # Run the summarization
    print(f"\nStarting summarization process...")
    print(f"Model: {llm.get_model_name()}")
    print(f"Using abstracts: {USE_ABSTRACTS}")
    print(f"Target interviewee: {TARGET_INTERVIEWEE or 'All'}\n")

    result_df = run_summarization(
        target_interviewee=TARGET_INTERVIEWEE,
        use_abstracts=USE_ABSTRACTS,
        output_file=OUTPUT_FILE,
    )

    if result_df is not None:
        print(f"\nProcessing complete. Total records: {len(result_df)}")
        print(result_df)
    else:
        print("\nNo results to display.")
