#!/usr/bin/env python
# coding: utf-8

def getPrevah():   
    prevah_map = {
                "lus-code": ["albedo", "CanopyHeight", "LeafAreaIndex", "CanopyDirectThroughfall", "Landuse_class"],
                 1: [0.4,  0,   0,   1,    "Water"],
                 2: [0.16, 0,   0,   1,    "Settlements"],
                 3: [0.16, 10,  5.5, 0.72, "Coniferous forest"],
                 4: [0.14, 10,  5.1, 0.73, "Decidous forest"],
                 5: [0.15, 10,  5.3, 0.72, "Mixed forest"],
                 6: [0.25, 0,   3.6, 1,    "Cereals"],
                 7: [0.17, 0,   0,   1,    "Pasture"],
                 8: [0.15, 0,   2.1, 1,    "Bush"],
                18: [0.16, 0,   8.7, 1,    "Fruit"],
                19: [0.22, 0.2, 3.6, 0.95, "Vegetables"],
                20: [0.2,  0.5, 3.6, 0.95, "Wheat"],
                21: [0.22, 0,   0,   1,    "Alpine vegetation"],
                22: [0.13, 0,   0,   1,    "Wetland"],
                23: [0.2,  0,   0,   1,    "Rough pasture"],
                24: [0.25, 0,   0,   1,    "Subalpine meadow"],
                11: [0.15, 0,   0,   1,    "Road"],
                13: [0.5,  0,   0,   1,    "Firn"],
                14: [0.4,  0,   0,   1,    "Bare ice"],
                15: [0.35, 0,   0,   1,    "Rock"],
                25: [0.2,  0,   0,   1,    "Alpine meadow"],
                26: [0.2,  0,   0,   1,    "Bare soil vegetation"],
                28: [0.14, 0.7, 3.6, 0.9,  "Corn"],
                29: [0.13, 0.7, 0.1, 0.9,  "Grapes"]
                }
    return prevah_map


def getModis(version):
    if version == 17:        
        modis_map = {
                        "Land Use Category": ["Roughness Length", "Land Use Description"],
                        0:  [0.06,  "Water"],
                        1:  [0.04,  "Evergreen Needleleaf Forest"],
                        2:  [0.05,  "Evergreen Broadleaf Forest"],
                        3:  [0.04,  "Deciduous Needleleaf Forest"],
                        4:  [0.04,  "Deciduous Broadleaf Forest"],
                        5:  [0.04,  "Mixed Forests"],
                        6:  [0.03,  "Closed Shrublands"],
                        7:  [0.03,  "Open Shrublands"],
                        8:  [0.03,  "Woody Savannas"],
                        9:  [0.03,  "Savannas"],
                        10: [0.03,  "Grasslands"],
                        11: [0.055, "Permanent Wetlands"],
                        12: [0.04,  "Croplands"],
                        13: [0.03,  "Urban and Built-Up"],
                        14: [0.04,  "Cropland/Natural Vegetation Mosaic"],
                        15: [0.05,  "Snow and Ice"],
                        16: [0.02,  "Barren or Sparsely Vegetated"]
                    }        
    elif version == 20:        
        modis_map = {
                        "Land Use Category": ["Roughness Length", "Land Use Description"],
                        1:  [0.04,  "Evergreen Needleleaf Forest"],
                        2:  [0.05,  "Evergreen Broadleaf Forest"],
                        3:  [0.04,  "Deciduous Needleleaf Forest"],
                        4:  [0.04,  "Deciduous Broadleaf Forest"],
                        5:  [0.04,  "Mixed Forests"],
                        6:  [0.03,  "Closed Shrublands"],
                        7:  [0.03,  "Open Shrublands"],
                        8:  [0.03,  "Woody Savannas"],
                        9:  [0.03,  "Savannas"],
                        10: [0.03,  "Grasslands"],
                        11: [0.055, "Permanent Wetlands"],
                        12: [0.04,  "Croplands"],
                        13: [0.03,  "Urban and Built-Up"],
                        14: [0.04,  "Cropland/Natural Vegetation Mosaic"],
                        15: [0.05,  "Snow and Ice"],
                        16: [0.02,  "Barren or Sparsely Vegetated"],
                        17: [0.06,  "Water"],
                        18: [0.05,  "Wooded Tundra"],
                        19: [0.05,  "Mixed Tundra"],
                        20: [0.02,  "Barren Tundra"]
                    }
    else:
        modis_map = None
       
    return modis_map


def modis2prevah(version):
    if version == 17:
        modis2prevah_map = {
                                "modis": "prevah",
                                0:  1,
                                1:  3,
                                2:  3,
                                3:  4,
                                4:  4,
                                5:  5,
                                6:  8,
                                7:  8,
                                8:  24,
                                9:  21,
                                10: 7,
                                11: 22,
                                12: 6,
                                13: 2,
                                14: 6,
                                15: 14,
                                16: 26
                                }

    elif version == 20:
        modis2prevah_map = {
                                "modis": "prevah",
                                1:  3,
                                2:  3,
                                3:  4,
                                4:  4,
                                5:  5,
                                6:  8,
                                7:  8,
                                8:  24,
                                9:  21,
                                10: 7,
                                11: 22,
                                12: 6,
                                13: 2,
                                14: 6,
                                15: 14,
                                16: 26,
                                17: 1,
                                18: 26,
                                19: 26,
                                20: 26
                                }
    else:
        modis2prevah_map = None
        
    return modis2prevah_map
