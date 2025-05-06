import json
from langmem.tool import LangMemTool

tool = LangMemTool(memory_file="server_memory.pkl")

with open("scripts/fake_hotel_reviews.json", "r") as f:
    reviews = json.load(f)

for review in reviews:
    metadata = {
        "hotel_id": review["hotel_id"],
        "hotel_name": review["hotel_name"],
        "location": review["location"],
        "hotel_url": review["hotel_url"]
    }
    comment = review["comment"]
    tags = review["tags"]

    tool.add_memory_object({
        "text": f"{review['hotel_name']} in {review['location']}:\n{comment}",
        "metadata": metadata,
        "tags": tags
    })

tool.save()
print("✅ Loaded hotel reviews.")
