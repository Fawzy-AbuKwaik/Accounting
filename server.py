from fastapi import FastAPI, Request # FastAPI let me create my web server/app, Request represents a HTTP request that aarives my server Like whatsaap HTTP requaest (mate)
# Normally FastAPI returns JSON responses
from fastapi.responses import PlainTextResponse # PlainTextResponse return a plain text response. We need it to the webhook verification

app = FastAPI() # creat the FastAPI app intance. so I run: "python -m uvicorn server:app --reload", where server is server.py and app = FastAPI()
VERIFY_TOKEN = "my_verify_Token_55" # This is simply a variable containing a secret-ish verification string that I choose, when configuring the webhook with Meta, I'll give Meta the same value

@app.get("/") # this line called "Decorator", If someone sends a GET request to /, execute the function directly below. "http//127.0.0.1:8000/"
def home():
    return{"status": "invoice server is running"} # it is python dectionary, FastAPI will automatically convert it to JSON and send it back to the client.

@app.get("/webhook") # "http//127.0.0.1:8000/webhook" if someone sends a GET request to /webhook, execute the function directly below. This is the webhook verification endpoint that Meta will call to verify my webhook.
# async def means that this function is asynchronous, which allows it to handle multiple requests concurrently without blocking the server. 
# this function receive a parameter called request, has type Request, which represents the incoming HTTP request. 
# It allows me to access query parameters, headers, and other request data, 
# like "GET /webhook
                # ?hub.mode=subscribe
                # &hub.verify_token=my_verify_token_123
                # &hub.challenge=123456789"
# if all parameters are correct, return the challenge value back to Meta, which confirms that I own the webhook endpoint and that it is working correctly.
async def verify_webhook(request: Request): 
    mode      = request.query_params.get("hub.mode") # get the value of the query parameter hub.mode from the incoming request. This parameter is sent by Meta during the webhook verification process to indicate the mode of the request. In this case, it should be "subscribe" if Meta is trying to verify my webhook.
    token     = request.query_params.get("hub.verify_token") # get the value of the query parameter hub.verify_token from the incoming request. This parameter is sent by Meta during the webhook verification process to provide a token that I have previously set up in my Meta app settings. I will compare this token with my own VERIFY_TOKEN to ensure that the request is legitimate and coming from Meta.
    challenge = request.query_params.get("hub.challenge") # get the value of the query parameter hub.challenge from the incoming request. This parameter is sent by Meta during the webhook verification process and contains a random string that I need to return in my response if the verification is successful. Returning this challenge value confirms to Meta that I own the webhook endpoint and that it is working correctly.
    if mode == "subscribe" and token == VERIFY_TOKEN: # if the mode is "subscribe" and the token matches my VERIFY_TOKEN, it means that Meta is trying to verify my webhook and the request is legitimate.
        return PlainTextResponse(content = challenge, status_code = 200) # return a plain text response with the challenge value and a status code of 200 (OK). This tells Meta that the verification was successful and that I own the webhook endpoint.
    return PlainTextResponse(content = "Verification failed", status_code = 403) # If the mode is not "subscribe" or the token does not match my VERIFY_TOKEN, it means that the request is either not a verification request or is not coming from Meta. In this case, I return a plain text response with the content "Verification failed" and a status code of 403 (Forbidden). This tells Meta that the verification failed and that I do not own the webhook endpoint.
        
@app.post("/webhook") # if someone sends a POST request to /webhook, execute the function directly below. This is the webhook endpoint that Meta will call when there is a new message or event for my WhatsApp Business account.
async def receive_wehook(request: Request):
    data = await request.json() # read the incoming request body as JSON and store it in the variable data. This is where I will receive the actual message or event data from Meta.
    print(data) # print the received data to the console for debugging purposes. This allows me to see the structure and content of the incoming message or event data.
    return {"status": "received"}