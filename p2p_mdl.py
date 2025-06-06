import pandas as pd
from frozendict import frozendict
from copy import copy
import uuid
from pm4pymdl.objects.mdl.exporter import exporter as mdl_exporter


class Shared:
    TSTCT = {}
    EKBE_belnr_ebeln = {}
    EKPO_matnr_ebeln = {}
    EKPO_ebeln_banfn = {}
    EKPO_ebeln_ebelp = {}
    EKPO_objects = list()
    MSEG_mblnr_matnr = {}
    MSEG_mblnr_zeile = {}
    MSEG_mblnr_ebeln = {}
    MSEG_mblnr_ebeln_ebelp = {}
    MSEG_objects = list()
    RSEG_belnr_matnr = {}
    RSEG_belnr_ebeln_ebelp = {}
    RSEG_objects = list()
    BSEG_belnr_augbl = {}
    BSEG_belnr_buzei = {}
    BSEG_objects = list()
    MARA_objects = list()
    LFA1_objects = list()
    EBAN_events = {}
    EKKO_events = {}
    MKPF_events = {}
    RBKP_events = {}
    BKPF_events = {}
    events = []


def read_tstct():
    df = pd.read_csv("TSTCT.tsv", sep="\t", dtype={"SPRSL": str, "TCODE": str, "TTEXT": str})
    stream = df.to_dict('records')
    for el in stream:
        Shared.TSTCT[el["TCODE"]] = el["TTEXT"]


def get_activity(tcode):
    if tcode in Shared.TSTCT:
        return Shared.TSTCT[tcode]


def read_ekbe():
    df = pd.read_csv("EKBE.tsv", sep="\t", dtype={"EBELN": str, "EBELP": str, "BELNR": str})
    stream = df.to_dict('records')
    for el in stream:
        if str(el["BELNR"]).lower() != "nan":
            if not el["BELNR"] in Shared.EKBE_belnr_ebeln:
                Shared.EKBE_belnr_ebeln[el["BELNR"]] = set()
            Shared.EKBE_belnr_ebeln[el["BELNR"]].add(el["EBELN"])


def read_ekpo():
    df = pd.read_csv("EKPO.tsv", sep="\t",
                     dtype={"EBELN": str, "EBELP": str, "MATNR": str, "BANFN": str, "BNFPO": str, "NETPR": float,
                            "PEINH": float, "NETWR": float, "BTWR": float})
    stream = df.to_dict('records')
    for el in stream:
        if str(el["MATNR"]).lower() != "nan":
            if not el["MATNR"] in Shared.EKPO_matnr_ebeln:
                Shared.EKPO_matnr_ebeln[el["MATNR"]] = set()
            Shared.EKPO_matnr_ebeln[el["MATNR"]].add(el["EBELN"])
        if str(el["BANFN"]).lower() != "nan":
            if not el["EBELN"] in Shared.EKPO_ebeln_banfn:
                Shared.EKPO_ebeln_ebelp[el["EBELN"]] = set()
            Shared.EKPO_ebeln_ebelp[el["EBELN"]].add(el["BANFN"])
        if not el["EBELN"] in Shared.EKPO_ebeln_ebelp:
            Shared.EKPO_ebeln_ebelp[el["EBELN"]] = set()
        Shared.EKPO_ebeln_ebelp[el["EBELN"]].add(el["EBELN"] + "_" + el["EBELP"])
        Shared.EKPO_objects.append(
            {"object_id": el["EBELN"] + "_" + el["EBELP"], "object_type": "EBELN_EBELP", "object_matnr": el["MATNR"],
             "object_netpr": el["NETPR"], "object_peinh": el["PEINH"], "object_netwr": el["NETWR"],
             "object_brtwr": el["BRTWR"], "object_table": "EKPO", "object_ebeln": el["EBELN"],
             "object_ebelp": el["EBELP"]})
    print("read ekpo")


