from addict import Dict
import db
import random
import re
import microsoft

babyProds = [
  "The First Years Stack Up Cups",
  "Mommy's Helper Outlet Plugs, 36 Count",
  "Nuby Ice Gel Teether Keys",
  "Medela Breast Milk Storage Bags, 100 count Ready to Use Milk Storage Bags for Breastfeeding, Self…",
  "Summer Infant Contoured Changing Pad",
  "OXO Tot Grape Cutter, Teal",
  "Regalo Easy Step 39-Inch Extra Wide Baby Gate, Bonus Kit, Includes 6-Inch Extension Kit, 4 Pack…",
  "Infant Optics DXR-8 Video Baby Monitor with Interchangeable Optical Lens",
  "Munchkin Arm & Hammer Diaper Pail Snap, Seal and Toss Refill Bags, 20 Bags, Holds 600 Diapers",
  "ChoiceRefill Compatible with Diaper Genie Pails, 4-Pack, 1080 Count",
  "Philips Avent SCF190/01 Soothie 0-3mth Green/Green, 2pk",
  "Munchkin Miracle 360 Trainer Cup, Green/Blue, 7 Ounce, 2 Count",
  "Baby Banana Infant Training Toothbrush and Teether, Yellow",
  "Baby Einstein Take Along Tunes Musical Toy",
  "Haakaa Silicone Breastfeeding Manual Breast Pump Milk Pump 100% Food Grade Silicone BPA…",
  "OXO Tot Bottle Brush with Nipple Cleaner and Stand, Gray",
  "Infantino Flip 4-in-1 Convertible Carrier",
  "Philips AVENT Soothie Pacifier, 0-3 Months, 2-Pack, Pink/Purple",
  "American Baby Company Waterproof Fitted Crib and Toddler Protective Mattress Pad Cover, White",
  "Sposie Booster Pads Diaper Doubler, 90 Count, 3 Packs of 30 Pads",
  "Fisher-Price Sit-Me-Up Floor Seat",
  "Hatch Baby Rest Night Light, Sound Machine and Time-to-Rise",
  "Graco SnugRide Click Connect 30/35 LX Infant Car Seat Base, Black, One Size",
  "Baby Einstein Octoplush Plush Toy",
  "Skip Hop Moby Bath Tear-Free Waterfall Rinser Bath Cup, Blue",
  "Playtex Diaper Genie Complete Assembled Diaper Pail with Odor Lock Technology & 1 Full Size…",
  "Graco Premium Foam Crib & Toddler Bed Mattress, Water Resistant Breathable Foam Crib & Toddler…",
  "Munchkin Waterproof Changing Pad Liners, 3 Count",
  "Summer Infant My Size Potty - Training Toilet for Toddler Boys & Girls - with Flushing Sounds and…",
  "ThermoPro TP65 Digital Wireless Hygrometer Indoor Outdoor Thermometer Wireless…",
  "Gund Baby Animated Flappy The Elephant Plush Toy",
  "Dekor Plus Diaper Pail Refills | Most Economical Refill System | Quick & Easy to Replace | No…",
  "The First Years Take & Toss Spill-Proof Sippy Cups, 10 Ounce, 4 Count",
  "Munchkin 2 Piece Snack Catcher, Blue/Green",
  "Enovoe Car Window Shade - (4 Pack) - 21\"x14\" Cling Sunshade for Car Windows - Sun, Glare…",
  "Sassy Developmental Bumpy Ball",
  "Philips AVENT Bottle Warmer, Fast",
  "Fridababy NoseFrida Nasal Aspirator with 20 Extra Hygiene Filters",
  "Munchkin Float and Play Bubbles Bath Toy, 4 Count",
  "Metene Medical Forehead and Ear Thermometer,Infrared Digital Thermometer…",
  "Gerber Birdseye 3-Ply Prefold Cloth Diapers, White, 10 Count",
  "Munchkin Warm Glow Wipe Warmer",
  "Graco Affix Youth Booster Seat with Latch System, Atomic, One Size",
  "Boppy Newborn Lounger, Elephant Love Gray",
  "Graco Simple Sway Baby Swing, Abbington, One Size",
  "Diaper Genie Playtex Carbon Filter Refill Tray for Diaper Pails, 4 Carbon Filters",
  "Dr. Brown's 3 Piece Bottle Brush",
  "Munchkin Miracle 360 Sippy Cup, Green/Blue, 10 Ounce, 2 Count",
  "Sassy Wonder Wheel Activity Center",
  "Oball Shaker"
]

