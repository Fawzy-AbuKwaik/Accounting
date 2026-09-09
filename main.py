from pathlib import Path
from dotenv import load_dotenv # for .env file (where we store our API key), we do that to avoid hardcoding the API key in the code (for security reasons)
from openai import OpenAI # We're going to use it to communicate with the OpenAI API.
import base64 # Base64 converts binary data into text characters (encoding)
import os # os gives Python access to operating-system-related functionality

load_dotenv() # as loading the variables
# os.getenv("OPENAI_API_KEY") to get the value of the variable OPENAI_API_KEY from the .env file (loading)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # which creates an object that knows how to communicate with the API

image_path = Path("invoices/صيدلية البهاء.jpeg") # select image
if image_path.exists():
    print("Invoice found")
    print("path:", image_path)
else:
    print("Invoice not found")
    
with open(image_path, "rb") as image_file: # open the image file in binary mode
    # image_file.read()Reads all the image bytes
    # base64.b64encode Converts those bytes into Base64
    # decode("utf-8") Converts the Base64 bytes into a normal Python string.
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    response = client.responses.create( # create a response from the API and store the response
        model = "gpt-5.6",
        input = [ # Python list
            { # Python dictionary
                "role": "user", # This says that the following content represents the user's request to the AI. It's basically equivalent to I sending to chatgpt a message in app or website
                "content": [ # We're giving the AI multiple pieces of content -> Analyze an invoice + the actual image.
                    {
                        "type": "input_text", # This piece of content is text (prompt)
                        "text": """Extract exactly:
                        - name
                        - business_number
                        - invoice_number
                        
                        IMPORTANT INVOICE NUMBER RULE:
                        The invoice number may consist of a letter and a number.
                        the letter may be printed separateky or some diatance away from the numeric part of the invoice number.
                        For example:
                        If the invoice shows the letter "B" separately and the number "01101", return: "invpice_number": "B01101"
                        Look around the invoice for a letter that belongs to the invoice number.
                        Dont return only the numeric part if such a prefix letter exists.
                         
                        Return only JSON like this:
                        {
                            "name": "",
                            "business_number": "",
                            "invoice_number": ""
                        }
                        If a value is unclear, return null.
                        """
                    },
                    {
                        "type": "input_image", # The next content is an image.
                        "image_url": f"data:image/jpeg;base64,{image_base64}" # sent the image after decoding it to base64 and then converting it to a data URL format.
                    }
                ]
            }
        ]
    )
    print(response.output_text)