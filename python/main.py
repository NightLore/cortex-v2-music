import asyncio
import json
from lib.cortex import Cortex

def update_stats(stats, data, count):
    new_count = count + 1
    stats[0] = (stats[0] * count + data['met'][1]) / new_count
    stats[1] = (stats[1] * count + data['met'][3]) / new_count
    stats[2] = (stats[2] * count + data['met'][6]) / new_count
    stats[3] = (stats[3] * count + data['met'][8]) / new_count
    stats[4] = (stats[4] * count + data['met'][10]) / new_count
    stats[5] = (stats[5] * count + data['met'][12]) / new_count
    return new_count

def print_data(data):
    print("Data:", data)
    print("Met:", data['met'])
    print("Engagement:", data["met"][1])
    print("Excitement:", data["met"][3])
    print("Long-term Excitement:", data["met"][4])
    print("Stress:", data["met"][6])
    print("Relaxation:", data["met"][8])
    print("Interest:", data["met"][10])
    print("Focus:", data["met"][12])

async def connect(cortex):
    print("Loading Cortex", flush=True)
    # await cortex.inspectApi()
    await cortex.get_user_login()
    await cortex.get_cortex_info()
    await cortex.has_access_right()
    await cortex.request_access()
    await cortex.authorize(debit=10000)
    await cortex.get_license_info()
    print("Connecting to headset...", flush=True)
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("Headset connected", flush=True)
        await cortex.create_session(activate=True,
                                    headset_id=cortex.headsets[0])
        await cortex.create_record(title="test record 1")
        await cortex.subscribe(['met'])
        
        stats = [0, 0, 0, 0, 0, 0]
        count = 0
        #while input().strip() is not "q":
        data = json.loads(await cortex.get_data())
        print_data(data)
        count = update_stats(stats, data, count)
        await cortex.close_session()
    else:
        print("Failed to connect to headset", flush=True)


def run():
    print("Starting...", flush=True)
    cortex = Cortex('./cortex_creds')
    asyncio.run(connect(cortex))
    print("CLOSING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    cortex.close()


if __name__ == '__main__':
    run()