def read_mseg():
    df = pd.read_csv("MSEG.tsv", sep="\t",
                     dtype={"MBLNR": str, "ZEILE": str, "MATNR": str, "LIFNR": str, "KUNNR": str, "EBELN": str,
                            "EBELP": str})
    stream = df.to_dict('records')
    for el in stream:
        if str(el["MATNR"]).lower() != "nan":
            if not el["MBLNR"] in Shared.MSEG_mblnr_matnr:
                Shared.MSEG_mblnr_matnr[el["MBLNR"]] = set()
            Shared.MSEG_mblnr_matnr[el["MBLNR"]].add(el["MATNR"])
        if not el["MBLNR"] in Shared.MSEG_mblnr_zeile:
            Shared.MSEG_mblnr_zeile[el["MBLNR"]] = set()
        Shared.MSEG_mblnr_zeile[el["MBLNR"]].add(el["MBLNR"] + "_" + el["ZEILE"])
        if str(el["EBELN"]).lower() != "nan" and str(el["EBELP"]).lower() != "nan":
            if not el["MBLNR"] in Shared.MSEG_mblnr_ebeln:
                Shared.MSEG_mblnr_ebeln[el["MBLNR"]] = set()
            Shared.MSEG_mblnr_ebeln[el["MBLNR"]].add(el["EBELN"])
            if not el["MBLNR"] in Shared.MSEG_mblnr_ebeln_ebelp:
                Shared.MSEG_mblnr_ebeln_ebelp[el["MBLNR"]] = set()
            Shared.MSEG_mblnr_ebeln_ebelp[el["MBLNR"]].add(el["EBELN"] + "_" + el["EBELP"])
        Shared.MSEG_objects.append(
            {"object_id": el["MBLNR"] + "_" + el["ZEILE"], "object_type": "MBLNR_ZEILE", "object_matnr": el["MATNR"],
             "object_lifnr": el["LIFNR"], "object_kunnr": el["KUNNR"], "object_table": "MSEG",
             "object_mblnr": el["MBLNR"], "object_zeile": el["ZEILE"]})
    print("read mseg")


def read_rseg():
    df = pd.read_csv("RSEG.tsv", sep="\t",
                     dtype={"BELNR": str, "EBELN": str, "EBELP": str, "MATNR": str, "WRBTR": float})
    stream = df.to_dict('records')
    for el in stream:
        if str(el["MATNR"]).lower() != "nan":
            if not el["BELNR"] in Shared.RSEG_belnr_matnr:
                Shared.RSEG_belnr_matnr[el["BELNR"]] = set()
            Shared.RSEG_belnr_matnr[el["BELNR"]].add(el["MATNR"])
        if not el["BELNR"] in Shared.RSEG_belnr_ebeln_ebelp:
            Shared.RSEG_belnr_ebeln_ebelp[el["BELNR"]] = set()
        Shared.RSEG_belnr_ebeln_ebelp[el["BELNR"]].add(el["BELNR"] + "_" + el["EBELN"] + "_" + el["EBELP"])
        Shared.RSEG_objects.append(
            {"object_id": el["BELNR"] + "_" + el["EBELN"] + "_" + el["EBELP"], "object_type": "BELNR_EBELN_EBELP",
             "object_matnr": el["MATNR"], "object_wrbtr": el["WRBTR"], "object_table": "RSEG",
             "object_belnr": el["BELNR"], "object_ebeln": el["EBELN"], "object_ebelp": el["EBELP"],
             "object_ebeln_ebelp": el["EBELN"] + "_" + el["EBELP"]})
    print("read rseg")


def read_bseg():
    df = pd.read_csv("BSEG.tsv", sep="\t", dtype={"BELNR": str, "BUZEI": str, "AUGBL": str, "WRBTR": str})
    stream = df.to_dict("r")
    for el in stream:
        if str(el["AUGBL"]).lower() != "nan":
            if not el["BELNR"] in Shared.BSEG_belnr_augbl:
                Shared.BSEG_belnr_augbl[el["BELNR"]] = set()
            Shared.BSEG_belnr_augbl[el["BELNR"]].add(el["AUGBL"])
        if not el["BELNR"] in Shared.BSEG_belnr_buzei:
            Shared.BSEG_belnr_buzei[el["BELNR"]] = set()
        Shared.BSEG_belnr_buzei[el["BELNR"]].add(el["BELNR"] + "_" + el["BUZEI"])
        Shared.BSEG_objects.append(
            {"object_id": el["BELNR"] + "_" + el["BUZEI"], "object_type": "BELNR_BUZEI", "object_augbl": el["AUGBL"],
             "object_wrbtr": el["WRBTR"], "object_table": "BSEG", "object_belnr": el["BELNR"],
             "object_buzei": el["BUZEI"]})
    print("read bseg")


