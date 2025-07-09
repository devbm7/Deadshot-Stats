import google.generativeai as genai
import streamlit as st
from PIL import Image
import json
import re
from typing import Dict, List, Optional, Any
import os

# Configure Gemini API
def configure_gemini(api_key: str):
    """Configure the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)

def extract_data_from_image(image: Image.Image, api_key: str) -> Dict[str, Any]:
    """
    Extract structured data from a gaming screenshot using Gemini API.
    
    Args:
        image: PIL Image object
        api_key: Gemini API key
    
    Returns:
        Dictionary containing extracted data
    """
    try:
        # Configure Gemini
        configure_gemini(api_key)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create the prompt for structured data extraction
        prompt = """
        Analyze this gaming screenshot and extract the following information in JSON format:
        
        {
            "players": [
                {
                    "player_name": "string (exact player name as shown in the image)",
                    "kills": number,
                    "deaths": number,
                    "assists": number (if available),
                    "score": number,
                    "weapon": "string",
                    "ping": number (if visible),
                    "coins": number (if visible)
                }
            ],
            "game_mode": "string (Team/FFA)",
            "map_name": "string (if visible)",
            "match_length": number (in minutes, if visible),
            "extraction_confidence": "high/medium/low"
        }
        
        Important notes:
        - Extract player names EXACTLY as they appear in the image, including case sensitivity
        - Common player names in this system include: DevilOHeaven, MaXiMus22, Heet63, Alice, Bob, Charlie, David
        - Only extract information that is clearly visible in the image
        - For missing data, use null values
        - If you can't determine game mode, default to "FFA"
        - If you can't determine map, use null
        - If you can't determine match length, use null
        - Be conservative with confidence levels
        - Return ONLY the JSON object, no additional text
        """
        
        # Generate content from image
        response = model.generate_content([prompt, image])
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            extracted_data = json.loads(json_str)
            return extracted_data
        else:
            # If no JSON found, try to parse the entire response
            try:
                extracted_data = json.loads(response_text)
                return extracted_data
            except json.JSONDecodeError:
                st.error("Failed to parse Gemini API response as JSON")
                return {"error": "Failed to parse response", "raw_response": response_text}
                
    except Exception as e:
        st.error(f"Error extracting data from image: {str(e)}")
        return {"error": str(e)}

def validate_extracted_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate the extracted data and return any errors.
    
    Args:
        data: Extracted data dictionary
    
    Returns:
        List of validation error messages
    """
    errors = []
    
    if "error" in data:
        errors.append(f"Extraction error: {data['error']}")
        return errors
    
    if "players" not in data:
        errors.append("No player data found in the image")
        return errors
    
    if not isinstance(data["players"], list):
        errors.append("Player data must be a list")
        return errors
    
    if len(data["players"]) == 0:
        errors.append("No players found in the image")
        return errors
    
    # Validate each player
    for i, player in enumerate(data["players"]):
        if not isinstance(player, dict):
            errors.append(f"Player {i+1} data must be a dictionary")
            continue
        
        required_fields = ["player_name", "kills", "deaths", "score"]
        for field in required_fields:
            if field not in player:
                errors.append(f"Player {i+1} missing required field: {field}")
        
        # Validate numeric fields
        numeric_fields = ["kills", "deaths", "score"]
        for field in numeric_fields:
            if field in player and player[field] is not None:
                if not isinstance(player[field], (int, float)) or player[field] < 0:
                    errors.append(f"Player {i+1} {field} must be a non-negative number")
    
    return errors

def format_extracted_data_for_display(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the extracted data for display in the Streamlit interface.
    
    Args:
        data: Raw extracted data
    
    Returns:
        Formatted data for display
    """
    if "error" in data:
        return data
    
    formatted_data = {
        "game_mode": data.get("game_mode", "FFA"),
        "map_name": data.get("map_name"),
        "match_length": data.get("match_length"),
        "players": []
    }
    
    for player in data.get("players", []):
        # Clean up player name - remove extra whitespace and common artifacts
        player_name = player.get("player_name", "")
        if player_name:
            player_name = player_name.strip()
            # Remove common artifacts that might be extracted
            player_name = player_name.replace("Player", "").strip()
            # Handle specific player names that might have artifacts
            if player_name.lower() in ["deviloheaven", "devil", "heaven"]:
                player_name = "DevilOHeaven"
            elif player_name.lower() in ["maximus22", "maximus", "max"]:
                player_name = "MaXiMus22"
            elif player_name.lower() in ["heet63", "heet", "63"]:
                player_name = "Heet63"
            elif not player_name:
                player_name = "Unknown Player"
        
        formatted_player = {
            "player_name": player_name,
            "kills": player.get("kills", 0),
            "deaths": player.get("deaths", 0),
            "assists": player.get("assists"),
            "score": player.get("score", 0),
            "weapon": player.get("weapon", "AK47"),
            "ping": player.get("ping"),
            "coins": player.get("coins", 0),
            "team": None  # Will be set based on game mode
        }
        formatted_data["players"].append(formatted_player)
    
    return formatted_data

def get_extraction_confidence(data: Dict[str, Any]) -> str:
    """
    Get the confidence level of the extraction.
    
    Args:
        data: Extracted data
    
    Returns:
        Confidence level string
    """
    if "error" in data:
        return "error"
    
    return data.get("extraction_confidence", "low") 