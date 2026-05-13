def normalize_city(city: str) -> str:
    city = city.strip()

    # If user already provided country → respect it
    if "," in city:
        return city

    # Default assumption (based on your use case)
    return f"{city}, India"