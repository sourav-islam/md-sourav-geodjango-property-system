from sentence_transformers import SentenceTransformer


_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> list[float]:
    model = get_model()
    return model.encode(text).tolist()


def embed_location(location) -> list[float]:
    text = location.name
    if location.address:
        text += f", {location.address}"
    return embed_text(text)


def embed_property(property_obj) -> list[float]:
    parts = [
        property_obj.title,
        property_obj.description,
        property_obj.property_type,
        property_obj.location.name,
        f"{property_obj.bedrooms} bedrooms",
        f"{property_obj.bathrooms} bathrooms",
    ]
    if property_obj.amenities:
        parts.append(", ".join(property_obj.amenities))
    return embed_text(" ".join(filter(None, parts)))
