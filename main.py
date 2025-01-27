# tools to come
# nitro gen | DONE
# server joiner 
# dm tool 
# token checker | Done
#
# when running nitro gen, to stop it press CTRL+C as not make a timeout code for it yet

from fastapi import *
import uvicorn
import time
from threading import Thread
import requests
import os
import string
import numpy as np
from discord_webhook import DiscordWebhook

app = FastAPI()

#all discord functions will be here
class DiscordFunctions():
    def WebhookSpam(webhook: str, message: str, timeout: float):
        start = time.time()
        while True:
            try:
                hook = requests.post(webhook, json={'content': message})
                if hook.status_code == 204:
                    if time.time() - start > timeout:
                        break
            except:
                raise HTTPException(status_code=400, detail="There is a problem with the webhook provided!")
        
    def DeleteWebhook(webhook: str):
        try:
            response = requests.delete(webhook)
            if response.status_code == 204:
                print(f"\nWebhook {webhook} deleted successfully.\n")
            else:
                print(f"\nFailed to delete webhook: {webhook} . Status code: {response.status_code}\n")
        except Exception as e:
            print(f"\nError deleting webhook: {e}\n")

    #this function will send all the code to a webhook
    def NitroGenerator(webhook_url: str):
        while True:
            try:
                characters = string.ascii_letters + string.digits
                length = 16  # Length of nitro code
                random_string = ''.join(np.random.choice(list(characters), size=length))
                t = random_string
                output_code = f"https://discord.gift/{t}"  # Code to output (if link works or doesn't)
                webhook_output_false = f"**Nitro Code | Does Not Work :(**\n {output_code}"
                webhook_output_true = f"**Nitro Code | Works :)**\n {output_code}"
                
                #send request to API
                response = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{random_string}?with_application=true&with_subscription_plan=true")

                if response.status_code == 200:
                    webhook = DiscordWebhook(url=webhook_url, content=webhook_output_true)
                    webhook.execute()
                    break  # Stop the code after finding a working Nitro code
                else: # any other HTTP codes other than '200' will trigger this
                    webhook = DiscordWebhook(url=webhook_url, content=webhook_output_false)
                    webhook.execute()
            except Exception as e:
                print(f"Error generating Nitro codes: {e}\n") # outpts to terminal
                error_message = f"Error generating Nitro codes: {e}\n"
                webhook = DiscordWebhook(url=webhook_url, content=error_message)
                webhook.execute()
        
    def TokenChecker(webhook_url: str, Token: str):
        #required headers for API
        headers = {
            'Authorization': f'{Token}'
        }

        #send GET request to API
        response = requests.get(f"https://discord.com/api/v9/users/@me", headers=headers)

        if response.status_code == 200:
            content = "**Token Information**" + "\n" + "```" + response.text + "```" 
        else:  # any other HTTP codes other than '200' will trigger this
            content = f"**Error** ```{response.status_code} - {response.text}```"  

        webhook = DiscordWebhook(url=webhook_url, content=content)
        webhook.execute()

@app.post("/Webhook_Spam")
async def Execute_Spam(webhook: str, message: str, timeout: float):
    if not webhook or not message or timeout <= 0:
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    
    Spam = Thread(target=DiscordFunctions.WebhookSpam, args=(webhook, message, timeout))
    Spam.start()

    return {"message": "Webhook spamming has started!"}

@app.post("/Delete_Webhook")
async def Remove_Webhook(webhook: str):
    if not webhook:
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    
    Delete = Thread(target=DiscordFunctions.DeleteWebhook, args=(webhook,))
    Delete.start()

    return {"message": "Webhook has been deleted!"}

@app.post("/Token_Checker")
async def Token_Checker(webhook: str, Token: str):
    if not Token:
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    
    TokenChecker = Thread(target=DiscordFunctions.TokenChecker, args=(webhook, Token))
    TokenChecker.start()

    return {"message": "Token Validated!"}

@app.get("/Nitro_Generator")
async def Nitro_Generator(webhook: str):
    if not webhook:
        raise HTTPException(status_code=400, detail="Invalid input parameters.")
    
    Generate = Thread(target=DiscordFunctions.NitroGenerator, args=(webhook,))
    Generate.daemon = True
    Generate.start()

    return {"message": "Generating Nitro Codes!"}

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') # works on Linux and windows | This makes the terminal less cluttered 
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True) #runs on localhost at port 5000