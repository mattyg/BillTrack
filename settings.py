import sys

# Bill Names [prefix][number]-[congress]
HOUSE_BILL = 'hr3811-112'
SENATE_BILL = 's2041-112'


# Supportive groups (Codes in CRP_categories.txt, data available at maplight.org) 
GROUPS_SUPPORT = ['E01','LC150','LB100','M2000','G1100','J4000']

# Oppossition groups (Codes from CRP_categories.txt, data available at maplight.org)
GROUPS_OPPOSE = ['Q11']

# Big influencer groups (Codes from CRP_categories.txt, data available at maplight.org)
GROUPS_BIGPLAYERS = ['E1110']

# Years to calculate donations from
DONATION_YEARS = ['2010','2011','2012']


# Sunlight API Key (get yours here: http://services.sunlightlabs.com/)
API_KEY = 'b281fd9d3a124f53970f623de12b0596'


# Path to root BillTrack dir (with trailing slash)
MAIN_PATH = '/home/matt/CodingProjects/BillTrack/'

# Path to templates directory
TEMPLATES_PATH = MAIN_PATH+'templates/'

# Path to sqlite database file
DATABASE_PATH = MAIN_PATH+'db/kxltrackdata.db'

# Path to packages directory
PACKAGES_PATH = MAIN_PATH+'vendor/'

sys.path.append(PACKAGES_PATH)
GROUPS_SUPPORT_STRING = '|'.join(GROUPS_SUPPORT)
GROUPS_OPPOSE_STRING = '|'.join(GROUPS_OPPOSE)
DONATION_YEARS_STRING = '|'.join(DONATION_YEARS)
