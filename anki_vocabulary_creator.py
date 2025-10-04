import requests
from bs4 import BeautifulSoup
import genanki
import time
import re
import os
import tempfile
import hashlib
from typing import List, Dict, Optional
import argparse

class DictionaryScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_cambridge_definition(self, word: str) -> Optional[Dict]:
        """Get word definition from Cambridge Dictionary with audio"""
        try:
            url = f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the definition
            definition = ""
            definition_elem = soup.select_one('div.def.ddef_d.db')
            if definition_elem:
                definition = definition_elem.get_text().strip()
            
            if not definition:
                return None
            
            # Get pronunciation text
            pronunciation = ""
            pronunciation_elem = soup.select_one('span.pron.dpron')
            if pronunciation_elem:
                pronunciation = pronunciation_elem.get_text().strip()
            
            # Get example sentence
            example = ""
            example_elem = soup.select_one('div.examp.dexamp')
            if example_elem:
                example = example_elem.get_text().strip()
            
            # Get audio URL - Cambridge stores audio in data-src-mp3 attributes
            audio_url = None
            audio_elem = soup.select_one('source[type="audio/mpeg"]')
            if audio_elem:
                audio_url = audio_elem.get('src') or audio_elem.get('data-src-mp3')
            
            # Convert relative URL to absolute
            if audio_url:
                if audio_url.startswith('//'):
                    audio_url = f"https:{audio_url}"
                elif audio_url.startswith('/'):
                    audio_url = f"https://dictionary.cambridge.org{audio_url}"
            
            return {
                'word': word,
                'definition': definition,
                'pronunciation': pronunciation,
                'example': example,
                'source': 'Cambridge',
                'audio_url': audio_url
            }
            
        except Exception as e:
            print(f"Error fetching Cambridge definition for {word}: {e}")
            return None
    
    def download_audio(self, audio_url: str, word: str) -> Optional[bytes]:
        """Download audio and return as bytes"""
        if not audio_url:
            return None
            
        try:
            headers = {
                'Referer': 'https://dictionary.cambridge.org/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = self.session.get(audio_url, headers=headers)
            response.raise_for_status()
            
            # Check if we actually got audio data
            if response.content and len(response.content) > 1000:
                return response.content
            else:
                print(f"  ! Audio file too small or empty")
                return None
                
        except Exception as e:
            print(f"Error downloading audio for {word}: {e}")
            return None

class AnkiDeckCreator:
    def __init__(self, deck_name: str):
        self.deck_name = deck_name
        self.model = self.create_model()
        self.deck = genanki.Deck(
            abs(hash(deck_name)) % (10**8),
            deck_name
        )
        self.media_map = {}  # filename -> data mapping
    
    def create_model(self) -> genanki.Model:
        """Create a custom note model for vocabulary cards with audio"""
        return genanki.Model(
            abs(hash(self.deck_name)) % (10**8),
            'Vocabulary Model with Audio',
            fields=[
                {'name': 'Word'},
                {'name': 'Definition'},
                {'name': 'Pronunciation'},
                {'name': 'Example'},
                {'name': 'Source'},
                {'name': 'Audio'},
            ],
            templates=[
                {
                    'name': 'Card 1 - Word to Definition',
                    'qfmt': '''
                        <div style="text-align: center; font-family: Arial;">
                            <div style="font-size: 28px; font-weight: bold; margin: 20px 0;">
                                {{Word}}
                            </div>
                            {{#Pronunciation}}
                            <div style="font-size: 18px; color: #666; margin: 10px 0;">
                                /{{Pronunciation}}/
                            </div>
                            {{/Pronunciation}}
                            {{Audio}}
                        </div>
                    ''',
                    'afmt': '''
                        {{FrontSide}}
                        <hr style="margin: 20px 0;">
                        <div style="font-family: Arial;">
                            <div style="font-size: 18px; margin: 15px 0;">
                                <strong>Definition:</strong><br>
                                {{Definition}}
                            </div>
                            {{#Example}}
                            <div style="font-size: 16px; margin: 15px 0; font-style: italic; color: #444; border-left: 3px solid #ccc; padding-left: 10px;">
                                <strong>Example:</strong><br>
                                {{Example}}
                            </div>
                            {{/Example}}
                            <div style="font-size: 12px; color: #888; margin-top: 25px;">
                                Source: {{Source}}
                            </div>
                        </div>
                    ''',
                },
                {
                    'name': 'Card 2 - Definition to Word',
                    'qfmt': '''
                        <div style="font-family: Arial;">
                            <div style="font-size: 18px; margin: 15px 0;">
                                <strong>Definition:</strong><br>
                                {{Definition}}
                            </div>
                            {{#Example}}
                            <div style="font-size: 16px; margin: 15px 0; font-style: italic; color: #444; border-left: 3px solid #ccc; padding-left: 10px;">
                                <strong>Example:</strong><br>
                                {{Example}}
                            </div>
                            {{/Example}}
                        </div>
                    ''',
                    'afmt': '''
                        {{FrontSide}}
                        <hr style="margin: 20px 0;">
                        <div style="text-align: center; font-family: Arial;">
                            <div style="font-size: 28px; font-weight: bold; margin: 20px 0;">
                                {{Word}}
                            </div>
                            {{#Pronunciation}}
                            <div style="font-size: 18px; color: #666; margin: 10px 0;">
                                /{{Pronunciation}}/
                            </div>
                            {{/Pronunciation}}
                            {{Audio}}
                            <div style="font-size: 12px; color: #888; margin-top: 25px;">
                                Source: {{Source}}
                            </div>
                        </div>
                    ''',
                },
            ],
            css='''
                .card {
                    font-family: Arial;
                    margin: 20px;
                }
                audio {
                    width: 100%;
                    max-width: 300px;
                    margin: 15px 0;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
            '''
        )
    
    def add_note(self, word_data: Dict):
        """Add a note to the deck"""
        audio_field = ""
        
        if word_data.get('audio_data'):
            # Create a safe filename
            safe_word = re.sub(r'[^\w\-_]', '_', word_data['word'].lower())
            audio_filename = f"{safe_word}.mp3"
            audio_field = f'[sound:{audio_filename}]'
            
            # Store in media map
            self.media_map[audio_filename] = word_data['audio_data']
        
        note = genanki.Note(
            model=self.model,
            fields=[
                word_data['word'],
                word_data['definition'],
                word_data.get('pronunciation', ''),
                word_data.get('example', ''),
                word_data.get('source', ''),
                audio_field
            ]
        )
        self.deck.add_note(note)
    
    def save_deck(self, filename: str):
        """Save the deck to an .apkg file with media"""
        package = genanki.Package(self.deck)
        
        # Add media files using the correct approach
        if self.media_map:
            # Create temporary directory for media files
            with tempfile.TemporaryDirectory() as temp_dir:
                media_paths = []
                for audio_filename, audio_data in self.media_map.items():
                    temp_path = os.path.join(temp_dir, audio_filename)
                    with open(temp_path, 'wb') as f:
                        f.write(audio_data)
                    media_paths.append(temp_path)
                
                # Assign media files to package
                package.media_files = media_paths
                package.write_to_file(filename)
        else:
            package.write_to_file(filename)
        
        print(f"Deck saved as {filename}")
        print(f"Media files included: {len(self.media_map)}")

def read_word_list(filename: str) -> List[str]:
    """Read words from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            words = re.findall(r'\b[a-zA-Z]+\b', content)
            return list(set([word.lower() for word in words]))
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Create Anki deck from word list with audio pronunciations')
    parser.add_argument('input_file', help='Text file containing words')
    parser.add_argument('--output', '-o', default='vocabulary_deck.apkg', 
                       help='Output .apkg filename')
    parser.add_argument('--deck-name', '-n', default='Vocabulary Deck',
                       help='Name of the Anki deck')
    parser.add_argument('--include-audio', '-a', action='store_true', default=True,
                       help='Include audio pronunciations (default: True)')
    parser.add_argument('--delay', type=float, default=2.0,
                       help='Delay between requests in seconds (default: 2.0)')
    
    args = parser.parse_args()
    
    # Read words from file
    words = read_word_list(args.input_file)
    if not words:
        print("No words found in the input file.")
        return
    
    print(f"Found {len(words)} unique words.")
    
    # Initialize components
    scraper = DictionaryScraper()
    deck_creator = AnkiDeckCreator(args.deck_name)
    
    successful = 0
    failed = []
    audio_successful = 0
    
    # Process each word
    for i, word in enumerate(words, 1):
        print(f"Processing {i}/{len(words)}: {word}")
        
        word_data = scraper.get_cambridge_definition(word)
        
        if word_data:
            # Download audio if requested and available
            if args.include_audio and word_data.get('audio_url'):
                print(f"  Fetching audio from: {word_data['audio_url']}")
                audio_data = scraper.download_audio(word_data['audio_url'], word)
                if audio_data:
                    word_data['audio_data'] = audio_data
                    audio_successful += 1
                    print(f"  ✓ Audio downloaded ({len(audio_data)} bytes)")
                else:
                    print(f"  ✗ Audio download failed")
                    word_data['audio_data'] = None
            else:
                word_data['audio_data'] = None
            
            deck_creator.add_note(word_data)
            successful += 1
            print(f"  ✓ Added: {word}")
        else:
            failed.append(word)
            print(f"  ✗ Failed to get definition for: {word}")
        
        # Be respectful to the servers
        time.sleep(args.delay)
    
    # Save the deck
    deck_creator.save_deck(args.output)
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total words processed: {len(words)}")
    print(f"Successfully added: {successful} words")
    print(f"Audio files included: {audio_successful}")
    print(f"Failed: {len(failed)} words")
    if failed:
        print(f"Failed words: {', '.join(failed)}")

if __name__ == "__main__":
    main()
