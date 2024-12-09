from pysondb import db

medlemmer = db.getDb('medlemmer.json')
tilmeldinger = db.getDb('tilmeldinger.json')

# Denne funktion genererer en string ud fra en tabel i pysonDB-format i mere læsbart format
def table_to_text(table):
    out = ''
    for row in table:
        for field in row.values():
            out += str(field) + '\t'
        out += '\n'
    return out

# Denne funktion returnerer en liste af hold fra tabellen 'Tilmeldinger' uden dubletter
def find_unique_teams():
    data = tilmeldinger.getAll()
    disc = []
    for row in data:
        if row['Disciplin'] not in disc:
            disc.append(row['Disciplin'])
    return disc


# Denne funktion returnerer en liste af navne, som har en tilmelding på den valgte disciplin
def generate_team_list(discipline):
    listNamefromDiscipline = []
    disciplines = tilmeldinger.getBy({'Disciplin':discipline})
    for row in disciplines:
        persons = medlemmer.getBy({'Medlemsnummer':row['Medlem']})
        listNamefromDiscipline.append(persons[0]['Navn'])
    return listNamefromDiscipline


# Denne funktion tilføjer et medlem til tabellen 'Medlemmer'
def add_member(name, birthdate, fee):
    valid = False
    number = len(medlemmer.getAll())
    for medlem in medlemmer.getAll():
        if medlem['Navn']==name and medlem['Fødselsdag']==birthdate and medlem['Kontingent']==fee:
            valid = True
            break
    if not valid:
        medlemmer.add({'Medlemsnummer':number + 1, 'Navn':name, 'Fødselsdag':birthdate, 'Kontingent':fee})

# Denne funktion tilføjer en tilmelding til tabellen 'Tilmeldinger'
def add_participant(member_id, discipline, is_coach):
    valid = False
    for entry in tilmeldinger.getAll():
        if entry['Medlem']==member_id and entry['Disciplin']==discipline:
            valid = True
            break
    if not valid:
        tilmeldinger.add({'Medlem': member_id, 'Disciplin': discipline, 'Træner': is_coach})

#funktion som kan ændre træner status og sportsgræn for medlemmer
#benytter .update til at gøre dette (orignal data til dict)
#(nye data skal ændres til derefter)
member_id = input('enter memeber id')
def modifyMember(member_id, is_coach):
    for entry in tilmeldinger.getAll():
        if entry['id'] == member_id:
            tilmeldinger.update({'Træner':false, 'Træner':true, 'Disciplin':''}, {'Træner':true})






if __name__ == '__main__':
    print(table_to_text(medlemmer.getAll()))
    print(table_to_text(tilmeldinger.getAll()))

    ## Test af løsning på opgaver ##

    # Find og print discipliner
    hold = find_unique_teams()
    print(hold)

    # Print holdlister
    for h in hold:
        print(h)
        print(generate_team_list(h))

    # Tilføj medlemmer
    add_member('Alidia McGoon', '1950-10-17', 150)
    add_member('Osgood Tollet', '1979-09-30', 200)

    # Meld medlemmer på disciplin
    add_participant(9, 'Kapgang', True)
    add_participant(10, 'Kapgang', False)