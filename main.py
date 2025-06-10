from pyswip import Prolog
import ast
import math
import curses

prolog = Prolog()
prolog.consult("planer.pl")
prolog.consult("time.pl")

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

# Object oriented programming
class prolog_decrypter():
    def __init__(self):
        pass
    def decrypt_time(self, time_list):
        result = []
        for i in time_list:
            clean = i.strip("-")
            clean = clean.replace("time", "")
            tup = ast.literal_eval(clean)
            result.append(tup)
        return result

# Procedural programming
def generate_schedules():
    return list(prolog.query("all_schedules(Result)"))[0]["Result"]

def input_professors():
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(1, 1, "Please input the names and surnames of the teachers.", curses.color_pair(4))
    current_y = 3
    current_subject_y = 1
    przedmioty = []
    slownik = {}
    inp = ""
    while True:
        stdscr.addstr(current_y - 2, 60, "Name and surname, at the end input 0: ", curses.color_pair(3))
        inp = str(stdscr.getstr(current_y - 1, 60, 30)).removeprefix("b").replace("'", "")
        if inp == "0":
            break
        stdscr.addstr(current_y, 10, inp, curses.color_pair(5))
        inp2 = ""
        current_subject_y = 1
        while True:
            stdscr.addstr(current_y - 2, 60, "                                                  ")
            stdscr.addstr(current_y - 2, 60, "Subjects, at the end input 0: ", curses.color_pair(3))
            stdscr.addstr(current_y - 1, 60, " " * 30)
            inp2 = str(stdscr.getstr(current_y - 1, 60, 30)).removeprefix("b").replace("'", "")
            if inp2 == "0":
                break
                inp2 = ""
            stdscr.addstr(current_y + current_subject_y, 10, " └----" + inp2, curses.color_pair(6))
            przedmioty.append(inp2.replace(" ", "_"))
            current_subject_y += 1
        slownik[inp.replace(" ", "_")] = przedmioty.copy()
        przedmioty.clear()
        current_y += current_subject_y + 2
    return slownik

# Programowanie strukturalne
def assert_professors_to_prolog(prowadzace):
    prolog.retractall("course(_, _)")
    prolog.retractall("teacher(_)")
    for i in prowadzace.keys():
        prolog.asserta(f"teacher('{str(i).lower()}')")
        for j in prowadzace[i]:
            prolog.asserta(f"course('{str(j).lower()}', '{str(i).lower()}')")

def assert_times_to_prolog(times):
    prolog.retractall("slot(_)")
    for i in range(len(times)):
        prolog.asserta(f"slot({str(i)})")

def display_schedule(plan, godziny, numer):
    stdscr.attroff(curses.color_pair(1))
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.color_pair(3))
    stdscr.attroff(curses.color_pair(4))
    stdscr.attroff(curses.color_pair(5))
    stdscr.attroff(curses.color_pair(6))
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 1, numer, curses.color_pair(5))
    zajecia = {}
    current_y = 0
    for godzina in godziny:
        zajecia[godzina] = []
    for j in range(len(plan)):
        entry = list(prolog.query(f"get_entry_data({plan[j]}, Przedmiot, Prowadzacy, Godzina, Sala)"))[0]
        godzina = entry["Godzina"]
        zajecia[godziny[godzina]].append(entry)
    current_color = 0
    for godzina in zajecia.keys():
        current_color += 1
        stdscr.attron(curses.color_pair(current_color % 2 + 1))
        stdscr.attron(curses.A_BOLD)
        current_y += 1
        hours = godzina[0][0]
        minutes = godzina[0][1]
        hours2 = godzina[1][0]
        minutes2 = godzina[1][1]
        time1 = " " * (1 - math.floor(len(str(hours)) / 2)) + str(hours) + ":" + str(minutes) * max(1, 2 * (len(str(minutes)) == 1))
        time2 = " " * (1 - math.floor(len(str(hours2)) / 2)) + str(hours2) + ":" + str(minutes2) * max(1, 2 * (len(str(minutes2)) == 1))
        stdscr.addstr(current_y * 3 - 1, 1, " " + " " * len(time1) + "   " + " " * len(time2) + " ")
        stdscr.addstr(current_y * 3, 1, " " + time1 + " - " + time2 + " ")
        stdscr.addstr(current_y * 3 + 1, 1, " " + " " * len(time1) + "   " + " " * len(time2) + " ")
        stdscr.attroff(curses.color_pair(current_color % 2 + 1))
        current_x = 0
        for entry in zajecia[godzina]:
            to_display = f"{entry["Przedmiot"].replace("_", " ")}: {entry["Prowadzacy"].replace("_", " ")}. Sala {entry["Sala"]} | "
            stdscr.addstr(current_y * 3, len(time1 + " - " + time2 + " |  ") + current_x, to_display, curses.color_pair(current_color % 2 + 3))
            current_x += len(to_display)
        stdscr.attroff(curses.color_pair(current_color % 2 + 1))
        stdscr.attroff(curses.A_BOLD)
        stdscr.refresh()

def display_schedules(plany, godziny):
    current_schedule = 0
    display_schedule(plany[current_schedule], godziny, f"Schedule variant number {current_schedule + 1}/{len(plany)}:")
    stdscr.keypad(True)
    curses.noecho()
    while True:
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT:
            current_schedule = (current_schedule - 1) % len(plany)
        elif inp == curses.KEY_RIGHT:
            current_schedule = (current_schedule + 1) % len(plany)
        elif inp == curses.KEY_UP:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break
        display_schedule(plany[current_schedule], godziny, f"Schedule variant number {current_schedule + 1}/{len(plany)}:")
        stdscr.refresh()

def intro():
    curses.echo()
    curses.cbreak()
    stdscr.addstr(1, 1, "Input the hour the classes should start: ", curses.color_pair(5))
    start = int(stdscr.getstr(2, 1, 2))
    stdscr.addstr(3, 1, "Input the hour the classes should end: ", curses.color_pair(6))
    finisz = int(stdscr.getstr(4, 1, 2))
    stdscr.addstr(5, 1, "Input how long should the class last(in minutes): ", curses.color_pair(5))
    ile_trwaja = int(stdscr.getstr(6, 1, 2))
    stdscr.addstr(7, 1, "Input how long should the recess be(in minutes): ", curses.color_pair(6))
    przerwa = int(stdscr.getstr(8, 1, 2))
    stdscr.refresh()
    query = f"time_to_minutes({start}, 0, Start), time_to_minutes({finisz}, 0, End), ClassDuration is {ile_trwaja}, Recess is {przerwa}, schedule_classes(Start, End, ClassDuration, Recess, Classes)"
    decrypter = prolog_decrypter()
    prolog_list = list(prolog.query(query))[0]["Classes"]
    decrypted = decrypter.decrypt_time(prolog_list)
    prowadzace = input_professors()
    assert_times_to_prolog(decrypted)
    assert_professors_to_prolog(prowadzace)
    plany = generate_schedules()
    display_schedules(plany, decrypted)

if __name__ == "__main__":
    curses.wrapper(intro())
    stdscr.keypad(True)