"""Basic usage example."""

from phoebe_client import PhoebeClient

with PhoebeClient(host="localhost", port=8001) as client:
    print(f"Session: {client.phoebe.session_id}")

    client.set_value(qualifier='period', component='binary', kind='orbit', context='component', value=1.5)
    client.set_value(qualifier='teff', component='primary', kind='star', context='component', value=6000)

    period = client.get_value(qualifier='period', component='binary', kind='orbit', context='component')
    print(f"Period: {period}")

    client.add_dataset(kind='lc', dataset='lc01', passband='Johnson:V', compute_times=[0., 0.5, 1.0])

    result = client.run_compute()
    print(f"Success: {result.get('success')}")