def read_mara():
    df = pd.read_csv("MARA.tsv", sep="\t",
                     dtype={"MATNR": str, "ERSDA": str, "ERNAM": str, "MBRSH": str, "MATKL": str, "NTGEW": str,
                            "VOLUMN": str, "TRAGR": str})
    # MATNR str
    # ERSDA str
    # ERNAM str
    # MBRSH str
    # MATKL str
    # NTGEW str
    # VOLUMN str
    # TRAGR str
    stream = df.to_dict("r")
    for el in stream:
        Shared.MARA_objects.append(
            {"object_id": el["MATNR"], "object_type": "MATNR", "object_table": "MARA", "object_ersda": el["ERSDA"],
             "object_mbrsh": el["MBRSH"], "object_matkl": el["MATKL"], "object_ntgew": el["NTGEW"],
             "object_volum": el["VOLUM"], "object_tragr": el["TRAGR"]})
    print("read mara")


def read_lfa1():
    df = pd.read_csv("LFA1.tsv", sep="\t", dtype={"LIFNR": str, "LAND1": str, "NAME1": str, "ORT01": str, "REGIO": str})
    stream = df.to_dict("r")
    for el in stream:
        Shared.LFA1_objects.append(
            {"object_id": el["LIFNR"], "object_type": "LIFNR", "object_table": "LFA1", "object_land1": el["LAND1"],
             "object_name1": el["NAME1"], "object_ort01": el["ORT01"], "object_regio": el["REGIO"]})
    print("read lfa1")


def read_eban():
    df = pd.read_csv("EBAN.tsv", sep="\t", dtype={"BANFN": str, "BNFPO": str, "ERNAM": str, "ERDAT": str, "MATNR": str})
    df["ERDAT"] = pd.to_datetime(df["ERDAT"], format="%d.%m.%Y", errors='coerce')
    stream = df.to_dict('records')
    for el in stream:
        if not el["BANFN"] in Shared.EBAN_events:
            Shared.EBAN_events[el["BANFN"]] = list()
        Shared.EBAN_events[el["BANFN"]].append({"event_activity": get_activity("ME51N"), "event_timestamp": el["ERDAT"],
                                                "event_table": "EBAN"})
        Shared.EBAN_events[el["BANFN"]] = sorted(Shared.EBAN_events[el["BANFN"]], key=lambda x: x["event_timestamp"])


def read_ekko():
    df = pd.read_csv("EKKO.tsv", sep="\t", dtype={"EBELN": str, "AEDAT": str, "ERNAM": str, "LIFNR": str})
    df["AEDAT"] = pd.to_datetime(df["AEDAT"], format="%d.%m.%Y", errors='coerce')
    stream = df.to_dict('records')
    for el in stream:
        if not el["EBELN"] in Shared.EKKO_events:
            Shared.EKKO_events[el["EBELN"]] = list()
        Shared.EKKO_events[el["EBELN"]].append(
            {"event_activity": get_activity("ME21N"), "event_timestamp": el["AEDAT"], "event_table": "EKKO"})
        Shared.EKKO_events[el["EBELN"]] = sorted(Shared.EKKO_events[el["EBELN"]], key=lambda x: x["event_timestamp"])


def read_mkpf():
    df = pd.read_csv("MKPF.tsv", sep="\t",
                     dtype={"MBLNR": str, "CPUDT": str, "CPUTM": str, "USNAM": str, "TCODE": str, "TCODE2": str})
    df["event_timestamp"] = df["CPUDT"] + " " + df["CPUTM"]
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], format="%d.%m.%Y %H:%M:%S", errors='coerce')
    stream = df.to_dict('records')
    for el in stream:
        if str(el["TCODE"]).lower() != "nan":
            if not el["MBLNR"] in Shared.MKPF_events:
                Shared.MKPF_events[el["MBLNR"]] = list()
            Shared.MKPF_events[el["MBLNR"]].append(
                {"event_activity": get_activity(el["TCODE"]), "event_timestamp": el["event_timestamp"],
                 "event_resource": el["USNAM"], "event_table": "MKPF"})
            Shared.MKPF_events[el["MBLNR"]] = sorted(Shared.MKPF_events[el["MBLNR"]],
                                                     key=lambda x: x["event_timestamp"])


