"""Basic usage example."""

from phoebe_client import PhoebeClient

with PhoebeClient(host="localhost", port=8001) as client:
    print(f"Session: {client.phoebe.client_id}")

    client.set_value(twig='period@binary', value=1.5)
    client.set_value(twig='teff@primary', value=6000)

    period = client.get_value(twig='period@binary')
    print(f"Period: {period}")

    client.add_dataset(kind='lc', dataset='lc01', passband='Johnson:V')

    result = client.run_compute()
    print(f"Success: {result.get('success')}")
