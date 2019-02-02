def get_hour_bucket_from_slot(slot):
    slot_hour_tuple = list()
    slot_hour_tuple.append(int(slot[0].split(':')[0]))
    slot_hour_tuple.append(int(slot[1].split(':')[0]))
    return slot_hour_tuple