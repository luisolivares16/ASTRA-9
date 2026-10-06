STATION_NAME = 'ASTRA-9'
MAX_CALLSIGN_LENGTH = 20
BASE_SCORE = 50.0
SECURITY_SHIFT = 4


def calculate_clearance(missions, accuracy, penalties, energy=100):
    score = BASE_SCORE
    score += missions * 12
    score += accuracy * 0.25
    score -= penalties * 9
    score += energy // 10

    bonus = missions % 3
    score += bonus ** 2

    risk_gap = abs(100 - accuracy)
    score -= risk_gap / 20
    score -= pow(2, penalties)

    score = round(score, 2)
    tier = int(score // 25)

    return score, tier


def power_diagnostic(power):
    charge = power
    charge += 12
    charge -= 5
    charge *= 2
    charge /= 3
    charge //= 2
    charge %= 7
    charge **= 2

    return charge


def encode_access_phrase(message, encrypt=True):
    shift = SECURITY_SHIFT

    if not encrypt:
        shift = -shift

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

    translation_table = str.maketrans(alphabet, shifted_alphabet)
    encoded_message = message.translate(translation_table)

    return encoded_message


def create_station_pass(
    callsign,
    missions,
    accuracy,
    penalties,
    phrase,
    energy=100,
    encrypt=True
):
    if not isinstance(callsign, str):
        return 'Invalid callsign: must be a string'

    cleaned_callsign = callsign.strip().lower()
    cleaned_callsign = cleaned_callsign.replace('_', '-')

    if not cleaned_callsign:
        return 'Invalid callsign: cannot be empty'

    if len(cleaned_callsign) > MAX_CALLSIGN_LENGTH:
        return f'Invalid callsign: must be at most {MAX_CALLSIGN_LENGTH} characters'

    if ' ' in cleaned_callsign:
        return 'Invalid callsign: cannot contain spaces'

    if not cleaned_callsign.startswith('cadet-'):
        return 'Invalid callsign: must start with "cadet-"'

    if cleaned_callsign.endswith('-'):
        return 'Invalid callsign: cannot end with -'

    if cleaned_callsign.count('-') != 2:
        return 'Invalid callsign: must contain exactly two hyphens'

    if cleaned_callsign.find('admin') != -1:
        return 'Invalid callsign: reserved name'

    alias = cleaned_callsign[6:]
    alias_parts = alias.split('-')
    display_name = ' '.join(alias_parts).title()

    if callsign.isupper():
        input_case = 'Upper'
    elif callsign.islower():
        input_case = 'Lower'
    else:
        input_case = 'Mixed'

    short_code = (alias[:3] + alias[-2:]).upper()

    if not isinstance(missions, int):
        return 'Invalid missions: must be an integer'

    if missions < 0:
        return 'Invalid missions: must be non-negative'

    if not isinstance(accuracy, (int, float)):
        return 'Invalid accuracy: must be a number'

    if accuracy < 0 or accuracy > 100:
        return 'Invalid accuracy: must be between 0 and 100'

    if not isinstance(penalties, int) or penalties < 0:
        return 'Invalid penalties: must be a non-negative integer'

    if not isinstance(energy, (int, float)) or energy < 0 or energy > 100:
        return 'Invalid energy: must be a number between 0 and 100'

    if not isinstance(phrase, str):
        return 'Invalid phrase: must be a string'

    score, tier = calculate_clearance(
        missions,
        accuracy,
        penalties,
        energy
    )

    encoded_phrase = encode_access_phrase(phrase, encrypt)
    diagnostic = power_diagnostic(energy)

    if score >= 130:
        if phrase and phrase[0] == '!':
            status = 'Priority'
        else:
            status = 'Approved'
    elif score >= 90:
        status = 'Limited'
    else:
        status = 'Denied'

    if encrypt:
        mode_label = 'encrypted'.capitalize()
    else:
        mode_label = 'decrypted'.capitalize()

    report = f'{STATION_NAME} ACCESS PASS'
    report += f'\nPilot: {display_name}'
    report += f'\nCode: {short_code}'
    report += f'\nInput case: {input_case}'
    report += f'\nStatus: {status}'
    report += f'\nClearance: {score}'
    report += f'\nTier: {tier}'
    report += f'\nMode: {mode_label}'
    report += f'\nAccess phrase: {encoded_phrase}'
    report += f'\nDiagnostic: {diagnostic}'

    return report
def run_terminal():
    print('=== ASTRA-9 ACCESS TERMINAL ===')
    callsign = input('Enter your callsign: ')
    missions = int(input('Enter number of missions completed: '))
    accuracy = float(input('Enter accuracy:'))
    penalties = int(input('Enter penalties: '))
    energy = float(input('Enter energy level: '))
    phrase = input('Enter access phrase: ')
    encrypt_choice = input('Encrypt access phrase? (y/n): ')
    encrypt = encrypt_choice.replace(' ', '').lower() == 'y'
    result = create_station_pass(callsign, missions, accuracy, penalties, phrase, energy, encrypt)
    print(result)
run_terminal()