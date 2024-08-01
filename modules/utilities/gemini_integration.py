import os
import textwrap

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

crop_diagnosis = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        "is_infected": genai.protos.Schema(type=genai.protos.Type.BOOLEAN),
        "crop_name": genai.protos.Schema(type=genai.protos.Type.STRING),
        "crop_type": genai.protos.Schema(type=genai.protos.Type.STRING),
        "disease_name": genai.protos.Schema(type=genai.protos.Type.STRING),
        "treatment_recommendation": genai.protos.Schema(type=genai.protos.Type.STRING),
        "how_to_identify_disease": genai.protos.Schema(type=genai.protos.Type.STRING),
        "causes_of_disease": genai.protos.Schema(type=genai.protos.Type.STRING),
        "other_things_to_note": genai.protos.Schema(type=genai.protos.Type.STRING),
        "confidence_level": genai.protos.Schema(type=genai.protos.Type.NUMBER),
    },
    required=[
        "is_infected",
        "confidence_level",
        "crop_name",
        "crop_type",
        "disease_name",
        "treatment_recommendation",
    ],
)

treatment_recommendation = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        "title": genai.protos.Schema(type=genai.protos.Type.STRING),
        "description": genai.protos.Schema(type=genai.protos.Type.STRING),
    },
)


def call_gemini(prompt: dict):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt["text"], prompt["img"]], stream=True)
    return response


add_to_database = genai.protos.FunctionDeclaration(
    name="add_to_database",
    description=textwrap.dedent(
        """\
        Adds entities to the database.
        """
    ),
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={"crop_diagnosis": crop_diagnosis},
    ),
)


def get_disease_data(prompt, imagePaths):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", tools=[add_to_database])
    ## loop through the imagePaths and upload the images
    uploadedImages = []
    for dict in imagePaths:
        image = genai.upload_file(path=dict)
        uploadedImages.append(image)
        result = model.generate_content(
            [
                f"""
            You are an expert in agriculture and you have been asked
            to provide information on a crop disease.
            Add the response to the database
            {prompt}
            """,
                *uploadedImages,
            ],
            # Force a function call
            tool_config={"function_calling_config": "ANY"},
        )
    fc = result.candidates[0].content.parts[0].function_call
    images = [file_obj.uri for file_obj in uploadedImages]
    return type(fc).to_dict(fc)["args"]["crop_diagnosis"], images
