from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth
)

TOKEN = "jdxJKJ0pzquMbDS97QLF8U3b2r6YTj3Q"

auth = BoxDeveloperTokenAuth(TOKEN)
client = BoxClient(auth)

outfile = open(
    "box_tree.txt",
    "w",
    encoding="utf-8"
)

def walk(folder_id, path=""):

    items = client.folders.get_folder_items(
        folder_id
    )

    for item in items.entries:

        current_path = (
            f"{path}/{item.name}"
        )

        if item.type == "folder":

            line = (
                f"[DIR]  {current_path}"
            )

            print(line)
            outfile.write(line + "\n")

            walk(
                item.id,
                current_path
            )

        else:

            line = (
                f"[FILE] {current_path}"
            )

            print(line)
            outfile.write(line + "\n")

print("Building tree...")

walk("0")

outfile.close()

print(
    "\nSaved: box_tree.txt"
)
