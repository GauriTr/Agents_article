
import sys, os
from webportcrew.crew import WebportcrewCrew


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    WebportcrewCrew().crew().kickoff(inputs=inputs)


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        WebportcrewCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")



if __name__ == '__main__':
    run()