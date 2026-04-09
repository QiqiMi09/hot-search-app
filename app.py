from flask import Flask, render_template, jsonify, request
import requests
import os
import openai

app = Flask(__name__)
ai_content_cache = {}

# DeepSeek API Key and Base URL
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Initialize Doubao client (compatible with OpenAI SDK)
import sys # Added this import

# Initialize DeepSeek client (compatible with OpenAI SDK)
# We initialize deepseek_client only if DEEPSEEK_API_KEY is available
deepseek_client = None

# Ensure API keys are set before proceeding
if not DEEPSEEK_API_KEY:
    print("Error: DEEPSEEK_API_KEY environment variable is not set. Exiting.")
    sys.exit(1) # Exit immediately if key is missing

if not TIANAPI_KEY:
    print("Error: TIANAPI_API_KEY environment variable is not set. Exiting.")
    sys.exit(1) # Exit immediately if key is missing

deepseek_client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL, timeout=60.0)

# Test DeepSeek API key validity on startup
try:
    test_response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=1
    )
    print("DeepSeek API key is valid.")
except openai.APIStatusError as e:
    print(f"Error: DeepSeek API key is invalid or API call failed: {e}")
    print("Please check your DeepSeek API key and ensure it has the necessary permissions.")
    sys.exit(1) # Exit if API key test fails
except Exception as e:
    print(f"An unexpected error occurred while testing DeepSeek API key: {e}")
    sys.exit(1) # Exit for other unexpected errors during key test
except openai.APIStatusError as e:
    print(f"Error: DeepSeek API key is invalid or API call failed: {e}")
    print("Please check your DeepSeek API key and ensure it has the necessary permissions.")
except Exception as e:
    print(f"An unexpected error occurred while testing DeepSeek API key: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hot_searches')
def get_hot_searches():
    try:
        # Construct the API URL for Tianapi Weibo Hot Search
        tianapi_url = f"https://apis.tianapi.com/weibohot/index?key={TIANAPI_KEY}"
        response = requests.get(tianapi_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        if data['code'] == 200 and 'list' in data['result']:
            hot_searches = []
            for i, item in enumerate(data['result']['list']):
                # Use 'hotword' for title and assign a rank
                hot_searches.append({'id': i + 1, 'title': item['hotword'], 'rank': i + 1})
            return jsonify(hot_searches)
        else:
            print(f"Error fetching hot searches from Tianapi: {data.get('msg', 'Unknown error')}")
            # Fallback to mock data if Tianapi call fails or returns empty
            return jsonify(get_mock_hot_searches())
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Tianapi: {e}")
        # Fallback to mock data if there's a connection error
        return jsonify(get_mock_hot_searches())
    except Exception as e:
        print(f"An unexpected error occurred while fetching hot searches: {e}")
        return jsonify(get_mock_hot_searches())

def get_mock_hot_searches():
    # NOTE: Reverted to mock data after real APIs proved unreliable.
    return [
        {'id': 1, 'title': '热搜新闻标题1：震惊！某地发现稀有古生物化石，揭秘地球生命演化新篇章', 'rank': 1},
        {'id': 2, 'title': '热搜新闻标题2：科技巨头发布划时代AI芯片，算力飙升千倍，或将引领新工业革命', 'rank': 2},
        {'id': 3, 'title': '热搜新闻标题3：国际影星出席环保峰会，呼吁全球关注气候变化，身体力行倡导绿色生活', 'rank': 3},
        {'id': 4, 'title': '全国多地迎来赏花热潮，春日美景如画，吸引游客纷至沓来', 'rank': 4},
        {'id': 5, 'title': '深度解析：新一代电动汽车技术突破，续航里程大幅提升，充电时间缩短一半', 'rank': 5},
        {'id': 6, 'title': '文化遗产数字化保护取得新进展，古籍文物“活”起来，公众可在线沉浸式体验', 'rank': 6},
        {'id': 7, 'title': '体育赛事爆冷！黑马选手一鸣惊人，力克卫冕冠军，创造历史', 'rank': 7},
        {'id': 8, 'title': '健康生活新风尚：专家建议多吃蔬菜水果，适量运动，保持良好作息', 'rank': 8},
        {'id': 9, 'title': '金融市场波动加剧，投资者关注全球经济走势，理性分析规避风险', 'rank': 9},
        {'id': 10, 'title': '教育改革新举措： STEAM课程融入中小学课堂，培养学生创新实践能力', 'rank': 10},
    ]

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Missing title'}), 400

    print(f"Attempting to generate content for title: {title}")
    print(f"DeepSeek client initialized with API key: {'sk-' + deepseek_client.api_key[30:] if deepseek_client.api_key else 'None'}") # Mask part of the key for security

    # Check cache first
    if title in ai_content_cache:
        print(f"Returning cached content for title: {title}")
        return jsonify({'text': ai_content_cache[title], 'image_url': ""})

    try:
        # Generate text content using DeepSeek's deepseek-chat model
        text_prompt = f"请根据以下新闻标题，用100字左右生成一段富有吸引力的图文描述：\n\n{title}"
        print(f"Sending text generation request to DeepSeek model: deepseek-chat")
        chat_completion = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": text_prompt}]
        )
        generated_text = chat_completion.choices[0].message.content
        print(f"Text generation successful. Generated text length: {len(generated_text)}")

        # Store in cache
        ai_content_cache[title] = generated_text

        # Image generation is disabled as per user request.
        image_url = ""
        print("Image generation skipped.")

        return jsonify({'text': generated_text, 'image_url': image_url})
    except openai.APIStatusError as e:
        print(f"Error: DeepSeek API call failed with status {e.status_code}: {e.response}")
        return jsonify({'error': f'AI生成内容失败: API调用失败 ({e.status_code})'}), 500
    except openai.APIConnectionError as e:
        print(f"Error: DeepSeek API connection failed: {e}")
        return jsonify({'error': 'AI生成内容失败: 连接到DeepSeek API服务器失败，请检查网络或API Key配置'}), 500
    except openai.APITimeoutError as e:
        print(f"Error: DeepSeek API request timed out: {e}")
        return jsonify({'error': 'AI生成内容失败: 请求超时，请稍后重试。'}), 500
    except Exception as e:
        print(f"An unexpected error occurred during AI content generation: {e}")
        return jsonify({'error': f'AI生成内容失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
