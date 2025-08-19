from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import openai
import os

news_bp = Blueprint('news', __name__)

def extract_text_from_url(url):
    """Extract text content from a news URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find the main content
        content_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            'main',
            '.main-content'
        ]
        
        content = None
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text()
                break
        
        if not content:
            content = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract title
        title_elem = soup.find('title')
        title = title_elem.get_text().strip() if title_elem else "خبر کا عنوان"
        
        return title, content
        
    except Exception as e:
        raise Exception(f"URL سے خبر نکالنے میں خرابی: {str(e)}")

def generate_news_analysis_mock(title, content):
    """Generate mock news analysis for testing"""
    return {
        "lower_thirds": [
            "سندھ طاس معاہدہ: بھارت کا 'فرار'؟",
            "ہیگ عدالت کا فیصلہ: بھارت نے مسترد کیا",
            "پانی کا تنازع: پاکستان کا موقف کیا ہے؟",
            "معاہدے کی خلاف ورزی: عالمی قانون کی پامالی؟",
            "آبی وسائل: علاقائی استحکام پر اثرات",
            "پاکستان کا دعویٰ: 'پانی کا ایک قطرہ بھی نہیں چھین سکتے'",
            "بھارت کا ردعمل: 'عدالت کا دائرہ اختیار نہیں'",
            "مستقبل کے تعلقات: پانی کا تنازع کتنا اہم؟"
        ],
        "questions": [
            "سندھ طاس معاہدے کی تاریخی اہمیت کیا ہے اور اس کے موجودہ تنازع پر کیا اثرات مرتب ہو سکتے ہیں؟",
            "بھارت کی جانب سے ہیگ عدالت کے فیصلے کو مسترد کرنے کے عالمی قانونی اور سفارتی مضمرات کیا ہیں؟",
            "پاکستان کے آبی وسائل پر اس تنازع کے ممکنہ طویل مدتی اثرات کیا ہو سکتے ہیں؟",
            "کیا اس تنازع کا علاقائی امن و استحکام پر کوئی اثر پڑے گا؟",
            "دونوں ممالک کے درمیان پانی کے تنازع کو حل کرنے کے لیے کون سے سفارتی راستے اختیار کیے جا سکتے ہیں؟",
            "کیا یہ تنازع دونوں ممالک کے درمیان دیگر دوطرفہ تعلقات کو مزید خراب کر سکتا ہے؟",
            "عالمی برادری اس تنازع میں کیا کردار ادا کر سکتی ہے؟",
            "پاکستان اور بھارت کے درمیان پانی کے مسئلے پر مستقبل میں تعاون کے کیا امکانات ہیں؟"
        ],
        "analysis": {
            "lt_selection": "لوئر تھرڈز کا انتخاب خبر کے مرکزی نکات کو اجاگر کرنے کے لیے کیا گیا ہے، جن میں بھارت کا ہیگ عدالت کے فیصلے کو مسترد کرنا، سندھ طاس معاہدے کی اہمیت، اور پاکستان کے موقف کو شامل کیا گیا ہے۔",
            "question_importance": "پینل کے سوالات خبر کے مختلف پہلوؤں، جیسے تاریخی، سیاسی، اور مستقبل کے اثرات کو زیر بحث لانے کے لیے ڈیزائن کیے گئے ہیں۔",
            "observations": "اس خبر میں کئی اہم سیاسی اور سفارتی پہلو نمایاں ہیں۔ بھارت کا ہیگ عدالت کے فیصلے کو مسترد کرنا عالمی قانون اور بین الاقوامی معاہدوں کے احترام کے حوالے سے سوالات اٹھاتا ہے۔",
            "professional_standards": "اس تجزیے میں غیر جانبداری کو برقرار رکھنے کی کوشش کی گئی ہے، اور تمام دعوے خبر میں موجود حقائق پر مبنی ہیں۔"
        }
    }

def generate_news_analysis(title, content):
    """Generate news analysis using OpenAI or mock data"""
    try:
        # For now, return mock data to test the functionality
        # Later this can be replaced with actual OpenAI API calls
        return generate_news_analysis_mock(title, content)
        
        # Uncomment below for actual OpenAI integration
        """
        client = openai.OpenAI()
        
        prompt = f'''
آپ ایک پروفیشنل صحافی، نیوز اینالسٹ، اور کرنٹ افیئرز پروگرام پروڈیوسر ہیں۔ دی گئی خبر کے لیے مکمل تجزیہ تیار کریں:

خبر کا عنوان: {title}
خبر کا متن: {content}

براہ کرم مندرجہ ذیل فارمیٹ میں جواب دیں:

LOWER_THIRDS:
1. [پہلا LT]
2. [دوسرا LT]
3. [تیسرا LT]
4. [چوتھا LT]
5. [پانچواں LT]
6. [چھٹا LT]
7. [ساتواں LT]
8. [آٹھواں LT]

QUESTIONS:
1. [پہلا سوال]
2. [دوسرا سوال]
3. [تیسرا سوال]
4. [چوتھا سوال]
5. [پانچواں سوال]
6. [چھٹا سوال]
7. [ساتواں سوال]
8. [آٹھواں سوال]

LT_SELECTION:
[LTs کے انتخاب کی وضاحت]

QUESTION_IMPORTANCE:
[سوالات کی اہمیت کی وضاحت]

OBSERVATIONS:
[مشاہدات اور پہلو]

PROFESSIONAL_STANDARDS:
[پروفیشنل معیار اور غیر جانبداری]
'''

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "آپ ایک ماہر اردو صحافی اور نیوز اینالسٹ ہیں۔"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        analysis_text = response.choices[0].message.content
        return parse_analysis_response(analysis_text)
        """
        
    except Exception as e:
        # Return mock data if AI fails
        return generate_news_analysis_mock(title, content)

def parse_analysis_response(text):
    """Parse the AI response into structured data"""
    try:
        result = {
            "lower_thirds": [],
            "questions": [],
            "analysis": {
                "lt_selection": "",
                "question_importance": "",
                "observations": "",
                "professional_standards": ""
            }
        }
        
        # Extract Lower Thirds
        lt_match = re.search(r'LOWER_THIRDS:(.*?)(?=QUESTIONS:|$)', text, re.DOTALL)
        if lt_match:
            lt_text = lt_match.group(1).strip()
            lts = re.findall(r'\d+\.\s*(.+)', lt_text)
            result["lower_thirds"] = [lt.strip() for lt in lts if lt.strip()]
        
        # Extract Questions
        q_match = re.search(r'QUESTIONS:(.*?)(?=LT_SELECTION:|$)', text, re.DOTALL)
        if q_match:
            q_text = q_match.group(1).strip()
            questions = re.findall(r'\d+\.\s*(.+)', q_text)
            result["questions"] = [q.strip() for q in questions if q.strip()]
        
        # Extract Analysis sections
        sections = {
            "lt_selection": r'LT_SELECTION:(.*?)(?=QUESTION_IMPORTANCE:|$)',
            "question_importance": r'QUESTION_IMPORTANCE:(.*?)(?=OBSERVATIONS:|$)',
            "observations": r'OBSERVATIONS:(.*?)(?=PROFESSIONAL_STANDARDS:|$)',
            "professional_standards": r'PROFESSIONAL_STANDARDS:(.*?)$'
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result["analysis"][key] = match.group(1).strip()
        
        return result
        
    except Exception as e:
        # Fallback parsing if regex fails
        return generate_news_analysis_mock("", "")

@news_bp.route('/summarize', methods=['POST'])
def summarize_news():
    """Main endpoint for news summarization"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "کوئی ڈیٹا نہیں ملا"}), 400
        
        input_type = data.get('type')
        content = data.get('content')
        
        if not input_type or not content:
            return jsonify({"error": "براہ کرم خبر کا متن یا لنک داخل کریں"}), 400
        
        if input_type == 'url':
            try:
                title, news_content = extract_text_from_url(content)
                sources = [{"name": "خبر کا ذریعہ", "url": content}]
            except Exception as e:
                return jsonify({"error": f"URL سے خبر نکالنے میں خرابی: {str(e)}"}), 400
        else:
            title = "خبر کا عنوان"
            news_content = content
            sources = []
        
        # Generate analysis
        analysis_result = generate_news_analysis(title, news_content)
        
        response = {
            "title": title,
            "sources": sources,
            "lower_thirds": analysis_result["lower_thirds"],
            "questions": analysis_result["questions"],
            "analysis": analysis_result["analysis"]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"تجزیہ تیار کرنے میں خرابی: {str(e)}"}), 500

@news_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to check if API is working"""
    return jsonify({"message": "API is working!", "status": "success"})

