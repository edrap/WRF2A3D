# -*- coding: utf-8 -*-

def sno_gen(statname, virnum, statlon, statlat, statalt, ProfileDate, sno_path):

    vir_common = "BareSoil_z0 = 0.03\nSoilAlbedo = 0.25\nCanopyLeafAreaIndex = 0\nCanopyHeight = 0\nCanopyDirectThroughfall = 1\nnSoilLayerData = 0\nnodata = -999\ntz = 1\nHS_Last = 0.0\nSlopeAngle = 0\nSlopeAzi = 0\nnSnowLayerData = 0\nWindScalingFactor = 0\nErosionLevel = 0\nTimeCountDeltaHS = 0\nfields = timestamp Layer_Thick T Vol_Frac_I Vol_Frac_W Vol_Frac_V Vol_Frac_S Rho_S Conduc_S HeatCapac_S rg rb dd sp mk mass_hoar ne CDot metamo\n[DATA]\n"

    fw1_path = sno_path+statname+".sno"
    open(fw1_path, "w").close()

    with open(fw1_path, "a") as fw1:

        fw1.write("SMET 1.1 ASCII\n")
        fw1.write("[HEADER]\n")
        fw1.write("station_id = %d\n" % virnum)
        fw1.write("station_name = %s\n" % statname)
        fw1.write("longitude = %f\n" % statlon)
        fw1.write("latitude = %f\n" % statlat)
        fw1.write("altitude = %f\n" % statalt)
        fw1.write("ProfileDate = %s\n" % ProfileDate)

        fw1.write(vir_common)

def vstat_gen(stat, virnum, statlon, statlat, statalt):
    statname = stat.replace(", ", "-").replace(" ", "_").replace("'", "").lower()
    print("VSTATION"+str(virnum), "= latlon", statlat, statlon, statalt)
    print("SNOWFILE"+str(virnum), "=",statname+".sno\n")

def vstat_gen_csv(stat, virnum, statlon, statlat, statalt):
    statname = stat.replace(", ", "-").replace(" ", "_").replace("'", "").lower()
    print("CSV"+str(virnum)+"_NAME =", stat)
    print("CSV"+str(virnum)+"_ID =", virnum)
    print("CSV"+str(virnum)+"_NR_HEADERS = 1")
    print("CSV"+str(virnum)+"_COLUMNS_HEADERS = 1")
    print("STATION"+str(virnum),"=", statname+".csv")
    print("POSITION"+str(virnum), "= latlon", statlat, statlon, statalt)
    print("SNOWFILE"+str(virnum), "=",statname+".sno\n")

def sno_gen_soil(ds, dss, ProfileDate, nSoilLayerData, fr1, prevah_map, modis_map, modis2preva_map, i, j, fw1_path, virnum, stat):
    
    statname = stat.replace(", ", "-").replace(" ", "_").replace("'", "").lower()

    with open(fw1_path, "a") as fw1:

        fw1.write("SMET 1.1 ASCII\n")
        fw1.write("[HEADER]\n")
        fw1.write("station_id = %s\n" % str(virnum))
        fw1.write("station_name = %s\n" % stat)
        fw1.write("longitude = %f\n" % ds.lon[j].values)
        fw1.write("latitude = %f\n" % ds.lat[i].values)
        fw1.write("altitude = %f\n" % ds["HGT"][0,i,j].values)
        fw1.write("ProfileDate = %s\n" % ProfileDate)

        lui_modis = int(ds["LU_INDEX"][0,i,j].values)
        lui_prevah = int(ds["LUS"][0,i,j].values)

        BareSoil_z0 = modis_map[lui_modis][0]
        fw1.write("BareSoil_z0 = %f\n" % BareSoil_z0)

        fw1.write("SoilAlbedo = %f\n" % ds["ALBBCK"][0,i,j].values)
        fw1.write("CanopyLeafAreaIndex = %f\n" % ds["LAI"][0,i,j].values)

        CanopyHeight = prevah_map[lui_prevah][1]
        fw1.write("CanopyHeight = %f\n" % CanopyHeight)
        CanopyDirectThroughfall = prevah_map[lui_prevah][3]
        fw1.write("CanopyDirectThroughfall = %f\n" % CanopyDirectThroughfall)

        fw1.write("nSoilLayerData = %d\n" % nSoilLayerData)

        fw1.write(fr1)

        for k in range(nSoilLayerData-1, -1, -1):

            Layer_Thick = dss["DZS"][k]
            T = dss["TSLB"][0, k, i, j]
            Vol_Frac_W = dss["SH2O"][0, k, i, j]
            Vol_Frac_V = 0.
            Vol_Frac_I = dss["SMOIS"][0, k, i, j] - dss["SH2O"][0, k, i, j]
            Vol_Frac_S = 1. - dss["SMOIS"][0, k, i, j]
            Rho_S = 2600.0
            Conduc_S = 0.9
            HeatCapac_S = 1000
            rg = 3.5
            rb = 0
            dd = 0
            sp = 0
            mk = 0
            mass_hoar = 0
            ne = 1
            CDot = 0
            metamo = 0

            fw1.write("%s %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %d %f %f\n" % (ProfileDate, Layer_Thick, T, Vol_Frac_I, Vol_Frac_W, Vol_Frac_V, Vol_Frac_S, Rho_S, Conduc_S, HeatCapac_S, rg, rb, dd, sp, mk, mass_hoar, ne, CDot, metamo))
