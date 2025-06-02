import re
from collections import defaultdict

def load_music_works(file_location):
    """Extract music work details from a CSV file into a structured format."""
    with open(file_location, 'r', encoding='utf-8') as f:
        text = f.read()

    # Define a regex pattern to capture fields from each CSV entry
    field_pattern = re.compile(
        r'(?P<title>[^\n;]+);'  # Work title
        r'(?P<summary>"(?:[^"]|"")*"|[^;]+);'  # Summary or description
        r'(?P<year>\d+);'  # Creation year
        r'(?P<era>[^;]+);'  # Historical era
        r'(?P<artist>[^;]+);'  # Artist(s)
        r'(?P<duration>\d{2}:\d{2}:\d{2});'  # Length of the work
        r'(?P<work_id>O\d+)'  # Unique identifier
    )

    # Process each entry and store in a list
    work_records = []
    for record in field_pattern.finditer(text):
        work_entry = record.groupdict()
        work_entry['title'] = work_entry['title'].strip()  # Trim whitespace from title
        work_records.append(work_entry)

    return work_records

def fetch_ordered_artists(file_location):
    """Retrieve a list of unique artists, sorted alphabetically."""
    works = load_music_works(file_location)
    
    # Gather all artists, accounting for multiple artists per work
    artist_list = {artist.strip() for work in works for artist in work['artist'].split(',')}
    
    return sorted(artist_list)

def compute_era_distribution(file_location):
    """Calculate the number of works in each historical era."""
    works = load_music_works(file_location)
    
    # Tally works by era
    era_tally = defaultdict(int)
    for work in works:
        era_tally[work['era']] += 1
    
    return dict(era_tally)

def group_titles_by_era(file_location):
    """Organize work titles by era, with titles sorted alphabetically."""
    works = load_music_works(file_location)
    
    # Group titles by era
    era_titles = defaultdict(list)
    for work in works:
        era = work['era'].strip()
        title = work['title'].strip()
        if era and title:  # Ensure fields are not empty
            era_titles[era].append(title)
    
    # Sort titles within each era
    for era in era_titles:
        era_titles[era].sort()
    
    return dict(era_titles)

# Demonstration of functionality
if __name__ == "__main__":
    data_file = '/home/bart/Desktop/PL2025-A104350/TPC2/obras.csv'
    
    # Display sorted artists
    artists = fetch_ordered_artists(data_file)
    print("=== Lista de Artistas (Ordem Alfabética) ===")
    for idx, artist in enumerate(artists, 1):
        print(f"{idx}. {artist}")
    
    # Display distribution of works by era
    era_dist = compute_era_distribution(data_file)
    print("\n=== Número de Obras por Era ===")
    for era, num_works in sorted(era_dist.items()):
        print(f"Era: {era}, Obras: {num_works}")
    
    # Display titles grouped by era
    titles_by_era = group_titles_by_era(data_file)
    print("\n=== Títulos de Obras por Era ===")
    for era in sorted(titles_by_era.keys()):
        print(f"\nEra: {era}")
        for idx, title in enumerate(titles_by_era[era], 1):
            print(f"  {idx}. {title}")