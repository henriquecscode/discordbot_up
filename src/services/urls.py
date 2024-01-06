from services.utils.faculties import Faculty
def get_base_url(faculty:Faculty):
    return f"https://sigarra.up.pt/{faculty.value}/pt"