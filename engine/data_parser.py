def load_equip_slots():
    path = os.path.join(GAME_DATA_DIR, "EquipSlotCategory.csv")
    slots = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)
        header = next(reader)
        next(reader)

        log(f"[PARSER] EquipSlot headers: {header}")

        for row in reader:
            try:
                key = int(row[0])

                detected = None

                for i in range(1, len(row)):
                    if row[i] == "1":
                        col = header[i].lower()

                        # MUCH STRONGER MATCHING
                        if "main" in col:
                            detected = "weapon"
                        elif "off" in col:
                            detected = "offhand"
                        elif "head" in col:
                            detected = "head"
                        elif "body" in col:
                            detected = "body"
                        elif "hand" in col or "glove" in col:
                            detected = "hands"
                        elif "leg" in col:
                            detected = "legs"
                        elif "foot" in col:
                            detected = "feet"
                        elif "ear" in col:
                            detected = "earrings"
                        elif "neck" in col:
                            detected = "necklace"
                        elif "wrist" in col:
                            detected = "bracelet"
                        elif "finger" in col or "ring" in col:
                            detected = "ring"

                if detected:
                    slots[key] = detected
                else:
                    log(f"[SLOT WARNING] Unknown slot mapping for key {key}")

            except Exception as e:
                log(f"[SLOT ERROR] {e}")

    log(f"[PARSER] Slot mappings loaded: {len(slots)}")
    return slots
