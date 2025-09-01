# CRED Conversation Analysis Tool

A Python tool for analyzing CRED customer service conversations using a local OpenChat API to assess agent performance across multiple parameters.

## Features

- **Multiple Assessment Types**: Analyzes conversations for:
  - Opening protocols (greeting, introduction, customer confirmation)
  - Closing protocols (feedback requests, proper endings)
  - Reassurance statements
  - Hold procedures
  - Further assistance offers

- **Local API Integration**: Works with your local OpenChat API
- **Robust Error Handling**: Includes retry mechanisms for failed API calls
- **Flexible Processing**: Can process all conversations or sample subsets
- **CSV Output**: Saves results in organized CSV files with timestamps

## Prerequisites

- Python 3.8 or higher
- Local OpenChat API running at `http://192.168.30.239:8000/chat`
- CRED Excel file with conversation data

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your data**:
   - Create a `data` directory in the project root
   - Place your CRED Excel file (`TAReport (30).xlsx`) in the `data` directory
   - Ensure the Excel file has sheets named "Transcript" and "Primary Info"

## Configuration

Edit `config.py` to customize settings:

```python
# API settings
OPENCHAT_API_URL = "http://192.168.30.239:8000/chat"
OPENCHAT_MODEL = "openchat/openchat-3.5-1210"

# File paths
CRED_DATA_PATH = "./data"
CRED_FILE_NAME = "TAReport (30).xlsx"

# Processing settings
REQUEST_TIMEOUT = 60
RETRY_DELAY = 2  # seconds between API calls
```

## Usage

### 1. Test the Setup

First, test that everything is working:

```bash
python test_api.py
```

This will test:
- API connection
- JSON extraction
- Single conversation processing

### 2. Run the Analysis

```bash
python main.py
```

The script will:
1. Test API connectivity
2. Load your conversation data
3. Ask for processing options:
   - Process all conversations
   - Process sample (first 5)
   - Process custom number
4. Run all assessments
5. Save results to CSV files

### 3. Output Files

Results are saved in the `results/` directory with timestamps:
- `opening_results_YYYYMMDD_HHMMSS.csv`
- `closing_results_YYYYMMDD_HHMMSS.csv`
- `reassurance_results_YYYYMMDD_HHMMSS.csv`
- `hold_results_YYYYMMDD_HHMMSS.csv`
- `further_assistance_results_YYYYMMDD_HHMMSS.csv`
- `combined_results_YYYYMMDD_HHMMSS.csv`

## Project Structure

```
Check_DATA/
├── config.py              # Configuration settings
├── api_client.py          # OpenChat API client
├── data_loader.py         # Excel data loading and processing
├── prompts.py             # Assessment prompts and guidelines
├── processor.py           # Conversation processing logic
├── main.py               # Main execution script
├── test_api.py           # API testing script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── data/                # Place your Excel file here
│   └── TAReport (30).xlsx
└── results/             # Output CSV files (created automatically)
```

## Assessment Parameters

### 1. Opening Assessment
Checks if the agent:
- Greets the customer appropriately
- Introduces themselves with their name
- Confirms the customer's name

### 2. Closing Assessment
Checks if the agent:
- Asks for further assistance
- Requests feedback
- Transfers call for feedback
- Closes with proper greetings

### 3. Reassurance Assessment
Checks if the agent provides reassuring statements to customers.

### 4. Hold Assessment
Checks if the agent properly requests to put customers on hold.

### 5. Further Assistance Assessment
Checks if the agent offers additional help.

## Troubleshooting

### API Connection Issues
- Ensure your OpenChat API is running at the configured URL
- Check if the API is accessible via curl:
  ```bash
  curl http://192.168.30.239:8000/chat -H "Content-Type: application/json" -d '{"model": "openchat/openchat-3.5-1210", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello"}], "max_tokens": 100, "temperature": 0}'
  ```

### Data Loading Issues
- Ensure the Excel file is in the `data/` directory
- Check that sheet names match: "Transcript" and "Primary Info"
- Verify the file format is `.xlsx`

### Processing Issues
- Start with a small sample (option 2) to test
- Check the console output for specific error messages
- Ensure your API can handle the conversation length

## Customization

### Adding New Assessment Types
1. Add new guidelines to `prompts.py`
2. Create a new prompt following the existing pattern
3. Add the prompt to `ASSESSMENT_PROMPTS` dictionary
4. The processor will automatically handle the new assessment type

### Modifying Assessment Criteria
Edit the guidelines in `prompts.py` to adjust what constitutes "Met" vs "Not Met" for each assessment type.

## Support

If you encounter issues:
1. Run `python test_api.py` to diagnose problems
2. Check the console output for error messages
3. Verify your API is running and accessible
4. Ensure your data file is properly formatted

## License

This project is for internal use at CRED. 