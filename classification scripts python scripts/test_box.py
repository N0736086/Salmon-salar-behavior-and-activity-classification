from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

TOKEN = "NLidSRiNdSVkq5PiXLvftGQy92DnYMp9"

auth = BoxDeveloperTokenAuth(TOKEN)
client = BoxClient(auth)

me = client.users.get_user_me()

print("Connected to Box")
print("Name:", me.name)
print("Login:", me.login)
