from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth

TOKEN = "NLidSRiNdSVkq5PiXLvftGQy92DnYMp9"

FOLDER_ID = "353082741274"

auth = BoxDeveloperTokenAuth(TOKEN)
client = BoxClient(auth)

items = client.folders.get_folder_items(
    FOLDER_ID,
    limit=1000
)

for item in items.entries:
    print(
        f"{item.type:10}  {item.id}  {item.name}"
    )
