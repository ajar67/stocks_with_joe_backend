import sys

def process_api_key(api_key):
    print('it got here take1')
    print(f"Received API Key: {api_key}")
    print("it got here take2")
    # Your processing logic here

if __name__ == '__main__':
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        process_api_key(api_key)
    else:
        print("No API key provided")