electronics = [
  "Google WiFi system, 3-Pack - Router replacement for whole home coverage (NLS-1304-25)",
  "Fire 7 Tablet with Alexa, 7\" Display, 8 GB, Black - with Special Offers",
  "All-New Fire HD 8 Tablet | Hands-Free with Alexa | 8\" HD Display, 16 GB, Black - with Special Offers",
  "Fire HD 10 Tablet with Alexa Hands-Free, 10.1\" 1080p Full HD Display, 32 GB, Black - with…",
  "NETGEAR R6700 Nighthawk AC1750 Dual Band Smart WiFi Router, Gigabit Ethernet (R6700)",
  "Fire 7 Tablet with Alexa, 7\" Display, 8 GB, Marine Blue - with Special Offers",
  "Intel Core i7-8700K Desktop Processor 6 Cores up to 4.7GHz Turbo Unlocked LGA1151 300 Series…",
  "HP Pavilion 21.5-Inch IPS LED HDMI VGA Monitor (22cwa)",
  "ONIKUMA Stereo Gaming Headset for PS4, Xbox One, PC, Enhanced 7.1 Surround Sound,…",
  "Anker 4-Port USB 3.0 Ultra Slim Data Hub for Macbook, Mac Pro/mini, iMac, Surface Pro, XPS,…",
  "Fire 7 Tablet with Alexa, 7\" Display, 8 GB, Punch Red - with Special Offers",
  "HP 23.8-inch FHD IPS Monitor with Tilt/Height Adjustment and Built-in Speakers (VH240a, Black)",
  "Fire 7 Kids Edition Tablet, 7\" Display, 16 GB, Blue Kid-Proof Case",
  "Fire 7 Kids Edition Tablet, 7\" Display, 16 GB, Pink Kid-Proof Case",
  "NETGEAR CM500-1AZNAS (16x4) DOCSIS 3.0 Cable Modem, Max download speeds of…",
  "Google WiFi system, 1-Pack - Router replacement for whole home coverage - NLS-1304-25",
  "All-New Fire HD 8 Kids Edition Tablet, 8\" HD Display, 32 GB, Blue Kid-Proof Case",
  "TP-Link AC1750 Smart WiFi Router - 5GHz Dual Band Gigabit Wireless Internet Routers for…",
  "Sabrent 4-Port USB 2.0 Hub with Individual Power Switches and LEDs (HB-UMLS)",
  "TP-Link AC750 Dual Band WiFi Range Extender, Repeater, Access Point w/Mini Housing Design,…",
  "Certified Refurbished Fire HD 8 Tablet with Alexa, 8\" HD Display, 32 GB, Black - with Special Offers",
  "Acer Aspire E 15, 15.6\" Full HD, 8th Gen Intel Core i3-8130U, 6GB RAM Memory, 1TB HDD, 8X DVD,…",
  "Fire HD 10 Tablet with Alexa Hands-Free, 10.1\" 1080p Full HD Display, 32 GB, Marine Blue - with…",
  "Sceptre E205W-1600 20\" 75Hz Ultra Thin LED Monitor HDMI VGA Build-in Speakers, Metallic…",
  "All-New Fire HD 8 Kids Edition Tablet, 8\" HD Display, 32 GB, Pink Kid-Proof Case",
  "Netgear (R7000-100PAS) Nighthawk AC1900 Dual Band WiFi Router, Gigabit Router, Open Source…",
  "Fosmon Xbox One/One X/One S Controller Charger, [Dual Slot] High Speed Docking…",
  "Apple iPad 2 MC769LL/A 9.7-Inch 16GB (Black) 1395 - (Certified Refurbished)",
  "Sceptre E248W-19203R 24\" Ultra Thin 75Hz 1080p LED Monitor 2X HDMI VGA Build-in…",
  "Fire 7 Tablet with Alexa, 7\" Display, 8 GB, Canary Yellow - with Special Offers",
  "MOSPRO Trail Camera Viewer for iPhone iPad Mac & Android, SD & Micro SD Memory Card Reader…",
  "Microsoft Surface Dock (PD9-00003)",
  "ASUS Whole Home Dual-Band AiMesh Router (AC1900) for Mesh Wifi System (Up to 1900…",
  "All-New Fire HD 8 Tablet | Hands-Free with Alexa | 8\" HD Display, 16 GB, Marine Blue - with Special…",
  "Acer SB220Q bi 21.5\" Full HD (1920 x 1080) IPS Ultra-Thin Zero Frame Monitor (HDMI & VGA Port)",
  "Cool Sticker 100pcs Random Music Film Vinyl Skateboard Guitar Travel Case Sticker Door…",
  "SanDisk 128GB microSDXC UHS-I card for Nintendo Switch - SDSQXAO-128G-GN6ZA",
  "NETGEAR Gigabit Cable Modem (32x8) DOCSIS 3.1 | for XFINITY by Comcast and Cox. Compatible…",
  "NETGEAR Orbi Ultra-Performance Whole Home Mesh WiFi System - fastest WiFi router and…",
  "NETGEAR AC1200 Dual Band Smart WiFi Router, Gigabit Ethernet (R6230)",
  "HyperX Cloud II Gaming Headset - 7.1 Surround Sound - Memory Foam Ear Pads - Durable…",
  "ASUS Chromebook C202SA-YS02 11.6\" Ruggedized and Water Resistant Design with…",
  "Fire HD 10 Tablet with Alexa Hands-Free, 10.1\" 1080p Full HD Display, 32 GB, Punch Red - with…",
  "Intel Core i9-9900K Desktop Processor 8 Cores up to 5.0 GHz Turbo Unlocked LGA1151 300 Series…",
  "TP-Link N450 Wi-Fi Router - Wireless Internet Router for Home(TL-WR940N)",
  "All-New Fire HD 8 Tablet | Hands-Free with Alexa | 8\" HD Display, 32 GB, Black - with Special Offers",
  "ARRIS SURFboard SB6190 32x8 DOCSIS 3.0 Cable Modem - Retail Packaging - White",
  "All-New Fire HD 8 Tablet | Hands-Free with Alexa | 8\" HD Display, 16 GB, Punch Red - with Special…",
  "Apple MagSafe 60W Power Adapter for MacBook MC461LL/A (for MacBook and 13-inch MacBook…",
  "Fire HD 10 Tablet with Alexa Hands-Free, 10.1\" 1080p Full HD Display, 64 GB, Black - with…"
]

