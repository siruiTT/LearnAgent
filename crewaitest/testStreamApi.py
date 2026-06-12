import requests
import json

# API 地址
url = "http://localhost:8000/chat"

# 请求数据
data = {
    "messages": [{"role": "user", "content": "你好，请介绍一下自己"}],
    "stream": True
}

# 发送 POST 请求，stream=True 接收流式响应
response = requests.post(url, json=data, stream=True)

# 逐行读取流式输出
for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        # SSE 格式：data: {...}
        if line_str.startswith('data: '):
            json_str = line_str[6:]  # 去掉 "data: " 前缀
            try:
                chunk = json.loads(json_str)
                # 提取内容
                delta = chunk['choices'][0]['delta']
                content = delta.get('content', '')
                finish_reason = chunk['choices'][0].get('finish_reason')

                if content:
                    print(content, end='', flush=True)
                if finish_reason:
                    print(f"\n\n[结束: {finish_reason}]")
            except json.JSONDecodeError:
                pass  # 忽略非 JSON 行