def read_rbkp():
    df = pd.read_csv("RBKP.tsv", sep="\t", dtype={"BELNR": str, "USNAM": str, "TCODE": str, "CPUDT": str, "CPUTM": str})
    df["event_timestamp"] = df["CPUDT"] + " " + df["CPUTM"]
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], format="%d.%m.%Y %H:%M:%S", errors='coerce')
    stream = df.to_dict('records')
    for el in stream:
        if str(el["TCODE"]).lower() != "nan":
            if not el["BELNR"] in Shared.RBKP_events:
                Shared.RBKP_events[el["BELNR"]] = list()
            Shared.RBKP_events[el["BELNR"]].append(
                {"event_activity": get_activity(el["TCODE"]), "event_timestamp": el["event_timestamp"],
                 "event_resource": el["USNAM"], "event_table": "RBKP"})
            Shared.RBKP_events[el["BELNR"]] = sorted(Shared.RBKP_events[el["BELNR"]],
                                                     key=lambda x: x["event_timestamp"])


def read_bkpf():
    df = pd.read_csv("BKPF.tsv", sep="\t", dtype={"BELNR": str, "CPUDT": str, "CPUTM": str, "USNAM": str, "TCODE": str})
    rbkp_df = pd.read_csv("RBKP.tsv", sep="\t",
                          dtype={"BELNR": str, "USNAM": str, "TCODE": str, "CPUDT": str, "CPUTM": str})
    df = df[df["BELNR"].isin(rbkp_df["BELNR"])]
    df["event_timestamp"] = df["CPUDT"] + " " + df["CPUTM"]
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], format="%d.%m.%Y %H:%M:%S", errors='coerce')
    stream = df.to_dict('records')
    for el in stream:
        if str(el["TCODE"]).lower() != "nan":
            if not el["BELNR"] in Shared.BKPF_events:
                Shared.BKPF_events[el["BELNR"]] = list()
            Shared.BKPF_events[el["BELNR"]].append(
                {"event_activity": get_activity(el["TCODE"]), "event_timestamp": el["event_timestamp"],
                 "event_resource": el["USNAM"], "event_table": "BKPF"})
            Shared.BKPF_events[el["BELNR"]] = sorted(Shared.BKPF_events[el["BELNR"]],
                                                     key=lambda x: x["event_timestamp"])


