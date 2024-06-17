# Master's Thesis

With this work, we compare the impact of different human-AI collaboration frameworks on clinicians’ diagnostic performance. Most notably, we compare hypothesis-driven AI and recommendations-driven AI as introduced by Miller, [2023](https://arxiv.org/abs/2302.12389).

**Our work is not yet available.**

This GitHub repository contains the code for the visual analytics workspace used to support this study.

_NB: An alternate version of the app was developped for the pre-study, replacing the task of complex medical diagnosis with finding a suspect in a mystery fiction, and can be found in the [sleuth branch](https://github.com/antoinebasseto/master_thesis/tree/sleuth)._

## Web app

A deployed web app is available [here](masterthesis-kjzdrg47twqjzhukze74pt) as long as OpenAI credits have not reached their limits.

## How to run

Follow these steps to set up and run the app:

1. Clone the repository by running the following command in your terminal:
    ```bash
    git clone https://github.com/antoinebasseto/master_thesis
    ```
2. Change into the cloned directory:
    ```bash
    cd master_thesis
    ```
3. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
4. Create the recommendations-driven and hypothesis-driven assistants on the OpenAI platform and get their id.
5. Create a `secrets.toml` file in a `.streamlit` directory and fill it with the required secrets. The structure of the secrets.toml file should look something like this:
    ```toml
    # directory here is master_thesis/.streamlit/secrets.toml
    OPENAI_API_KEY = your_openai_api_key
    OPENAI_RECOMMENDATIONS_DRIVEN_ASSISTANT_ID = your_recommendations_driven_assistant_id
    OPENAI_HYPOTHESIS_DRIVEN_ASSISTANT_ID = your_hypothesis_driven_assistant_id
    ```
    Ensure all necessary values are filled out correctly.
6. You can now run the application using Streamlit:
    ```bash
    streamlit run app.py
    ```