import asyncio
import json
import MoodMusic.skeleton as skeleton
import music.importer as importer
from lib.cortex import Cortex

def update_stats(stats, data):
    stats[0] = data['met'][1]
    stats[1] = data['met'][3]
    stats[2] = data['met'][6]
    stats[3] = data['met'][8]
    stats[4] = data['met'][10]
    stats[5] = data['met'][12]

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

def recommend(net, stats, songs, outputs):
    feeling_index = net.get_output_index(stats)
    feeling = outputs[feeling_index]
    print("--------------------------------------------")
    print("\nI believe you are feeling", feeling, flush=True)
    recommendation = importer.getRandom(songs[feeling_index])
    print("I recommend:", recommendation, flush=True)
    return feeling

def querySatisfaction(feeling):
    satisfied = input("...\nDo you like your recommendation? (Yes/No) ").strip().lower()
    if satisfied[0] is 'n':
        return input("How are you really feeling? (Choose one)\n"
                     "(Angry|Excited|Focused|Happy|Relaxed|Sad)|Pass|Quit\n").strip().lower()
    if satisfied[0] is 'q':
        return satisfied[0]
    return feeling
    
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
        outputs = skeleton.getDefaultOutputs()
        net = skeleton.getNetwork()
        songs = importer.importFiles()
        
        # update head
        count = update_stats(stats, json.loads(await cortex.get_data()))
        
        feeling = querySatisfaction(recommend(net, stats, songs, outputs))
        while feeling[0] is not 'q':
            if feeling[0] is not 'p':
                skeleton.superlearn(net, stats, skeleton.fixer(feeling, skeleton.getDefaultOutputs()))
                count = update_stats(stats, json.loads(await cortex.get_data()))

            feeling = querySatisfaction(recommend(net, stats, songs, outputs))
        await cortex.close_session()
    else:
        print("Failed to connect to headset", flush=True)


def main():
    print("Starting...", flush=True)
    cortex = Cortex('./cortex_creds')
    asyncio.run(connect(cortex))
    print("CLOSING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    cortex.close()


if __name__ == '__main__':
    main()
