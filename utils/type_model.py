TYPE = {
    "type1": ["REHM"],
    "type2": ["Holcim"],
    "type3": ["SEBA"],
    "type4": ["Baustoffen"],
    "type5": ["Altlasten", "BTSC"],
    "type6": ["KFN", "KEN"],
    "type7": ["Administration", "Disposition"],
    "type8": ["RZO"],
    "type9": ["HAURISEON"],
    "type10": ["Waage", "Waagschein"],
    "type11": ["Steine"],
    "type12": ["Entsorgung"]
}
TYPE_INFO = {
    "type1": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferscheinnummer", "Lieferscheinummer", "Lieferschelnnummer", "Lieterscheinnummer",
                            "Lleferschelnnummer", "Lleterscheinnummer"],
            "left": "t_left",
            "right": "t_right",
            "top": "t_top",
            "bottom": "t_bottom + t_height"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left - 2 * t_width",
            "right": "t_right + 2 * t_width",
            "top": "t_top",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Zeit", "Zelt"],
            "left": "t_left",
            "right": "t_right + 3 * t_width",
            "top": "t_top",
            "bottom": "t_bottom + 2 * t_height"
        },
        "Gewicht": {
            "search_word": ["Netto"],
            "left": "t_left",
            "right": "t_right + 3 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 5 * t_height"
        },
        "Volume": {
            "search_word": ["Menge"],
            "left": "t_left",
            "right": "t_right + 4 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 5 * t_height"
        }
    },
    "type2": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_right + 50",
            "right": "t_right + 2 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 10"
        },
        "DTS_Date": {
            "search_word": ["Datum", "Datum:"],
            "left": "t_right + 20",
            "right": "t_right + 10 * t_width",
            "top": "t_top - 15",
            "bottom": "t_bottom + 10"
        },
        "Gewicht": {
            "search_word": ["Menge", ".Menge"],
            "left": "t_left",
            "right": "t_right + t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + t_height"
        },
        "Volume": {
            "search_word": ["Menge", ".Menge"],
            "left": "t_left - 5",
            "right": "t_right + 1.5 * t_width",
            "top": "t_bottom + t_height",
            "bottom": "t_bottom + 4 * t_height"
        },
        "Fuhre": {
            "search_word": ["FUHRE"],
            "left": "t_right + 10",
            "right": "t_right + 2 * t_width",
            "top": "t_top - 20",
            "bottom": "t_bottom + 20"
        }
    },
    "type4": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_left - 50",
            "right": "t_right",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left - 20",
            "right": "t_right + 3 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Datum"],
            "left": "t_left - 20",
            "right": "t_right + t_width",
            "top": "t_bottom + 2 * t_height",
            "bottom": "t_bottom + 4 * t_height"
        },
        "Gewicht": {
            "search_word": ["Menge"],
            "left": "t_left - 20",
            "right": "t_right + t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 1.5 * t_height"
        },
        "Volume": {
            "search_word": ["Menge"],
            "left": "t_left - 20",
            "right": "t_right + t_width",
            "top": "t_bottom + 1.5 * t_height",
            "bottom": "t_bottom + 4 * t_height"
        }
    },
    "type5": {
        "Lieferschein_Nr": {
            "search_word": ["Bon"],
            "left": "t_right + t_width",
            "right": "t_right + 8 * t_width",
            "top": "t_top - 50",
            "bottom": "t_bottom - 5"
        },
        "DTS_Date": {
            "search_word": ["Zeit"],
            "left": "t_left - t_width",
            "right": "t_right + 8 * t_width",
            "top": "t_bottom - 20",
            "bottom": "t_bottom + 5 * t_height"
        },
        "Gewicht": {
            "search_word": ["Netto", "Natto"],
            "left": "t_left - 30",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom - 20",
            "bottom": "t_bottom + 3 * t_height"
        }
    },
    "type6": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_right + 60",
            "right": "t_right + 2 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 10"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_right + 10",
            "right": "t_right + 3 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 10"
        },
        "Gewicht": {
            "search_word": ["Nettogewicht", "Wettogewicht"],
            "left": "t_right",
            "right": "t_right + 3 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 5"
        }
    },
    "type7": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_left",
            "right": "t_right - 10",
            "top": "t_bottom",
            "bottom": "t_bottom + 4 * t_height"
        },
        "DTS_Date": {
            "search_word": ["Beladezeit", "Beladezelt"],
            "left": "t_left - 15",
            "right": "t_right + t_width",
            "top": "t_bottom + 10",
            "bottom": "t_bottom + 5 * t_height"
        },
        "Gewicht": {
            "search_word": ["Menge"],
            "left": "t_right",
            "right": "t_right + 5 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 10"
        },
        "Volume": {
            "search_word": ["Menge"],
            "left": "t_right",
            "right": "t_right + 5 * t_width",
            "top": "t_bottom + 8",
            "bottom": "t_bottom + 2 * t_height"
        }
    },
    "type7_B": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_left",
            "right": "t_right - 10",
            "top": "t_bottom",
            "bottom": "t_bottom + 4 * t_height"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left",
            "right": "t_right + 3 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 4 * t_height"
        },
        "Volume": {
            "search_word": ["M3"],
            "left": "t_left - 5 * t_width",
            "right": "t_right",
            "top": "t_bottom",
            "bottom": "t_bottom + 4 * t_height"
        }
    },
    "type8": {
        "Lieferschein_Nr": {
            "search_word": ["LIEFERSCHEIN"],
            "left": "t_right + 50",
            "right": "t_right + 2 * t_width",
            "top": "t_top - 2 * t_height",
            "bottom": "t_bottom + t_height"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Zeit", "Zelt"],
            "left": "t_left - 30",
            "right": "t_right + t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        },
        "Gewicht": {
            "search_word": ["NETTO"],
            "left": "t_left",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        }
    },
    "type9": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_right + 0.5 * t_width",
            "right": "t_right + 1.5 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 10"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_right + t_width",
            "right": "t_right + 5 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 5"
        },
        "DTS_Time": {
            "search_word": ["Beladezeit"],
            "left": "t_right + t_width",
            "right": "t_right + 3 * t_width",
            "top": "t_top - 5",
            "bottom": "t_bottom + 5"
        },
        "Gewicht": {
            "search_word": ["Menge"],
            "left": "t_left - 5",
            "right": "t_right + 5",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        }
    },
    "type10": {
        "Lieferschein_Nr": {
            "search_word": ["Waagschein", "aagschein", "laagschein", ".agschein"],
            "left": "t_right",
            "right": "t_right + t_width",
            "top": "t_top - t_height",
            "bottom": "t_bottom"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left - t_width",
            "right": "t_right",
            "top": "t_top",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Zeit"],
            "left": "t_left",
            "right": "t_right + 4 * t_width",
            "top": "t_top",
            "bottom": "t_bottom + 2 * t_height"
        },
        "Gewicht": {
            "search_word": ["Fahrzeugnummer"],
            "left": "t_left",
            "right": "t_right",
            "top": "t_bottom + 3 * t_height",
            "bottom": "t_bottom + 5 * t_height"
        }
    },
    "type11": {
        "Lieferschein_Nr": {
            "search_word": ["Recycling"],
            "left": "t_left - 40",
            "right": "t_right + 30",
            "top": "-2",
            "bottom": "t_top"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_left - 2 * t_width",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 3 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Zeit", "Zelt"],
            "left": "t_left - 2 * t_width",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 4 * t_height"
        },
        "Gewicht": {
            "search_word": ["Menge", "Mengė"],
            "left": "t_left - 1.5 * t_width",
            "right": "t_right + t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 3 * t_height"
        }
    },
    "type11_B": {
        "Lieferschein_Nr": {
            "search_word": ["Lieferschein"],
            "left": "t_right",
            "right": "t_right + t_width",
            "top": "-2",
            "bottom": "t_bottom + t_height"
        },
        "DTS_Date": {
            "search_word": ["Datum"],
            "left": "t_right",
            "right": "t_right + 4 * t_width",
            "top": "t_top - 20",
            "bottom": "t_bottom + 10"
        },
        "DTS_Time": {
            "search_word": ["Ladezeit"],
            "left": "t_left - 30",
            "right": "t_right",
            "top": "t_bottom",
            "bottom": "t_bottom + 3 * t_height"
        },
        "Volume": {
            "search_word": ["Menge"],
            "left": "t_left",
            "right": "t_right + t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        }
    },
    "type12": {
        "Lieferschein_Nr": {
            "search_word": ["Mulden"],
            "left": "t_right + t_width",
            "right": "t_right + 3 * t_width",
            "top": "t_top - 10",
            "bottom": "t_top + 10"
        },
        "DTS_Date": {
            "search_word": ["Datum", "Datumwe"],
            "left": "t_left - 10",
            "right": "t_right + 2 * t_width",
            "top": "t_bottom",
            "bottom": "t_bottom + 2 * t_height"
        },
        "DTS_Time": {
            "search_word": ["Tara"],
            "left": "t_right + 3.6 * t_width",
            "right": "t_right + 6 * t_width",
            "top": "t_top - 10",
            "bottom": "t_bottom + 5"
        },
        "Gewicht": {
            "search_word": ["Netto"],
            "left": "t_right + t_width",
            "right": "t_right + 3 * t_width",
            "top": "t_top - 5",
            "bottom": "t_bottom + 5"
        }
    }
}