pets = [
  "Pampers Swaddlers Disposable Diapers",
  "Dr. Elsey's Cat Ultra Premium Clumping Cat Litter  ( Pack May Vary )",
  "Pampers Swaddlers Disposable Diapers",
  "AmazonBasics Pet Training and Puppy Pads",
  "Pampers Swaddlers Disposable Diapers",
  "Taste of the Wild Grain Free High Protein Dry Dog Food High Prairie Adult - Venison & Bison",
  "Greenies Dog Dental Chews Dog Treats - Teenie Size (5-15 lb Dogs)",
  "Purina Fancy Feast Medleys",
  "Arm & Hammer Clump & Seal Platinum Litter, Multi-Cat,",
  "AmazonBasics Dog Waste Bags with Dispenser and Leash Clip, Standard and EPI Additive (meets…",
  "Greenies Dog Dental Chews Dog Treats - Regular Size (25-50 lb Dogs)",
  "PetSafe ScoopFree Self-Cleaning Cat Litter Box Tray Refills, Non-Clumping Crystal Cat Litter, 3…",
  "Bayer Seresto Flea and Tick Collar for Dogs",
  "Greenies Pill Pocket Soft Dog Treats - Chicken",
  "Rocco & Roxie Professional Strength Stain & Odor Eliminator - Enzyme-Powered Pet Odor & Stain…",
  "Novartis Capstar Flea Tablets for Dogs and Cats",
  "Blue Buffalo Life Protection Formula Natural Adult Dry Dog Food, Chicken and Brown Rice",
  ".Fresh Step Ultra Unscented Litter, Clumping Cat Litter, 20 Pounds",
  "Carefresh Complete Pet Bedding",
  "TOMSENN Dog Lion Mane - Realistic & Funny Lion Mane for Dogs - Complementary Lion Mane for…",
  "Earth Rated Poop Bags Dog Waste Bags, Refill Rolls",
  "Greenies Dog Dental Chews Dog Treats - Petite Size (15-25 lb Dogs)",
  "Petrodex Enzymatic Toothpaste Dog Poultry Flavor, 6.2 oz",
  "Pampers Swaddlers Disposable Diapers",
  "Nutramax Cosequin DS Plus with MSM Chewable Tablets",
  "Purina Fancy Feast Medleys",
  ".Arm & Hammer Ultra Last Litter, 40 Lbs (Packaging May Vary)",
  "Providence Engraving Pet ID Tags | 8 Shapes & Colors to Choose From | Dog Cat Aluminum",
  "Purina Tidy Cats LightWeight Glade Tough Odor Solutions Clumping Cat Litter",
  "Pampers Swaddlers Disposable Diapers",
  "Pampers Swaddlers Disposable Diapers",
  "Milk-BoneMilk-Bone",
  "Pet King Brands Zymox Otic Pet Ear Treatment with Hydrocortisone",
  "Pedigree Dentastix Original Large Treats Dogs, 32 Treats",
  "Greenies Dog Dental Chews Dog Treats - Large Size (50-100 lb Dogs)",
  "[Upgrade Version] Pet Grooming Glove - Gentle Deshedding Brush Glove - Efficient Pet Hair…",
  "Bayer Advantage II Flea Prevention for Cats",
  "Purina Fancy Feast Medleys",
  "Petrainer PET998DRB1 Dog Training Collar Rechargeable and Rainproof 330 yd Remote Dog…",
  "Wellness Natural Grain Free Puppy Training Treats",
  "Hefty Strong Large 30 Gallon Trash Bags - Multipurpose - Drawstring - 74 Count",
  "Fresh Step UltraCare Febreze Freshness, Clumping Cat Litter",
  "Purina Fortiflora Canine Nutritional Supplement Box",
  "Comfort Zone Calming Diffuser Refills",
  "Dog Nail Clippers and Trimmer By Boshel - With Safety Guard to Avoid Over-cutting Nails & Free…",
  "Milk-Bone Original Dog Treats",
  "PetSafe RFA-67D-11 6 Volt Battery (Pack of 2)",
  "Pampers Swaddlers Disposable Diapers Size",
  "Petmate 71034 Arm & Hammer Swivel Bin & Rake Pooper Scooper, Scented Bags Included, One…",
  "TEMPTATIONS Mixup Treats for Cats 16 ounces"
]

