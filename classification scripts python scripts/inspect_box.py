# inspect_box.py

from boxsdk import Client, OAuth2

TOKEN = "BYDPwij9tQPa62uet0W2LScBOrdQ8J4L"

auth = OAuth2(
    client_id="wa7xe9pk9vk9z16q0wwza9ngcbkpp9c2",
    client_secret="TpKfUC9MTNRmQBKDlVDO3DHM4JN0r7oP",
    access_token=TOKEN
)

client = Client(auth)

root = client.folder(folder_id="0")

def walk(folder, level=0):

    print("  " * level + f"[DIR] {folder.name}")

    items = folder.get_items(limit=1000)

    for item in items:

        if item.type == "folder":

            walk(
                client.folder(item.id),
                level + 1
            )

        else:

            print(
                "  " * (level + 1)
                + f"[FILE] {item.name}"
            )

walk(root)
