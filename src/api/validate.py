from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

def validate_s3_connection(bucket_name, aws_access_key_id, aws_secret_access_key):
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3.head_bucket(Bucket=bucket_name)
        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/api/validate-connection', methods=['POST'])
def validate_connection():
    data = request.json
    bucket_name = data.get('bucket_name')
    aws_access_key_id = data.get('aws_access_key_id')
    aws_secret_access_key = data.get('aws_secret_access_key')

    if not bucket_name or not aws_access_key_id or not aws_secret_access_key:
        return jsonify({"error": "Missing required parameters"}), 400

    valid, error_message = validate_s3_connection(bucket_name, aws_access_key_id, aws_secret_access_key)
    if valid:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)