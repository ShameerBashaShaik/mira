from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os
import glob

# Load environment variables
load_dotenv()

# Initialize the Mira client with API key from environment variable
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

def deploy_flows():
    """
    Deploy all flow YAML files from the flows directory to the Mira platform.
    """
    # Get all YAML files in the flows directory
    flow_files = glob.glob("flows/*.yaml")

    for flow_file in flow_files:
        try:
            # Create flow from YAML file
            flow = Flow(source=flow_file)

            # Deploy to the platform
            client.flow.deploy(flow)

            # Get flow name from filename
            flow_name = os.path.splitext(os.path.basename(flow_file))[0]
            flow_id = f"aahnik/{flow_name}"
            print(f"Flow deployed successfully with ID: {flow_id}")

        except FlowError as e:
            print(f"Error deploying flow {flow_file}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error with {flow_file}: {str(e)}")

def test_flow(flow_id, inputs):
    """
    Execute the flow with given inputs.
    """
    try:
        # Execute the flow with inputs
        result = client.flow.execute(flow_id, inputs)
        return result
    except FlowError as e:
        print(f"Error running flow: {str(e)}")
        return None

def main():
    # Deploy the flow
    print("Deploying flow...")
    deploy_flows()

    # Test the notes maker flow with a sample text
    text_sample = """
    ChatGPT is an AI language model that helps with various tasks, such as coding, writing, answering questions, and more. It's versatile and can be used across many fields.
    """

    print("\nTesting notes-maker flow...")
    result = test_flow("aahnik/notes-maker", {
        "text": text_sample,  # Text to be turned into notes
        "language": "english",  # Language of the text
        "summary_length": 100  # Optional: Define the length of the summary or notes
    })
    if result:
        print("\nGenerated Notes:")
        print(result)

if __name__ == "__main__":
    main()
