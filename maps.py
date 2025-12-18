import overpy

def near_by_hospitals(location,radius = 500):
    api = overpy.Overpass()

    (lat, lon) = location
    query = f"""
    [out:json];
    node(around:{radius},{lat},{lon})[amenity=hospital];
    out;
    """
    result = api.query(query)
    return result.nodes
    # for node in result.nodes:
    #     name = node.tags.get("name", "Unnamed Hospital")
    #     phone = node.tags.get("phone") or node.tags.get("contact:phone", "Not available")
    #     website = node.tags.get("website") or node.tags.get("contact:website", "Not available")
    #     print(f"{name}\n  Phone: {phone}\n  Website: {website}\n")

# near_by_hospitals(location=(17.385044, 78.486671))
