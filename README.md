# Anki Vocabulary Creator

A powerful Python script that automatically generates Anki flashcards with definitions, pronunciations, and audio from Cambridge Dictionary. Perfect for language learners, students, and anyone looking to build their vocabulary efficiently.

![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

## 🚀 Features

- **Automated Flashcard Creation**: Convert word lists into ready-to-use Anki decks
- **Rich Media Support**: Includes definitions, examples, pronunciations, and native speaker audio
- **Dual Card Types**: Generates both word→definition and definition→word cards for better retention
- **Batch Processing**: Process hundreds of words automatically in one go
- **Cambridge Dictionary Integration**: Fetches accurate definitions and high-quality audio pronunciations
- **Customizable**: Multiple output options and configuration settings
- **Error Handling**: Continues processing even if some words fail, with detailed error reporting
- **Duplicate Prevention**: Automatically skips words already in your deck

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 genanki
```

### 2. Download the Script
```bash
git clone https://github.com/yourusername/anki-vocabulary-creator.git
cd anki-vocabulary-creator
```

## 🛠 Quick Start

### 1. Create a Word List
Create a text file with your vocabulary words:
```bash
echo "serendipity
ephemeral
quintessential
melancholy
ubiquitous" > words.txt
```

### 2. Generate Anki Deck
```bash
python anki_vocabulary_creator.py words.txt
```

### 3. Import into Anki
- Open Anki
- Go to `File → Import`
- Select the generated `vocabulary_deck.apkg` file
- Start studying!

## 📖 Complete Usage

### Basic Command
```bash
python anki_vocabulary_creator.py words.txt
```

### Advanced Options
```bash
# Custom output filename
python anki_vocabulary_creator.py words.txt --output my_vocabulary.apkg

# Custom deck name
python anki_vocabulary_creator.py words.txt --deck-name "Advanced English Vocabulary"

# Disable audio for faster processing
python anki_vocabulary_creator.py words.txt --no-audio

# Adjust request delay (be respectful to servers)
python anki_vocabulary_creator.py words.txt --delay 2.5

# Use Oxford Dictionary instead of Cambridge
python anki_vocabulary_creator.py words.txt --dictionary oxford
```

### Full Command Reference
```bash
usage: anki_vocabulary_creator.py [-h] [--output OUTPUT] [--deck-name DECK_NAME]
                                 [--include-audio] [--delay DELAY]
                                 [--dictionary {cambridge,oxford}]
                                 input_file

Create Anki decks from word lists with definitions and audio

positional arguments:
  input_file            Text file containing words (one per line or space-separated)

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output .apkg filename (default: vocabulary_deck.apkg)
  --deck-name DECK_NAME, -n DECK_NAME
                        Name of the Anki deck (default: Vocabulary Deck)
  --include-audio, -a   Include audio pronunciations (default: True)
  --delay DELAY         Delay between requests in seconds (default: 2.0)
  --dictionary {cambridge,oxford}, -d {cambridge,oxford}
                        Dictionary source (default: cambridge)
```

## 📝 Input Format

Your input text file can contain words in several formats:

### One word per line:
```
serendipity
ephemeral
quintessential
```

### Space-separated words:
```
serendipity ephemeral quintessential melancholy ubiquitous
```

### Mixed content (script extracts words automatically):
```
I need to learn these words: serendipity, ephemeral, and quintessential.
Also practice: melancholy ubiquitous

New words for today:
- paradigm
- eloquent
- resilient
```

The script automatically:
- ✅ Extracts individual words
- ✅ Removes duplicates
- ✅ Converts to lowercase
- ✅ Handles punctuation and special characters

## 🎯 Output Structure

The script generates an Anki deck (.apkg file) with beautiful, functional cards:

### Card 1: Word → Definition
**Front:**
```
serendipity
/ˌser.ənˈdɪp.ə.ti/
[Audio Player]
```

**Back:**
```
Definition:
the fact of finding interesting or valuable things by chance

Example:
We met through a series of serendipitous events.

Source: Cambridge Dictionary
```

### Card 2: Definition → Word
**Front:**
```
Definition:
the fact of finding interesting or valuable things by chance
```

**Back:**
```
serendipity
/ˌser.ənˈdɪp.ə.ti/
[Audio Player]

Source: Cambridge Dictionary
```

## 🔧 Example Workflow

### 1. Prepare Your Word List
```bash
cat > academic_words.txt << EOF
perspective
facilitate
comprehensive
articulate
dilemma
paradigm
methodology
synthesize
criterion
hypothesis
EOF
```

### 2. Generate Anki Deck
```bash
python anki_vocabulary_creator.py academic_words.txt \
  --deck-name "Academic Vocabulary" \
  --output academic_cards.apkg \
  --delay 2.0
```

### 3. Import and Study
- Open Anki
- `File → Import` → Select `academic_cards.apkg`
- Your deck appears in the deck list
- Start studying with spaced repetition!

## 📊 Sample Output

When you run the script, you'll see real-time progress:

```bash
🎯 Found 28 unique words to process
📚 Using Cambridge Dictionary
🔊 Audio: Enabled
──────────────────────────────────────────────────
📖 Processing 1/28: serendipity
  ✅ Audio downloaded (14562 bytes)
  ✅ Added: serendipity
📖 Processing 2/28: ephemeral
  ✅ Audio downloaded (13891 bytes)
  ✅ Added: ephemeral
...
──────────────────────────────────────────────────
📊 SUMMARY
✅ Successfully added: 26 words
🔊 Audio files included: 24
❌ Failed: 2 words
📝 Failed words: obscure_term, technical_jargon
💾 Output file: vocabulary_deck.apkg
🎉 Deck generation complete! Import into Anki to start studying.
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError: No module named 'requests'"**
```bash
# Install required packages
pip install requests beautifulsoup4 genanki
```

**Audio files not playing in Anki**
- Ensure Anki is updated to the latest version
- Check that media files are enabled in Anki preferences
- Verify your system can play MP3 files
- Try importing a smaller deck first to test

**"Failed to fetch definition" errors**
- Check your internet connection
- Verify the word exists in Cambridge Dictionary
- Increase delay between requests: `--delay 3.0`
- Some very rare or technical words might not be found

**Rate limiting or connection issues**
- Increase the delay between requests: `--delay 3.0`
- Process smaller batches of words (50-100 at a time)
- Try during off-peak hours

**Some words fail to process**
- The script continues with other words if some fail
- Check the failed words list in the output summary
- Try processing failed words separately in a new run

### Debug Mode
For advanced troubleshooting, you can modify the script to enable debug output:

```python
# Add this at the beginning of main() function
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance & Limitations

### Performance Metrics
- **Processing Speed**: ~2-3 seconds per word (with audio)
- **Success Rate**: ~90-95% for common English words
- **Audio Availability**: ~85% of words have audio pronunciations
- **File Size**: ~1-2MB per 100 words (with audio included)

### Current Limitations
- Works best with common English vocabulary
- Audio may not be available for very rare words
- Requires internet connection for dictionary lookups
- Cambridge Dictionary is primary source (Oxford support experimental)


## 🔗 Alternative: MyVocabs.com Extension

If you're looking for a web-based solution to complement this tool, check out **[MyVocabs.com Chrome Extension](https://www.myvocabs.com/)**:

**MyVocabs.com Extension Features:**
- 📚 Save words from any website with one click
- 🎯 Create and organize vocabulary lists
- 🔊 Audio pronunciations
- 📖 Definitions and examples
- 🔄 Sync across devices
- 📊 Progress tracking
- 🎮 Interactive learning games

**How MyVocabs.com can help:**
1. Use the MyVocabs extension to collect words as you browse the web
2. Export your word lists from MyVocabs.com
3. Use this Python script to convert those word lists into Anki decks
4. Get the best of both worlds: easy word collection + powerful spaced repetition


## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

### How to Contribute
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Areas for Contribution
- Support for additional dictionaries
- Enhanced error handling and retry logic
- Additional card templates and styling
- Batch processing optimizations
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cambridge Dictionary** for providing free access to definitions and audio
- **Anki** for the incredible spaced repetition system that revolutionized learning
- **genanki library** for making Anki deck generation accessible in Python
- **MyVocabs.com** for providing a great web-based vocabulary collection tool
- **Contributors** and users who help improve this tool

## 🌟 Pro Tips

### For Best Results
1. **Group words by theme** (academic, business, medical, etc.)
2. **Process in batches** of 50-100 words for better reliability
3. **Include audio** for better pronunciation learning
4. **Use meaningful deck names** for organization
5. **Review failed words** and try them separately

### Integration Workflow
1. **Collect words** using the Chrome extension or MyVocabs.com
2. **Export your word lists** to text files
3. **Process with this script** to create Anki decks
4. **Study with Anki** using spaced repetition
5. **Track progress** and add new words regularly

## 🎓 Learning Science Behind This Tool

This tool leverages several proven learning techniques:

- **Spaced Repetition**: Anki's algorithm shows cards at optimal intervals
- **Dual Coding**: Combining text definitions with audio pronunciations
- **Active Recall**: Testing yourself with definition→word cards
- **Context Learning**: Example sentences provide real-world usage

### 📚 Example Use Cases

- **Students**: Build academic vocabulary for tests and studies
- **Professionals**: Learn industry-specific terminology
- **Language Learners**: Expand general vocabulary efficiently
- **Writers**: Improve word choice and expression
- **Readers**: Capture and learn new words from books

---

**Happy learning!** 🎓✨

*Transform your vocabulary learning with automated, science-backed flashcard creation!*

---
### 🔄 Complete Workflow Example

**Step 1: Collect Words**
- Use MyVocabs.com extension to save words from articles
- Or manually create a list from your reading

**Step 2: Export Words**
- Export from MyVocabs.com as text
- Or copy-paste from your notes

**Step 3: Generate Deck**
```bash
python anki_vocabulary_creator.py my_vocabulary.txt --deck-name "My Reading Vocabulary"
```

**Step 4: Study**
- Import into Anki
- Study daily with spaced repetition
- Watch your vocabulary grow!

Start building your vocabulary today with just a simple text file! 🚀