sitesIds = random.sample(list(range(1000000)), 50)
for i in range(1, 5):
    percentBaby = 1 - i * .7
    percentElectronics = i * 0.1
    percentPets = i * .2
    lat = random.random() * 3 + 36.5
    long = random.random() * 20 + -140
    siteId = sitesIds[i]
    db.writeSQL("INSERT into SITES values ({}, {}, {})".format( siteId, long, lat))
    numOrders = random.randint(0, 2000) + 50
    for i in range(1, numOrders):
        itemId = random.random() * 1000000
        actualAmount = random.random() * 10 + 11;
        dice = random.random()
        if dice < percentBaby:
            itemName = babyProds[random.randint(0,49)]
        elif dice > percentBaby and dice < (1 - percentPets):
            itemName = electronics[random.randint(0,49)]
        else:
            itemName = pets[random.randint(0,49)]
        itemName = re.sub('\'', '', itemName)
        itemName = re.sub(',', '', itemName)
        itemName = re.sub('/', '', itemName)
        itemName = re.sub('-', '', itemName)
        itemName = re.sub('ā', 'a', itemName)
        itemName = re.sub('ā', 'a', itemName)
        db.writeSQL("INSERT into \"dbo\".\"individualItems\" (ncrItemId, price, description) values (N\'{}\', {}, N\'{}\')".format(itemId, actualAmount, itemName))
        possibleMatch =  db.readSQL("SELECT id from individualItems where ncrItemId = N\'{}\' and price = {}".format(itemId, actualAmount))
        weekDay = random.randint(0,6)
        hour = random.randint(0,23)
        query = "INSERT into \"dbo\".\"individualTransactions\" (indItemId, dayOfWeek, hourOfDay, siteId) values ({}, {}, {}, N\'{}\' )".format(possibleMatch[0][0], weekDay, hour, siteId)
        db.writeSQL(query)
#
ids = db.readSQL("SELECT individualTransactions.id from individualTransactions left join categories on categories.id = categoryId where categories.description is null");
ids = [tranId[0] for tranId in ids]
for tranId in ids:
    microsoft.generateConceptForTransaction(tranId)
