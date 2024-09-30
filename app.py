import os
from flask import Flask, render_template, request, jsonify
import boto3
import json 

app = Flask(__name__)

bedrock_runtime = boto3.client('bedrock-runtime')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        try:
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-v2',
                body=json.dumps({
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": 300,
                    "temperature": 0.5,
                    "top_p": 1,
                    "stop_sequences": ["\n\nHuman:"]
                })
            )
            response_body = json.loads(response['body'].read())
            return jsonify({'response': response_body['completion']})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
