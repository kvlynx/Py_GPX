## Functions:

# Process extensions inside each point (to extract power, hr and cad)
def process_extensions(extensions):
    ext_data = {}
    for ext in extensions:
        tag_name = ext.tag.split('}')[-1]  # Extract tag name without namespace
        if 'TrackPointExtension' in tag_name:
            for child in list(ext):
                child_tag_name = child.tag.split('}')[-1]  # Extract child tag name without namespace
                ext_data[child_tag_name] = child.text
        else:
            if ext.text:
                ext_data[tag_name] = ext.text
            else:
                ext_data[tag_name] = {}
    return ext_data

# Create ditionaries of gpx points (having at the same level: lat, long, ele, power, hr, cad ...)
def create_dictionaries(gpx_data):
    point_dicts = []
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                time = point.time
                latitude = point.latitude
                longitude = point.longitude
                elevation = point.elevation if point.elevation is not None else None  # Handle missing elevation data

                extensions_data = process_extensions(point.extensions)

                point_dict = {
                    'time': time,
                    'latitude': latitude,
                    'longitude': longitude,
                    'elevation': elevation,
                    **extensions_data  # Include extension tags at the same level
                }
                point_dicts.append(point_dict)
    return point_dicts
