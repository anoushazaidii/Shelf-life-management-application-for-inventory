from appV2 import app, db, MaterialDescription

material_descriptions = [
    {'Material Discription': 'ISOCYNATE', 'CODE ': '260007000200', 'shelf_life': 180, 'u_o_m': "PC"},
    {'Material Discription': 'POLYOL FOR CYCLOPENTANE', 'CODE ': '260008000700', 'shelf_life': 180, 'u_o_m': "PC"},
    {'Material Discription': 'AL COOLING POUCH (200x230)MM 500GM', 'CODE ': '121000527100', 'shelf_life': 180, 'u_o_m': "PC"},
    {'Material Discription': 'COOLING BAG 500GM 160X200MM(DF-400 COM)', 'CODE ': '121000875901', 'shelf_life': 180, 'u_o_m': "PC"},
    
]


# material_descriptions = [
#     {'Material Discription': 'ALUMINIUM TAPE 50 mm x 50 m', 'CODE ': '110018000900', 'shelf_life': 180, 'u_o_m': "PC"},
#     {'Material Discription': 'BREATHING NON-WOVEN PAPER TAPE W15 50M', 'CODE ': '110018008500', 'shelf_life': 540, 'u_o_m': ""},
#     {'Material Discription': 'BOPP CLEAR TAPE 48 mm x 50 m x 0.045 mm', 'CODE ': '110018007000', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': '3M DOUBLE ADHESIVE TAPE (WIDTH 491 MM)', 'CODE ': '121000003385', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'DOUBLE ADHESIVE TAPE 0.3x13 mm', 'CODE ': '121000003804', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'BITUM 90X60X2', 'CODE ': '121000023500', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FLUXMATIC LIQUID FLUX', 'CODE ': '260027016500', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'PET POLYEST TAPE (BLUE PRESSURE SENSITIVE TAPE) 0.05X60 (50 M/ROL)', 'CODE ': '110018008400', 'shelf_life': 730, 'u_o_m': ""},
#     {'Material Discription': 'PET POLYEST TAPE (BLUE PRESSURE SENSITIVE TAPE) 0.05X40 (50 M/ROL)', 'CODE ': '110018008300', 'shelf_life': 730, 'u_o_m': ""},
#     {'Material Discription': 'LOGO INVERETER TECHNOLOGY (NEW)- Silver', 'CODE ': '121000001415', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'QC PASS STICKER WITH D LOGO', 'CODE ': '120034005800', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'INVERTER TECHNOLIGY LOGO BLACK PRINT', 'CODE ': '121000003648', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'RIBBON CHINA WAX 110 mm x 450 meter', 'CODE ': '110007000200', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'SILICON LOGO LIMITED EDITION FOR FRZ9195', 'CODE ': '121000871001', 'shelf_life': 365, 'u_o_m': ""},
#     {'Material Discription': 'SILICON LOGO GLASS DOOR FOR FF 9195', 'CODE ': '121000871101', 'shelf_life': 365, 'u_o_m': ""},
#     {'Material Discription': 'COOLING BAG 1000 GRM (SIZE 300X250MM)', 'CODE ': '121000003627', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'COOLING BAG 250 GRAM 80X300MM D60', 'CODE ': '121000038700', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'COOLING BAG 500 GRM D60', 'CODE ': '121000036800', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POLYOL FOR CYCLOPENTANE ICI MA 02804-Y', 'CODE ': '260008000800', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POLYOL FOR CYCLOPENTANE', 'CODE ': '260008000700', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'ISOCYNATE', 'CODE ': '260007000200', 'shelf_life': 365, 'u_o_m': ""},
#     {'Material Discription': 'CYCLOPENTANE (GAS)', 'CODE ': '260006091400', 'shelf_life': 365, 'u_o_m': ""},
#     {'Material Discription': 'REFRIGERANT GAS R-600 A', 'CODE ': '260006079100', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FRZ DOOR SHEET.4x733.5x614D60290HLG I250', 'CODE ': '121000854701', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FRZ DOOR SHEET.4x733.5x514D60270HLG I250', 'CODE ': '121000854501', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'RD SHEET 0.4X733.5X965 D60 FH PLCOPE', 'CODE ': '121000415000', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'FD SHEET 0.4X733.5X514 D60270 FH PLCOPE', 'CODE ': '121000414900', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'FF EVAPORATOR D66 LOC', 'CODE ': '121000393600', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FF EVAPORATOR D76 LOC', 'CODE ': '121000393400', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POT EVAPORATOR FOR FRZ D60270 LOC', 'CODE ': '121000393300', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POT EVAPORATOR FOR FRZ D66360 LOC', 'CODE ': '121000393200', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POT EVAPORATOR FOR FRZ D76465 LOC', 'CODE ': '121000393100', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'VCM SHEET0.4X783X847MM WHITEPEARL HSV087', 'CODE ': '121000315900', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'VCM SHEET0.4X783X1097MM WHITEPEARLHSV087', 'CODE ': '121000315800', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'REF EVAPORATOR FOR DFD NEW', 'CODE ': '121000183300', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'REF EVAPORATOR D76 NEW', 'CODE ': '121000143600', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FF EVAPORATOR 476 X 350MM FOR D66 NEW', 'CODE ': '121000143100', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FRZ DOOR SHEET .4X733.5X614D60290MT.GOLD', 'CODE ': '121000062300', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'VF EVAPORATOR ASSEMBLED & PAINTED', 'CODE ': '121000036600', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POT EVAPORATOR FOR FRZ D76 XXMM', 'CODE ': '121000032700', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'REF EVAPORATOR D76 FOR IOT', 'CODE ': '121000032001', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'CONDENSER D76465', 'CODE ': '121000029200', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'POT EVAPORATOR FOR FRZ D60270 380x270mm', 'CODE ': '121000023900', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'WIRE TYPE CONDENSER D60290 (TUBE=04MM)', 'CODE ': '121000016400', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'WIRE TYPE CONDENSER D73390 (TUBE=04MM)', 'CODE ': '121000016300', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'PLATE TYPE CONDENSER FOR FH TRIM', 'CODE ': '121000014600', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'DOOR SHEET 0.5X733.5X625 MM', 'CODE ': '121000010600', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FRONT FLAP RED 345X148 MM', 'CODE ': '120029000200', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'FRONT FLAP RED 435X148 MM', 'CODE ': '120029000100', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'RED VCM SHEET 0.4X733.5X964MM', 'CODE ': '120028011700', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'RED VCM SHEET 0.4X733.5X614MM', 'CODE ': '120028011600', 'shelf_life': 90, 'u_o_m': ""},
#     {'Material Discription': 'COOLING BAG 750 GRAM', 'CODE ': '120024014200', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'WRINKLE FREE PLATE -FRZ', 'CODE ': '120019040500', 'shelf_life': 180, 'u_o_m': ""},
#     {'Material Discription': 'DHT-11 TEMPERATURE AND HUMIDITY SENSOR', 'CODE ': '121000002236', 'shelf_life': 365, 'u_o_m': ""},
# ]

with app.app_context():
    for material in material_descriptions:
        new_material = MaterialDescription(material_description=material['Material Discription'], code=material['CODE '], shelf_life=material['shelf_life'],u_o_m=material['u_o_m'])
        db.session.add(new_material)
    db.session.commit()