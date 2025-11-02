"""Explicit session management example."""

from phoebe_client import PhoebeClient

client = PhoebeClient(host="localhost", port=8001)

try:
    session = client.create_session()
    print(f"Session ID: {session['client_id']}")
    
    client.set_value(twig='period@binary', value=2.5)
    result = client.save_bundle()
    
    if result.get('success'):
        bundle = result['result']['bundle']
        with open('my_bundle.phoebe', 'w') as f:
            f.write(bundle)
    
finally:
    client.close_session()
