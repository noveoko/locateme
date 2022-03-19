from collections import Counter
from random import choices
import multiprocessing
from time import time
import locale
locale.setlocale(locale.LC_ALL, '') 

PATH_TO_NAMES = 'usa_last_names.txt'
NEW_NAMES_TO_GENERATE = 100000

def naive_text_generation(path_to_file=PATH_TO_NAMES, new_names_to_generate=NEW_NAMES_TO_GENERATE):
    #start time
    start = time()
    """Generate names using really dumb algorithm"""
    real_last_names = set([a.strip() for a in open(path_to_file).read().split('\n') if a])
    generated_last_names = set()
    parts = generate_parts(real_last_names)
    ready_to_use = []
    for part in parts:
        part_strings = [a[0] for a in part]
        part_probs = [a[1] for a in part]
        ready_to_use.append([part_strings, part_probs])
    del(parts)
    ready_to_use = {a:ready_to_use[count] for count, a in enumerate(["start","mid","end"])}
    # random choice based on probability
    while len(generated_last_names) < new_names_to_generate:
        #use multiprocessing to speed up generation
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        result = pool.map(generate_name, [ready_to_use for _ in range(new_names_to_generate)])
        pool.close()
        pool.join()
        for name in result:
            generated_last_names.add(name)
        print("Generated {} names".format(len(generated_last_names)))
    else:
        #kill pool
        pool.terminate()
    #end time
    end = time()
    #add commas to long numbers in string

    print(f"Generated {len(generated_last_names):n} names in {end-start} seconds")
    #predict time to generate 1million names
    total_time = end-start
    time_for_1_million_records = total_time/len(generated_last_names)*1000000
    print(f"Predicted time to generate 1 million names: {time_for_1_million_records} seconds")
    return list(generated_last_names)

def generate_name(ready_to_use):
    name = []
    for part in ready_to_use:
        name.append(choices(ready_to_use[part][0], weights=ready_to_use[part][1], k=1)[0])
    return "".join(name).title()


def generate_parts(real_last_names):
    MIN_LEN = 2
    MAX_TOP = 9999
    START_INDEX = 3
    """Create a ton of tokens for name parts"""
    starts = [a[0:START_INDEX] for a in real_last_names]
    starts_top = Counter(starts).most_common(MAX_TOP)
    mids = [a for a in [a[START_INDEX:-START_INDEX] for a in real_last_names] if len(a) >= MIN_LEN]
    mids_top = Counter(mids).most_common(MAX_TOP*3)
    ends = [a[-START_INDEX:] for a in real_last_names]
    ends_top = Counter(ends).most_common(MAX_TOP)
    return (starts_top, mids_top, ends_top)

# real_last_names = set([a.strip() for a in open(PATH_TO_NAMES).read().split('\n') if a])
# parts = generate_parts(real_last_names)
# for part in parts:
#     print(part)



# print(f"Writing to file. Total: {len(fake_names)}")
# with open('fake_names.txt', 'w') as f:
#     for name in fake_names:
#         f.write(name + '\n')

if __name__ == '__main__':
    multiprocessing.freeze_support()
    fake_names = naive_text_generation()
    with open('generated_last_names.txt','w') as f:
        # chunks of 100 names each per line
        for i in range(0, len(fake_names), 100):
            f.write('|'.join(fake_names[i:i+100])+'\n')