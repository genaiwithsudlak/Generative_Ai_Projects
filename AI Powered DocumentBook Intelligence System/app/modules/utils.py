
# small utility helpers
def print_preview(text, n=200):
    return text[:n] + ("..." if len(text) > n else "")
