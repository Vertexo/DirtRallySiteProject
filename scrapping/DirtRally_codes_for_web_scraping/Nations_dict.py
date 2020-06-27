

# Based on integer key gets country's name.
def nations(nation_number):
    nations_dict = {1: 'England', 2: 'United States', 3: 'Japan', 4: 'Germany', 5: 'Scotland',
                    6: 'France', 7: 'Italy', 8: 'Spain', 9: 'Canada', 10: 'NO COUNTRY',
                    11: 'Belgium', 12: 'Turkey', 13: 'Portugal', 14: 'Finland', 15: 'Brazil',
                    16: 'Netherlands', 17: 'Ireland', 18: 'Austria', 19: 'Greece', 20: 'Luxembourg',
                    21: 'Slovenia', 22: 'Cyprus', 23: 'NO COUNTRY', 24: 'Australia', 25: 'Argentina',
                    26: 'Bulgaria', 27: 'NO COUNTRY', 28: 'China', 29: 'Croatia', 30: 'Czech Republic',
                    31: 'Denmark', 32: 'Estonia', 33: 'Slovakia', 34: 'Hungary', 35: 'Iceland',
                    36: 'India', 37: 'Indonesia', 38: 'Jamaica', 39: 'Jordan', 40: 'Latvia',
                    41: 'Lithuania', 42: 'Malaysia', 43: 'Mexico', 44: 'New Zealand', 45: 'Northern Ireland',
                    46: 'Norway', 47: 'Pakistan', 48: 'Poland', 49: 'Romania', 50: 'Russia',
                    51: 'Saudi Arabia', 52: 'NO COUNTRY', 53: 'South Africa', 54: 'Switzerland', 55: 'Thailand',
                    56: 'World', 57: 'Wales', 58: 'Bahrain', 59: 'NO COUNTRY', 60: 'NO COUNTRY',
                    61: 'NO COUNTRY', 62: 'Serbia', 63: 'South Korea', 64: 'Sweden', 65: 'United Arab Emirates',
                    66: 'NO COUNTRY', 67: 'NO COUNTRY', 68: 'NO COUNTRY', 69: 'Hong Kong', 70: 'Ecuador',
                    71: 'Cuba', 72: 'Venezuela', 73: 'Ghana', 74: 'Cameroon', 75: 'United Kingdom',
                    76: 'NO COUNTRY', 77: 'Isle of Man', 78: 'Kuwait', 79: 'Oman', 80: 'Qatar',
                    81: 'Yemen', 82: 'Nigeria', 83: 'Chile', 84: 'Kenya', 85: 'Monaco',
                    86: 'Ukraine', 87: 'Israel', 88: 'Colombia', 89: 'NO COUNTRY', 90: 'NO COUNTRY',
                    91: 'NO COUNTRY', 92: 'NO COUNTRY', 93: 'NO COUNTRY', 94: 'NO COUNTRY', 95: 'NO COUNTRY',
                    96: 'NO COUNTRY', 97: 'NO COUNTRY', 98: 'NO COUNTRY', 99: 'NO COUNTRY', 100: 'NO COUNTRY',
                    }

    return nations_dict.setdefault(nation_number, 'NO COUNTRY')