def write_events():
    for evk in Shared.EBAN_events:
        evs = Shared.EBAN_events[evk]
        i = 0
        while i < len(evs):
            ev = evs[i]
            ev["event_id"] = str(uuid.uuid4())
            nev = copy(ev)
            nev["BANFN"] = evk
            Shared.events.append(nev)
            i = i + 1
    for evk in Shared.EKKO_events:
        evs = Shared.EKKO_events[evk]
        i = 0
        while i < len(evs):
            ev = evs[i]
            ev["event_id"] = str(uuid.uuid4())
            nev = copy(ev)
            nev["EBELN"] = evk
            Shared.events.append(nev)
            if i == 0:
                if evk in Shared.EKPO_ebeln_banfn:
                    for it in Shared.EKPO_ebeln_banfn[evk]:
                        nev = copy(ev)
                        nev["BANFN"] = it
                        Shared.events.append(nev)
                if evk in Shared.EKPO_ebeln_ebelp:
                    for it in Shared.EKPO_ebeln_ebelp[evk]:
                        nev = copy(ev)
                        nev["EBELN_EBELP"] = it
                        Shared.events.append(nev)
            if i == len(evs) - 1:
                if evk in Shared.EKBE_belnr_ebeln:
                    for doc in Shared.EKBE_belnr_ebeln[evk]:
                        nev = copy(ev)
                        nev["MBLNR"] = doc
                        Shared.events.append(nev)
            i = i + 1
    for evk in Shared.MKPF_events:
        evs = Shared.MKPF_events[evk]
        i = 0
        while i < len(evs):
            ev = evs[i]
            ev["event_id"] = str(uuid.uuid4())
            nev = copy(ev)
            nev["MBLNR"] = evk
            Shared.events.append(nev)
            if i == 0:
                """
                if evk in Shared.EKPO_matnr_ebeln:
                    for ord in Shared.EKPO_matnr_ebeln[evk]:
                        nev = copy(ev)
                        nev["EBELN"] = ord
                        Shared.events.append(nev)
                """
                if evk in Shared.MSEG_mblnr_ebeln:
                    for it in Shared.MSEG_mblnr_ebeln[evk]:
                        nev = copy(ev)
                        nev["EBELN"] = it
                        Shared.events.append(nev)
                if evk in Shared.MSEG_mblnr_ebeln_ebelp:
                    for it in Shared.MSEG_mblnr_ebeln_ebelp[evk]:
                        nev = copy(ev)
                        nev["EBELN_EBELP"] = it
                        Shared.events.append(nev)
                if evk in Shared.MSEG_mblnr_matnr:
                    for mat in Shared.MSEG_mblnr_matnr[evk]:
                        nev = copy(ev)
                        nev["MATNR"] = mat
                        Shared.events.append(nev)
                if evk in Shared.MSEG_mblnr_zeile:
                    for it in Shared.MSEG_mblnr_zeile[evk]:
                        nev = copy(ev)
                        nev["MBLNR_ZEILE"] = it
                        Shared.events.append(nev)
            i = i + 1
    for evk in Shared.RBKP_events:
        evs = Shared.RBKP_events[evk]
        i = 0
        while i < len(evs):
            ev = evs[i]
            ev["event_id"] = str(uuid.uuid4())
            nev = copy(ev)
            nev["BELNR"] = evk
            Shared.events.append(nev)
            if i == 0:
                if evk in Shared.RSEG_belnr_matnr:
                    for mat in Shared.RSEG_belnr_matnr[evk]:
                        nev = copy(ev)
                        nev["MATNR"] = mat
                        Shared.events.append(nev)
                if evk in Shared.RSEG_belnr_ebeln_ebelp:
                    for it in Shared.RSEG_belnr_ebeln_ebelp[evk]:
                        nev = copy(ev)
                        nev["BELNR_EBELN_EBELP"] = it
                        Shared.events.append(nev)
                        nev = copy(ev)
                        nev["EBELN_EBELP"] = it.split("_")[1] + "_" + it.split("_")[2]
                        Shared.events.append(nev)
                if evk in Shared.EKBE_belnr_ebeln:
                    for it in Shared.EKBE_belnr_ebeln[evk]:
                        nev = copy(ev)
                        nev["EBELN"] = it
                        Shared.events.append(nev)
            i = i + 1
    for evk in Shared.BKPF_events:
        evs = Shared.BKPF_events[evk]
        i = 0
        while i < len(evs):
            ev = evs[i]
            ev["event_id"] = str(uuid.uuid4())
            nev = copy(ev)
            nev["BELNR"] = evk
            Shared.events.append(nev)
            if i == 0:
                if evk in Shared.BSEG_belnr_augbl:
                    for it in Shared.BSEG_belnr_augbl[evk]:
                        nev = copy(ev)
                        nev["AUGBL"] = it
                        Shared.events.append(nev)
                if evk in Shared.BSEG_belnr_buzei:
                    for it in Shared.BSEG_belnr_buzei[evk]:
                        nev = copy(ev)
                        nev["BELNR_BUZEI"] = it
                        Shared.events.append(nev)
            i = i + 1


if __name__ == "__main__":
    read_bseg()
    read_tstct()
    read_eban()
    read_bkpf()
    read_ekbe()
    read_ekpo()
    read_mseg()
    read_rseg()
    read_mara()
    read_lfa1()
    read_ekko()
    read_mkpf()
    read_rbkp()
    write_events()
    Shared.events = sorted(Shared.events, key=lambda x: x["event_timestamp"])
    print("written events")
    events_df = pd.DataFrame(Shared.events)
    print("got dataframe")
    events_df.type = "exploded"
    ekpo_objects = pd.DataFrame(Shared.EKPO_objects)
    mseg_objects = pd.DataFrame(Shared.MSEG_objects)
    rseg_objects = pd.DataFrame(Shared.RSEG_objects)
    mara_objects = pd.DataFrame(Shared.MARA_objects)
    lfa1_objects = pd.DataFrame(Shared.LFA1_objects)
    object_df = pd.concat([ekpo_objects, mseg_objects, rseg_objects, mara_objects, lfa1_objects])
    print("exporting")
    mdl_exporter.apply(events_df, "log_p2p.mdl", obj_df=object_df)
    print("exported")
    mdl_exporter.apply(events_df, "log_p2p.parquet", obj_df=object_df)
