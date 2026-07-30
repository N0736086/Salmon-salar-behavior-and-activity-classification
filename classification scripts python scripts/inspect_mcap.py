# inspect_mcap.py

from mcap.reader import make_reader

with open("sample.mcap", "rb") as f:

    reader = make_reader(f)

    print("\nChannels\n")

    for schema, channel, message in reader.iter_decoded_messages():

        print(channel.topic)

        break
