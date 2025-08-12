import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

class UdyamScraper:
    def __init__(self):
        self.base_url = "https://udyamregistration.gov.in/UdyamRegistration.aspx"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_form_schema(self):
        try:
            print("Fetching Udyam registration page...")
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            form_schema = {
                "step1": self.extract_step1_fields(soup),
                "step2": self.extract_step2_fields(soup),
                "validation_rules": self.extract_validation_rules(soup),
                "ui_components": self.extract_ui_components(soup)
            }
            
            with open('udyam_form_schema.json', 'w', encoding='utf-8') as f:
                json.dump(form_schema, f, indent=2, ensure_ascii=False)
            
            print("✅ Form schema extracted and saved to udyam_form_schema.json")
            return form_schema
            
        except Exception as e:
            print(f"❌ Error scraping form: {str(e)}")
            return None
    
    def extract_step1_fields(self, soup):
        """Extract Step 1 (Aadhaar) form fields"""
        step1_fields = []
        
        aadhaar_inputs = soup.find_all('input', {'id': re.compile(r'aadhaar|aadhar', re.I)})
        entrepreneur_inputs = soup.find_all('input', {'id': re.compile(r'entrepreneur|name', re.I)})
        
        
        for input_elem in aadhaar_inputs + entrepreneur_inputs:
            field_info = {
                "id": input_elem.get('id', ''),
                "name": input_elem.get('name', ''),
                "type": input_elem.get('type', 'text'),
                "placeholder": input_elem.get('placeholder', ''),
                "required": input_elem.get('required') is not None,
                "maxlength": input_elem.get('maxlength', ''),
                "pattern": input_elem.get('pattern', ''),
                "label": self.find_field_label(soup, input_elem)
            }
            step1_fields.append(field_info)
        
        return step1_fields
    
    def extract_step2_fields(self, soup):
        """Extract Step 2 (PAN) form fields"""
        step2_fields = []
        
        pan_inputs = soup.find_all('input', {'id': re.compile(r'pan|PAN', re.I)})
        
        for input_elem in pan_inputs:
            field_info = {
                "id": input_elem.get('id', ''),
                "name": input_elem.get('name', ''),
                "type": input_elem.get('type', 'text'),
                "placeholder": input_elem.get('placeholder', ''),
                "required": input_elem.get('required') is not None,
                "maxlength": input_elem.get('maxlength', ''),
                "pattern": input_elem.get('pattern', ''),
                "label": self.find_field_label(soup, input_elem)
            }
            step2_fields.append(field_info)
        
        return step2_fields
    
    def extract_validation_rules(self, soup):
        """Extract validation rules and patterns"""
        validation_rules = {
            "aadhaar": {
                "pattern": r"\d{12}",
                "description": "12-digit Aadhaar number"
            },
            "pan": {
                "pattern": r"[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}",
                "description": "PAN format: ABCDE1234F"
            },
            "otp": {
                "pattern": r"\d{6}",
                "description": "6-digit OTP"
            }
        }
        
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Extract PAN validation pattern
                pan_match = re.search(r'[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}', script.string)
                if pan_match:
                    validation_rules["pan"]["pattern"] = pan_match.group()
        
        return validation_rules
    
    def extract_ui_components(self, soup):
        """Extract UI components like dropdowns, buttons, etc."""
        ui_components = {
            "buttons": [],
            "dropdowns": [],
            "checkboxes": [],
            "radio_buttons": []
        }
        
        # Extract buttons
        buttons = soup.find_all('button') + soup.find_all('input', {'type': 'submit'})
        for btn in buttons:
            btn_info = {
                "id": btn.get('id', ''),
                "text": btn.get_text(strip=True) or btn.get('value', ''),
                "type": btn.get('type', 'button')
            }
            ui_components["buttons"].append(btn_info)
        
        # Extract dropdowns
        selects = soup.find_all('select')
        for select in selects:
            options = [opt.get_text(strip=True) for opt in select.find_all('option')]
            select_info = {
                "id": select.get('id', ''),
                "name": select.get('name', ''),
                "options": options
            }
            ui_components["dropdowns"].append(select_info)
        
        # Extract checkboxes
        checkboxes = soup.find_all('input', {'type': 'checkbox'})
        for cb in checkboxes:
            cb_info = {
                "id": cb.get('id', ''),
                "name": cb.get('name', ''),
                "checked": cb.get('checked') is not None
            }
            ui_components["checkboxes"].append(cb_info)
        
        return ui_components
    
    def find_field_label(self, soup, input_elem):
        """Find the label associated with an input field"""
        # Try to find label by for attribute
        input_id = input_elem.get('id')
        if input_id:
            label = soup.find('label', {'for': input_id})
            if label:
                return label.get_text(strip=True)
        
        # Try to find label by parent or sibling
        parent = input_elem.parent
        if parent:
            label = parent.find('label')
            if label:
                return label.get_text(strip=True)
        
        return ""

def main():
    scraper = UdyamScraper()
    schema = scraper.scrape_form_schema()
    
    if schema:
        print("\n📋 Extracted Form Schema Summary:")
        print(f"Step 1 Fields: {len(schema['step1'])}")
        print(f"Step 2 Fields: {len(schema['step2'])}")
        print(f"Validation Rules: {len(schema['validation_rules'])}")
        print(f"UI Components: {len(schema['ui_components']['buttons'])} buttons, {len(schema['ui_components']['dropdowns'])} dropdowns")
        
        print("\n🔍 Validation Rules Found:")
        for rule_name, rule_info in schema['validation_rules'].items():
            print(f"  {rule_name}: {rule_info['pattern']} - {rule_info['description']}")

if __name__ == "__main__":
    main() 